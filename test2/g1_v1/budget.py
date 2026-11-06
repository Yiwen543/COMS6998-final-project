"""Single non-resumable shared G1 budget. No tool dispatch in this module."""
import json
import os
import time
from pathlib import Path


class Refuse(RuntimeError):
    pass


class Budget:
    def __init__(self, path, caps, clock=time.monotonic):
        if any(type(value) is not int or value <= 0 for value in caps.values()):
            raise Refuse('CAPS_REQUIRE_POSITIVE_EXACT_INTEGERS')
        self.path = Path(path)
        self.clock = clock
        self.caps = caps.copy()
        self.start = clock()
        self.state = dict(start_monotonic=self.start, start_epoch=time.time(),
            caps=self.caps, reserved={'compile': 0, 'native': 0, 'physical': 0,
                                      'physical_cycles': 0, 'setup': 0},
            halted=False, halt_reason=None, events=[], completed=False)
        # Existing state, including a crash or previous profile, never resets.
        with self.path.open('x') as stream:
            json.dump(self.state, stream)
            stream.flush()
            os.fsync(stream.fileno())

    def save(self):
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

    def reserve(self, kind, job_id, cycles=0):
        if self.state['halted'] or self.state['completed']:
            raise Refuse('GLOBAL_HALT_OR_CLOSED')
        if self.elapsed() >= self.caps['wall_seconds'] - 5:
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
        self.state['events'].append(dict(job_id=job_id, kind=kind,
            status='RESERVED_BEFORE_DISPATCH', reserved_cycles=cycles,
            reserved_at_elapsed=self.elapsed()))
        self.save()
        return min(self.caps[kind + '_timeout'],
                   self.caps['wall_seconds'] - 5 - self.elapsed())

    def terminal(self, job_id, receipt):
        event = next(e for e in self.state['events'] if e['job_id'] == job_id)
        if event['status'] != 'RESERVED_BEFORE_DISPATCH':
            raise Refuse('DUPLICATE_TERMINAL')
        event.update(receipt)
        event['terminal_at_elapsed'] = self.elapsed()
        self.save()

    def complete(self):
        if self.elapsed() > self.caps['wall_seconds']:
            self.halt('TOTAL_WALL_CAP_EXCEEDED')
        self.state['completed'] = True
        self.state['total_elapsed_seconds'] = self.elapsed()
        self.state['remaining'] = {k: self.caps[k + '_jobs'] -
            self.state['reserved'][k] for k in ['compile', 'native', 'physical']}
        self.state['remaining']['physical_cycles'] = (
            self.caps['physical_cycles'] - self.state['reserved']['physical_cycles'])
        self.save()
