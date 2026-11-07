"""Read-only saved queue evidence arithmetic; no toolchain, network, or imports from project."""
import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'results/queue_bc_gpt6sol_20261026'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

paths = [
    'configs/queue_bc_pilot_gpt6sol.json',
    'results/queue_bc_gpt6sol_20261026/REPORT.md',
    'results/queue_bc_gpt6sol_20261026/target_costs.csv',
    'results/queue_bc_gpt6sol_20261026/metadata.json',
    'results/queue_bc_gpt6sol_20261026/semantic-proof.json',
    'results/queue_bc_gpt6sol_20261026/claude_audit_v2/disposition.md',
    'docs/heldout_queue_preflight.md', 'docs/claude_queue_crosscheck.md',
    'examples/heldout_queue/provenance.json',
    'examples/heldout_queue/docs/specification.md',
    'examples/heldout_queue/verif/tb_queue_pilot.sv',
    'scripts/queue_feedback.py', 'scripts/queue_reference.py',
    'scripts/run_queue_bc_pilot.py',
]
config = json.loads((ROOT / paths[0]).read_text())
bindings = {
    'spec': 'examples/heldout_queue/docs/specification.md',
    'checker': 'examples/heldout_queue/verif/tb_queue_pilot.sv',
    'feedback': 'scripts/queue_feedback.py',
    'engine': 'egraph/src/main.rs',
    'driver': 'scripts/sim_main_queue.cpp',
    'original': 'examples/heldout_queue/rtl/queue.sv',
    'variant': 'examples/heldout_queue/rtl/queue_variant.sv',
}
binding_results = {k: {'path': v, 'sha256': sha(ROOT / v),
    'matches_config': sha(ROOT / v) == config[k + '_sha256']} for k, v in bindings.items()}
rows = list(csv.DictReader((BASE / 'target_costs.csv').open()))
assert len(rows) == 12
arithmetic = {}
earlier = 0
for version in ('original', 'variant'):
    means = {a: sum(Fraction(int(r['api_tokens'])) for r in rows
        if r['version'] == version and r['arm'] == a) / 3 for a in ('B', 'C')}
    rounds = {a: [int(r['first_target_round']) for r in rows
        if r['version'] == version and r['arm'] == a] for a in ('B', 'C')}
    earlier += sum(c < b for b, c in zip(rounds['B'], rounds['C']))
    arithmetic[version] = {'mean_tokens_exact': {a: str(v) for a,v in means.items()},
        'C_minus_B_percent': float(100 * (means['C'] / means['B'] - 1)),
        'target_rounds_by_repetition_index': rounds}
metadata = json.loads((BASE / 'metadata.json').read_text())
proof = json.loads((BASE / 'semantic-proof.json').read_text())
assert len([p for g in proof['groups'] for p in g['pair_proofs']]) == proof['total_pair_proofs'] == 22
# A current-file mismatch is evidence to report, not permission to alter history.
skills = [Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md'),
    Path('/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md')]
result = {
    'phase': 'P21_LEGACY_METHOD_CHECKPOINT',
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'inputs': {p: sha(ROOT / p) for p in paths},
    'config_binding_checks': binding_results,
    'target_arithmetic': arithmetic, 'C_earlier_index_comparisons': earlier,
    'seed_and_ceiling': {k: {'initial': v['initial_coverage'],
        'ceiling': v['reference_ceiling']['coverage']} for k,v in metadata['version_setups'].items()},
    'saved_pair_proofs_count_only': proof['total_pair_proofs'],
    'proofs_freshly_executed': False,
    'hallmark_source_hashes': {str(p): sha(p) for p in skills},
    'draft_directory_existed_at_check': (ROOT / 'docs/designs/queue_efficiency_ablation_v1').exists(),
    'review_script_sha256': sha(Path(__file__)),
    'limits': ['Saved CSV/JSON arithmetic and current binding checks only.',
        'No raw replay, no new equivalence proof, no fee pricing verification.',
        'No sealed new design identity received; no exact-design acceptance.'],
}
print(json.dumps(result, indent=2))
