"""New six-round release;does not modify the frozen 36-round release."""
from pathlib import Path
import json
from resources import require,sha
ARMS=('B2_raw','C2_semantic')
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def expected(reg):return {(a,1,n) for a,n in reg['schedule']}
def freeze(root,directory,context,status):
    files={str(p.relative_to(root)):sha(p) for p in directory.rglob('*') if p.is_file() and p.name!='snapshot.json'}
    data=dict(context,status=status,directory=str(directory.relative_to(root)),files=files);p=directory/'snapshot.json'
    require(not p.exists(),'SNAPSHOT_ALREADY_EXISTS');dump(p,data);return dict(snapshot=str(p.relative_to(root)),sha256=sha(p))
def checked(root,row):
    p=(root/row['snapshot']).resolve();require(p.is_relative_to(root.resolve()) and sha(p)==row['sha256'],'SNAPSHOT_DRIFT');d=json.loads(p.read_text())
    for n,h in d['files'].items():
        f=(root/n).resolve();require(f.is_relative_to(root.resolve()) and sha(f)==h,'ROUND_ARTIFACT_DRIFT')
    if d['status']=='compiled':
        require(all(d['directory']+'/compiled/'+n in d['files'] for n in ['candidate.sv','candidate.json','replay.vvp']),'COMPILED_ARTIFACT_MISSING')
    return d

def release(root,snapshots,mode,reg):
    data=[checked(root,s) for s in snapshots]
    require(len(data)==6 and {(r['arm'],r['repetition'],r['round']) for r in data}==expected(reg),'ALL_SIX_SNAPSHOTS_REQUIRED')
    ids=[{r['session_id'] for r in data if r['arm']==a} for a in ARMS]
    require(all(len(x)==1 for x in ids) and ids[0]!=ids[1],'TWO_INDEPENDENT_SESSIONS_REQUIRED')
    require(not (root/'release.json').exists(),'RELEASE_EXISTS')
    dump(root/'all-round-candidates.json',dict(mode=mode,rounds=snapshots,all6_rounds_present=True,hidden_scoring_started=False,not_new_model_evidence=mode!='live'))
    finals=[]
    for a in ARMS:
        valid=sorted((r for r in data if r['arm']==a and r['status']=='compiled'),key=lambda r:r['round']);last=valid[-1] if valid else None
        finals.append(dict(arm=a,repetition=1,status='compiled' if last else 'invalid',selected_round=last['round'] if last else None,directory=last['directory']+'/compiled' if last else None))
    dump(root/'final-candidates.json',dict(mode=mode,candidates=finals))
    names=['all-round-candidates.json','final-candidates.json','calls.jsonl','run.json']
    dump(root/'release.json',dict(mode=mode,files={n:sha(root/n) for n in names},all_rounds_frozen=True,candidate_revision_allowed=False));return finals

def verify(root,reg):
    root=Path(root);r=json.loads((root/'release.json').read_text());require(r['all_rounds_frozen'] and not r['candidate_revision_allowed'],'RELEASE_FLAGS')
    for n,h in r['files'].items():require(sha(root/n)==h,'RELEASE_FILE_DRIFT')
    data=[checked(root,s) for s in json.loads((root/'all-round-candidates.json').read_text())['rounds']]
    require(len(data)==6 and {(r['arm'],r['repetition'],r['round']) for r in data}==expected(reg),'SIX_ROUND_SET_DRIFT')
    ids=[{x['session_id'] for x in data if x['arm']==a} for a in ARMS];require(all(len(x)==1 for x in ids) and ids[0]!=ids[1],'SESSION_DRIFT')
    finals=json.loads((root/'final-candidates.json').read_text())['candidates'];require(len(finals)==2 and {x['arm'] for x in finals}==set(ARMS),'FINAL_SET')
    for f in finals:
        valid=sorted((x for x in data if x['arm']==f['arm'] and x['status']=='compiled'),key=lambda x:x['round']);last=valid[-1] if valid else None
        require(f['repetition']==1 and f['selected_round']==(last['round'] if last else None) and f['directory']==(last['directory']+'/compiled' if last else None),'FINAL_SELECTION_DRIFT')
    return data
