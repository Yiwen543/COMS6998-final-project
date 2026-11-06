"""Capture one exact registered G1 entry invocation; no retry or new authority."""
from pathlib import Path
import hashlib,json,os,subprocess,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent
receipt=R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r05b.json'
assert hashlib.sha256(receipt.read_bytes()).hexdigest()=='82f56b7855e228b43a1f951a2e5d8f7bbd6dd835f1ecce3a5b09678142ae2dcc'
for n in ['execution-state.json','attempt.lock']:assert not (R/'test2/results/g1-qualification-v5b'/n).exists()
cmd=[str(R/'.venv/bin/python'),'test2/g1_v5b/runner.py','--execute-authorization',str(receipt.relative_to(R))]
record={'status':'ENTRY_CAPTURE_STARTED','command':cmd,'cwd':str(R),'start_epoch':time.time(),'scope':'Outer entry capture is separate from the authoritative registered G1 pool timer.','retry':False}
file=A/'entry-receipt.json'
with file.open('x') as f:json.dump(record,f,indent=2)
start=time.monotonic()
try:
 with (A/'entry.stdout.log').open('xb') as out,(A/'entry.stderr.log').open('xb') as err:
  result=subprocess.run(cmd,cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=out,stderr=err)
 record.update(status='ENTRY_RETURNED',exit_code=result.returncode,outer_elapsed_seconds=time.monotonic()-start,end_epoch=time.time())
except Exception as e:
 record.update(status='OUTER_CAPTURE_ERROR',error=type(e).__name__+':'+str(e),outer_elapsed_seconds=time.monotonic()-start,end_epoch=time.time())
 file.write_text(json.dumps(record,indent=2)+'\n');raise
file.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2));raise SystemExit(result.returncode)
