"""Run the new domain-scoped screen without changing historical runners."""
import argparse
from pathlib import Path
from run_midterm_fixed import ROOT
from real_parent_screen import replace
import screen_transaction_recovery as runner
import hierarchy_netlist_proof as proof_module
from wbxbar_conditional_semantics import SCOPE,ConditionalAdapter,ConditionalBitVectors,ConditionalNetlist,verify_certificate
from wbxbar_domain_proof import prove

def run(out):
    verify_certificate()
    code=runner.CODE+[Path(__file__).resolve(),ROOT/'scripts/wbxbar_domain_proof.py',ROOT/'scripts/wbxbar_conditional_semantics.py']
    with replace(runner,SCOPE=SCOPE,CODE=code,TransactionAdapter=ConditionalAdapter,TransactionBitVectors=ConditionalBitVectors,ObservationNetlist=ConditionalNetlist),replace(proof_module,prove=prove):
        runner.run('wbxbar',out,True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.output.resolve())
