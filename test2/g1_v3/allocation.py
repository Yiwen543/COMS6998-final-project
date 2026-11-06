"""Narrow, hash-bound R03 continuation of the immutable E01 grant/pool."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json

DECISION_SHA = '1f1e0214e69da41acee8974f2421df375c3c4cb8a499c2d148675bc741acde71'
GRANT_SHA = 'bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab'
POOL_SHA = '6da4346144d65356f57c5762058675f1acca9f1dad4ee8599c889dc49e1a7400'
P11_SHA = '6588231c1ddd0e71b8879e32ea944b40a8d6fe7a871fcf3ed918c669b13723db'
PHASE_SHA = '6fd9815afc1d8ae58cb6764ed3f1f40ec85ca49c2320751b1b6421cad4a3cd14'
PRIOR = {'compile': 0, 'native': 0, 'physical': 0, 'physical_cycles': 0, 'setup': 1}
PRIOR_ACTUAL = 0.04572445806115866
CUMULATIVE_CAPS = dict(compile_jobs=32, native_jobs=32, physical_jobs=32,
    physical_cycles=1024, cycles_per_run=32, wall_seconds=1200, setup_jobs=8,
    compile_timeout=20, native_timeout=10, physical_timeout=2, setup_timeout=2)


class AllocationError(ValueError):
    pass


def check(condition, message):
    if not condition:
        raise AllocationError(message)


def digest(path):
    path = Path(path)
    check(not path.is_symlink() and path.is_file(), 'MISSING_OR_SYMLINK_PREDECESSOR:' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Allocation:
    prior_reserved: tuple
    prior_actual_seconds: float
    prior_charge_seconds: int
    attempt_window_seconds: int
    predecessor_bindings: tuple
    inventory_predecessor_error: str

    def validate(self):
        check(dict(self.prior_reserved) == PRIOR and
              all(type(v) is int for _, v in self.prior_reserved), 'FALSE_PRIOR_COUNTS')
        check(type(self.prior_actual_seconds) is float and self.prior_actual_seconds == PRIOR_ACTUAL,
              'FALSE_PRIOR_ACTUAL_WINDOW')
        check(type(self.prior_charge_seconds) is int and self.prior_charge_seconds == 2,
              'FALSE_PRIOR_CONSERVATIVE_CHARGE')
        check(type(self.attempt_window_seconds) is int and self.attempt_window_seconds == 1198,
              'EXPANDED_ATTEMPT_WINDOW')
        expected = {'decision': DECISION_SHA, 'grant': GRANT_SHA,
                    'pool': POOL_SHA, 'review': P11_SHA, 'phase': PHASE_SHA}
        check(dict(self.predecessor_bindings) == expected, 'MISSING_OR_FALSE_PREDECESSOR_BINDINGS')
        check('PermissionError' in self.inventory_predecessor_error and
              '/bin/ps' in self.inventory_predecessor_error, 'MISSING_INVENTORY_PREDECESSOR_ERROR')


def load_allocation(root, reg):
    root = Path(root)
    expected = [('continuation_decision', 'continuation_decision_sha256', DECISION_SHA),
        ('user_authorization', 'user_authorization_sha256', GRANT_SHA),
        ('predecessor_pool', 'predecessor_pool_sha256', POOL_SHA),
        ('predecessor_review', 'predecessor_review_sha256', P11_SHA),
        ('predecessor_phase', 'predecessor_phase_sha256', PHASE_SHA)]
    for path_key, hash_key, fixed in expected:
        check(path_key in reg and hash_key in reg, 'MISSING_PREDECESSOR_FIELD:' + path_key)
        check(reg[hash_key] == fixed and digest(root / reg[path_key]) == fixed,
              'PREDECESSOR_HASH_DRIFT:' + path_key)
    decision = json.loads((root / reg['continuation_decision']).read_text())
    old = json.loads((root / reg['predecessor_pool']).read_text())
    for key in ['predecessor_pool', 'predecessor_phase', 'predecessor_review']:
        check(reg[key] == decision[key], 'PREDECESSOR_PATH_DRIFT:' + key)
    check(reg['user_authorization'] == decision['original_user_authorization'], 'GRANT_PATH_DRIFT')
    check(old['halted'] is True and old['completed'] is True, 'PREDECESSOR_NOT_TERMINAL')
    check(old['reserved'] == decision['prior_reserved'] == reg['prior_reserved'] == PRIOR,
          'FALSE_PRIOR_COUNTS')
    check(all(type(value) is int for value in reg['prior_reserved'].values()), 'PRIOR_COUNT_TYPES')
    check(old['total_elapsed_seconds'] == decision['predecessor_actual_window_seconds'] ==
          reg['prior_actual_window_seconds'] == PRIOR_ACTUAL, 'FALSE_PRIOR_ACTUAL_WINDOW')
    check(type(reg['prior_wall_charge_seconds']) is int and
          reg['prior_wall_charge_seconds'] == decision['prior_wall_charge_seconds'] == 2,
          'FALSE_PRIOR_CONSERVATIVE_CHARGE')
    check(type(reg['attempt_maximum_window_seconds']) is int and reg['attempt_maximum_window_seconds'] ==
          decision['retry_maximum_remaining']['execution_wall_seconds'] == 1198, 'EXPANDED_ATTEMPT_WINDOW')
    check(reg['remaining_allocation'] == decision['retry_maximum_remaining'], 'EXPANDED_REMAINING_ALLOCATION')
    cumulative = decision['cumulative_caps'].copy()
    check(cumulative.pop('native_depth') == reg['native_depth'] == 8, 'NATIVE_DEPTH')
    check(cumulative == reg['caps'], 'CUMULATIVE_CAPS_DRIFT')
    for kind in ['compile', 'native', 'physical', 'setup']:
        check(reg['remaining_allocation'][kind + '_jobs'] ==
              reg['caps'][kind + '_jobs'] - PRIOR[kind], 'REMAINING_COUNT_DRIFT:' + kind)
    check(reg['remaining_allocation']['physical_cycles'] == 1024, 'REMAINING_CYCLES')
    check(reg['caps']['wall_seconds'] == 1200 and 2 + 1198 == reg['caps']['wall_seconds'], 'WALL_ALLOCATION')
    check(reg['process_supervision'] == 'owned_process_group_only', 'NO_NEW_PROCESS_PERMISSION')
    check(reg['pool_state'] == reg['result_root'] + '/execution-state.json' and
          reg['pool_state'] != reg['predecessor_pool'], 'MUST_NOT_REOPEN_PREDECESSOR')
    allocation = Allocation(tuple(sorted(PRIOR.items())), PRIOR_ACTUAL, 2, 1198,
        tuple(sorted({'decision': DECISION_SHA, 'grant': GRANT_SHA, 'pool': POOL_SHA,
                      'review': P11_SHA, 'phase': PHASE_SHA}.items())), old['events'][0]['error'])
    allocation.validate()
    return allocation
