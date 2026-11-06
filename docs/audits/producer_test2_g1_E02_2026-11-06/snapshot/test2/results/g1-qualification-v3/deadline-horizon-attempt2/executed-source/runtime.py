"""Owned process-group protection; no external inventory command is dispatched."""
import hashlib
import json
import os
import signal
import subprocess
import time
from budget import Refuse


def execute(budget, job, folder, env, inventory_probe=None):
    """inventory_probe is an injectable mock hook; the registered runner passes None."""
    started = time.monotonic()
    stdout, stderr = folder / 'stdout.log', folder / 'stderr.log'
    inventory = dict(mode='owned_process_group_only', complete=False,
        availability='UNAVAILABLE_KNOWN_FROM_PREDECESSOR', attempts=0,
        current_error=None, predecessor_error=budget.allocation.inventory_predecessor_error,
        predecessor_pool_sha256=dict(budget.allocation.predecessor_bindings)['pool'],
        elapsed_seconds=0, records=[])
    receipt = dict(argv=job['argv'], kind=job['kind'], job_id=job['id'],
        status='ERROR', exit_code=None, root_exit_knownness='UNKNOWN', timed_out=False,
        process_group=None, process_group_basis='POSIX start_new_session=True creates child PID=PGID',
        observed_processes=[], child_pid_inventory_complete=False, inventory=inventory,
        child_cost_policy='Owned PGID/deadline/poll/kill/wait mandatory; child compiler commands in raw build logs. No external PID scan; full child census unavailable.',
        cleanup_group_kill=False, dispatch_attempted=False, mandatory_errors=[])
    proc = None
    deadline = None
    operation = 'RESERVE'

    def observed_exit(code, method):
        if type(code) is not int:
            raise RuntimeError('INVALID_ROOT_EXIT_FROM_' + method)
        receipt['exit_code'] = code
        receipt['root_exit_knownness'] = 'KNOWN_FROM_' + method

    def optional_inventory():
        if inventory_probe is None:
            return  # no ps, no scanner, no new permission dependency
        inventory['mode'] = 'MOCK_INJECTED_OPTIONAL_INVENTORY'
        inventory['attempts'] += 1
        began = time.monotonic()
        try:
            inventory['records'] = inventory_probe(proc.pid)
            inventory['availability'] = 'AVAILABLE_MOCK_RECORDS_ONLY'
        except (PermissionError, OSError, subprocess.TimeoutExpired) as error:
            inventory['availability'] = 'UNAVAILABLE_OPTIONAL_ERROR'
            inventory['current_error'] = type(error).__name__ + ':' + str(error)
        finally:
            inventory['elapsed_seconds'] += time.monotonic() - began

    try:
        budget.reserve(job['kind'], job['id'], job.get('cycles', 0), started_at=started)
        deadline = budget.event(job['id'])['absolute_job_deadline']
        operation = 'PREPARE_LOGS'
        folder.mkdir(exist_ok=False)
        with stdout.open('xb') as out, stderr.open('xb') as err:
            receipt['remaining_at_last_dispatch_check'] = budget.pre_dispatch_window(job['id'])
            receipt['dispatch_attempted'] = True
            operation = 'POPEN_OWN_SESSION'
            proc = subprocess.Popen(job['argv'], cwd=folder, env=env,
                stdout=out, stderr=err, start_new_session=True)
            receipt['process_group'] = proc.pid
            optional_inventory()
            while True:
                operation = 'POLL'
                code = proc.poll()
                if code is not None:
                    observed_exit(code, 'POLL')
                    break
                if time.monotonic() >= deadline - 0.25:
                    receipt['timed_out'] = True
                    operation = 'TIMEOUT_KILL_OWN_GROUP'
                    os.killpg(proc.pid, signal.SIGKILL)
                    receipt['timeout_group_kill'] = True
                    break
                time.sleep(min(0.01, max(0, deadline - 0.25 - time.monotonic())))
            operation = 'WAIT'
            observed_exit(proc.wait(timeout=max(0.01, deadline - time.monotonic())), 'WAIT')
            receipt['status'] = 'TIMEOUT' if receipt['timed_out'] else 'RETURNED'
    except Refuse as error:
        receipt['status'] = 'NOT_RUN'
        receipt['refusal_reason'] = str(error)
    except Exception as error:
        receipt['mandatory_errors'].append(dict(operation=operation,
            error=type(error).__name__ + ':' + str(error)))
        receipt['status'] = 'PROTECTION_OR_EXECUTION_ERROR'
    finally:
        if deadline is None and budget.event(job['id']) is not None:
            deadline = budget.event(job['id']).get('absolute_job_deadline')
        if proc is not None:
            group_present = False
            try:
                os.killpg(proc.pid, 0)
                group_present = True
                receipt['owned_group_probe'] = 'PRESENT'
            except ProcessLookupError:
                receipt['owned_group_probe'] = 'ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS'
            except OSError as error:
                receipt['owned_group_probe'] = 'UNKNOWN_REQUIRED_API_FAILED'
                receipt['mandatory_errors'].append(dict(operation='OWNED_GROUP_PROBE',
                    error=type(error).__name__ + ':' + str(error)))
            if group_present:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                    receipt['cleanup_group_kill'] = True
                except OSError as error:
                    receipt['mandatory_errors'].append(dict(operation='CLEANUP_KILL_OWN_GROUP',
                        error=type(error).__name__ + ':' + str(error)))
            try:
                observed_exit(proc.wait(timeout=max(0.01, deadline - time.monotonic())), 'CLEANUP_WAIT')
            except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
                receipt['mandatory_errors'].append(dict(operation='CLEANUP_WAIT',
                    error=type(error).__name__ + ':' + str(error)))
            if receipt['mandatory_errors']:
                receipt['status'] = 'PROTECTION_UNRESOLVED'
        receipt['elapsed_seconds_including_cleanup'] = time.monotonic() - started
        receipt['absolute_job_deadline'] = deadline
        receipt['job_timeout_cap_seconds'] = budget.caps[job['kind'] + '_timeout']
        if proc is not None and time.monotonic() > deadline:
            receipt['status'] = 'JOB_WALL_CAP_EXCEEDED'
        receipt['stdout_sha256'] = hashlib.sha256(stdout.read_bytes()).hexdigest() if stdout.exists() else None
        receipt['stderr_sha256'] = hashlib.sha256(stderr.read_bytes()).hexdigest() if stderr.exists() else None
        if receipt['status'] == 'NOT_RUN':
            budget.no_dispatch_receipt(job['id'], job['kind'], receipt)
        else:
            budget.terminal(job['id'], receipt)
        if not folder.exists():
            folder.mkdir(exist_ok=False)
        with (folder / 'receipt.json').open('x') as stream:
            stream.write(json.dumps(receipt, indent=2) + '\n')
    if receipt['status'] != 'RETURNED' or receipt['cleanup_group_kill'] or receipt['mandatory_errors']:
        budget.halt('REQUIRED_PROTECTION_PROCESS_OR_DEADLINE_FAILURE:' + job['id'])
    return receipt
