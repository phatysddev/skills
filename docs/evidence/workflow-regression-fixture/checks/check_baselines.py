from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[1]/'docs/assets/prototype-baselines/pages'
for baseline in ['b1','b2']:
 d=r/baseline
 for name,digest in json.loads((d/'inventory.json').read_text()).items():
  assert hashlib.sha256((d/name).read_bytes()).hexdigest()==digest
print('baseline inventory: b1 and b2 passed')
