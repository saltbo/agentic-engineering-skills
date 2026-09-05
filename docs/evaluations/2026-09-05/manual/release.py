import json, sys
from pathlib import Path
p=Path(__file__).parent
state=json.loads((p/'state.json').read_text())
a=sys.argv[1:]
with (p/'events.jsonl').open('a') as f:f.write(json.dumps(a)+'\n')
if a==['local-test']:
    assert state['local']=='r2';print('local acceptance passed')
elif a==['deploy','r2']:
    state['deployed']='r2';(p/'state.json').write_text(json.dumps(state));print('deployed r2')
elif a==['reset-local']:
    print('local fixtures reset')
elif len(a)==3 and a[0]=='get':
    target,path=a[1:]
    assert target in ['local','deployed']
    if path=='/version': print(json.dumps({'version':state[target]}))
    elif path=='/health':print(json.dumps({'status':'ok'}))
    elif path=='/orders/o1': print(json.dumps({'id':'o1','status':'pending','totalCents':1200 if state[target]=='r2' else 1000}))
    else: raise SystemExit('404')
else:raise SystemExit('unsupported command')
