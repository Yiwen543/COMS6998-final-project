"""Bounded process groups for the registered public G1 profile only."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def execute(budget, job, folder, env):
    started = time.monotonic()
    limit = budget.reserve(job['kind'], job['id'], job.get('cycles', 0))
    folder.mkdir(exist_ok=False)
    stdout, stderr = folder / 'stdout.log', folder / 'stderr.log'
    receipt = dict(argv=job['argv'], kind=job['kind'], job_id=job['id'],
        status='ERROR', exit_code=None, timed_out=False,
        process_group=None, observed_processes=[], child_pid_inventory_complete=False,
        child_cost_policy='All descendants belong to this logical batch job and its wall/cleanup deadline; verbose compiler/build commands retained. PID sampling is best effort, not an exhaustive spawn count.',
        monitor_calls=0, cleanup_group_kill=False)
    proc = None
    observed = set()
    deadline = started + limit
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            proc = subprocess.Popen(job['argv'], cwd=folder, env=env,
                stdout=out, stderr=err, start_new_session=True)
            receipt['process_group'] = proc.pid
            while proc.poll() is None:
                if time.monotonic() >= deadline - 0.25:
                    receipt['timed_out'] = True
                    os.killpg(proc.pid, signal.SIGKILL)
                    break
                # Record only our group; no unrelated argv/environment is saved.
                if deadline - time.monotonic() > 0.35:
                    ps = subprocess.run(['/bin/ps', '-ax', '-o', 'pid=,ppid=,pgid=,comm='],
                        env=env, capture_output=True, text=True, timeout=0.1)
                    receipt['monitor_calls'] += 1
                    for line in ps.stdout.splitlines():
                        fields = line.split(None, 3)
                        if len(fields) == 4 and fields[2] == str(proc.pid):
                            observed.add(tuple(fields))
                time.sleep(min(0.01, max(0, deadline - 0.25 - time.monotonic())))
            proc.wait(timeout=max(0.01, deadline - time.monotonic()))
            receipt['exit_code'] = proc.returncode
            receipt['status'] = 'TIMEOUT' if receipt['timed_out'] else 'RETURNED'
    except Exception as error:
        receipt['error'] = type(error).__name__ + ':' + str(error)
    finally:
        if proc is not None:
            try:
                os.killpg(proc.pid, 0)
                os.killpg(proc.pid, signal.SIGKILL)
                receipt['cleanup_group_kill'] = True
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=max(0.01, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                receipt['status'] = 'CLEANUP_UNRESOLVED'
        receipt['observed_processes'] = [list(x) for x in sorted(observed)]
        receipt['elapsed_seconds_including_cleanup'] = time.monotonic() - started
        receipt['job_timeout_cap_seconds'] = limit
        if receipt['elapsed_seconds_including_cleanup'] > limit:
            receipt['status'] = 'JOB_WALL_CAP_EXCEEDED'
        receipt['stdout_sha256'] = hashlib.sha256(stdout.read_bytes()).hexdigest() if stdout.exists() else None
        receipt['stderr_sha256'] = hashlib.sha256(stderr.read_bytes()).hexdigest() if stderr.exists() else None
        budget.terminal(job['id'], receipt)
        (folder / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if receipt['status'] != 'RETURNED' or receipt['cleanup_group_kill']:
        budget.halt('PROCESS_FAILURE_TIMEOUT_OR_LINGERING_GROUP:' + job['id'])
    return receipt
