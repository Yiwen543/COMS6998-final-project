"""Single non-resumable shared G1 budget. No tool dispatch in this module."""
import json
import os
import time
from pathlib import Path
from allocation import Allocation, CUMULATIVE_CAPS


class Refuse(RuntimeError):
    pass


class Budget:
    def __init__(self, path, caps, clock=time.monotonic, allocation=None, started_at=None):
        if any(type(value) is not int or value <= 0 for value in caps.values()):
            raise Refuse('CAPS_REQUIRE_POSITIVE_EXACT_INTEGERS')
        if not isinstance(allocation, Allocation):
            raise Refuse('MISSING_VERIFIED_CONTINUATION')
        allocation.validate()
        if caps != CUMULATIVE_CAPS:
            raise Refuse('CUMULATIVE_CAPS_MUST_MATCH_ORIGINAL_GRANT')
        self.path = Path(path)
        self.clock = clock
        self.caps = caps.copy()
        now = clock()
        self.start = now if started_at is None else started_at
        if self.start > now:
            raise Refuse('FUTURE_CLOCK_ORIGIN')
        self.attempt_window = allocation.attempt_window_seconds
        self.work_deadline = self.start + self.attempt_window - 5
        self.allocation = allocation
        self.state = dict(start_monotonic=self.start, start_epoch=time.time(),
            attempt_id='R05_CUMULATIVE_CONTINUATION',
            caps=self.caps, reserved=dict(allocation.prior_reserved),
            reserved_scope='CUMULATIVE_INCLUDING_PREDECESSOR',
            prior_reserved=dict(allocation.prior_reserved),
            attempt_reserved={'compile': 0, 'native': 0, 'physical': 0,
                              'physical_cycles': 0, 'setup': 0},
            predecessor_bindings=dict(allocation.predecessor_bindings),
            predecessor_pool_stays_immutable=True,
            prior_actual_window_seconds=allocation.prior_actual_seconds,
            prior_conservative_charge_seconds=allocation.prior_charge_seconds,
            prior_charge_is_not_measured_spend=True,
            cumulative_actual_window_seconds=allocation.prior_actual_seconds,
            cumulative_charged_window_seconds=allocation.prior_charge_seconds,
            current_attempt_window_seconds=self.attempt_window,
            start_epoch_scope='LEDGER_CREATION_EPOCH;window origin is start_monotonic',
            halted=False, halt_reason=None, events=[], completed=False)
        # Existing state, including a crash or previous profile, never resets.
        with self.path.open('x') as stream:
            json.dump(self.state, stream)
            stream.flush()
            os.fsync(stream.fileno())

    def save(self):
        self.state['attempt_elapsed_checkpoint_seconds'] = self.elapsed()
        self.state['cumulative_actual_window_seconds'] = self.allocation.prior_actual_seconds + self.elapsed()
        self.state['cumulative_charged_window_seconds'] = self.allocation.prior_charge_seconds + self.elapsed()
        temp = self.path.with_suffix('.tmp')
        with temp.open('x') as stream:
            json.dump(self.state, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, self.path)

    def elapsed(self):
        return self.clock() - self.start

    def halt(self, reason):
        self.state['halted'] = True
        self.state['halt_reason'] = self.state['halt_reason'] or reason
        self.save()

    def event(self, job_id):
        return next((e for e in self.state['events'] if e['job_id'] == job_id), None)

    def pre_dispatch_window(self, job_id):
        event = self.event(job_id)
        if event is None or event['status'] != 'RESERVED_BEFORE_DISPATCH':
            raise Refuse('NO_OPEN_RESERVATION')
        now = self.clock()
        remaining = min(event['absolute_job_deadline'],
                        self.work_deadline) - now
        if self.state['halted'] or self.state['completed'] or remaining <= 0.25:
            reason = 'INSUFFICIENT_DEADLINE_BEFORE_DISPATCH'
            event.update(status='NOT_RUN', dispatch_state='CHARGED_NOT_DISPATCHED',
                refusal_reason=reason, terminal_at_elapsed=self.elapsed(),
                remaining_at_refusal=remaining)
            self.halt(reason)
            raise Refuse(reason)
        return remaining

    def no_dispatch_receipt(self, job_id, kind, receipt):
        event = self.event(job_id)
        if event is None:
            self.state['events'].append(dict(job_id=job_id, kind=kind,
                status='NOT_RUN', dispatch_state='UNRESERVED_NOT_DISPATCHED',
                reserved_cycles=0, terminal_at_elapsed=self.elapsed(), process_receipt=receipt))
        elif event['status'] in ['RESERVED_BEFORE_DISPATCH', 'NOT_RUN']:
            event.update(status='NOT_RUN', dispatch_state='CHARGED_NOT_DISPATCHED',
                         terminal_at_elapsed=self.elapsed(), process_receipt=receipt)
        else:
            self.state.setdefault('refused_duplicate_dispatches', []).append(
                dict(job_id=job_id, process_receipt=receipt))
        self.save()

    def reserve(self, kind, job_id, cycles=0, started_at=None):
        if self.state['halted'] or self.state['completed']:
            raise Refuse('GLOBAL_HALT_OR_CLOSED')
        if self.clock() >= self.work_deadline:
            self.halt('GLOBAL_WORK_DEADLINE')
            raise Refuse('GLOBAL_WORK_DEADLINE')
        if any(e['job_id'] == job_id for e in self.state['events']):
            raise Refuse('DUPLICATE_JOB_NO_RETRY')
        if kind not in ['setup', 'compile', 'native', 'physical']:
            raise Refuse('UNREGISTERED_JOB_KIND')
        if type(cycles) is not int or cycles < 0 or (kind != 'physical' and cycles):
            raise Refuse('CYCLE_TYPE_OR_KIND')
        used = self.state['reserved']
        cap = self.caps.get(kind + '_jobs')
        if cap is not None and used[kind] >= cap:
            self.halt('JOB_CAP_' + kind)
            raise Refuse('JOB_CAP_' + kind)
        if kind == 'physical' and (cycles > self.caps['cycles_per_run'] or
                used['physical_cycles'] + cycles > self.caps['physical_cycles']):
            self.halt('PHYSICAL_CYCLE_CAP')
            raise Refuse('PHYSICAL_CYCLE_CAP')
        used[kind] += 1
        used['physical_cycles'] += cycles
        self.state['attempt_reserved'][kind] += 1
        self.state['attempt_reserved']['physical_cycles'] += cycles
        job_start = self.clock() if started_at is None else started_at
        deadline = min(job_start + self.caps[kind + '_timeout'],
                       self.work_deadline)
        self.state['events'].append(dict(job_id=job_id, kind=kind,
            status='RESERVED_BEFORE_DISPATCH', reserved_cycles=cycles,
            reserved_at_elapsed=self.elapsed(), absolute_job_start=job_start,
            absolute_job_deadline=deadline))
        self.save()
        # Persistence itself may consume the complete window. Reservations are
        # charged permanently even when no process can be dispatched afterwards.
        return self.pre_dispatch_window(job_id)

    def terminal(self, job_id, receipt):
        event = next(e for e in self.state['events'] if e['job_id'] == job_id)
        if event['status'] != 'RESERVED_BEFORE_DISPATCH':
            raise Refuse('DUPLICATE_TERMINAL')
        event.update(receipt)
        event['terminal_at_elapsed'] = self.elapsed()
        self.save()

    def complete(self):
        if self.elapsed() > self.attempt_window:
            self.halt('REMAINING_ATTEMPT_WALL_CAP_EXCEEDED')
        self.state['completed'] = True
        self.state['total_elapsed_seconds'] = self.elapsed()
        self.state['total_elapsed_scope'] = 'CURRENT_ATTEMPT_ONLY'
        self.state['cumulative_actual_window_seconds'] = self.allocation.prior_actual_seconds + self.elapsed()
        self.state['cumulative_charged_window_seconds'] = self.allocation.prior_charge_seconds + self.elapsed()
        if self.state['cumulative_charged_window_seconds'] > self.caps['wall_seconds']:
            self.halt('CUMULATIVE_WALL_CAP_EXCEEDED')
        self.state['remaining'] = {k: self.caps[k + '_jobs'] -
            self.state['reserved'][k] for k in ['compile', 'native', 'physical', 'setup']}
        self.state['remaining']['physical_cycles'] = (
            self.caps['physical_cycles'] - self.state['reserved']['physical_cycles'])
        self.save()
        # The terminal ledger write is inside the same attempt window. A slow
        # fsync/replace cannot turn an observed cap crossing into success.
        finished_elapsed = self.elapsed()
        if (finished_elapsed > self.attempt_window or
                self.allocation.prior_charge_seconds + finished_elapsed >
                self.caps['wall_seconds']):
            self.state['halted'] = True
            self.state['halt_reason'] = (self.state['halt_reason'] or
                'FINAL_PERSISTENCE_EXCEEDED_CUMULATIVE_WALL_CAP')
            self.state['total_elapsed_seconds'] = finished_elapsed
            self.state['late_final_persistence_elapsed_seconds'] = finished_elapsed
            self.save()
