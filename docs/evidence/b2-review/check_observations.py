"""Validate saved browser observations; does not create or replace a visual review."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / 'workflow-regression-fixture'
rows = json.loads((HERE / 'render-observations.json').read_text())
assert len(rows) == 16
pairs = []
for mode, size in [('desktop', {'width': 1280, 'height': 900}), ('mobile', {'width': 390, 'height': 844})]:
    for page in range(1, 5):
        pair = [r for r in rows if r['page'] == page and r['mode'] == mode]
        assert len(pair) == 2 and {r['surface'] for r in pair} == {'app', 'baseline'}
        baseline = next(r for r in pair if r['surface'] == 'baseline')
        app = next(r for r in pair if r['surface'] == 'app')
        assert baseline['metrics'] == app['metrics'], (mode, page, 'rendered metric mismatch')
        m = app['metrics']
        assert m['viewport'] == size and not m['overflow']
        assert m['colors'] == {'text': 'rgb(41, 38, 74)', 'summary': 'rgb(226, 222, 242)'}
        assert m['heading'] == ['Home', 'Booking', 'Account', 'Help'][page-1]
        assert len(m['links']) == 4
        assert (m['aside']['x'] > m['section']['x']) if mode == 'desktop' else (m['aside']['y'] >= m['section']['y'] + m['section']['height'])
        hashes = {r['surface']: hashlib.sha256((HERE / r['file']).read_bytes()).hexdigest() for r in pair}
        pairs.append({'mode': mode, 'page': page, 'rendered_metrics_equal': True, 'capture_sha256': hashes, 'capture_bytes_equal': hashes['app'] == hashes['baseline']})
nav = json.loads((HERE / 'navigation-observations.json').read_text())
assert len(nav) == 32
assert {(r['mode'], r['source'], r['target']) for r in nav} == {(m, s, t) for m in ['desktop', 'mobile'] for s in range(1, 5) for t in range(1, 5)}
assert all(r['passed'] for r in nav)
for name, digest in json.loads((HERE / 'preserved-input-hashes.json').read_text()).items():
    assert hashlib.sha256((FIXTURE / name).read_bytes()).hexdigest() == digest, ('historical input changed', name)
print(json.dumps({'pairs': pairs, 'navigation_checks': 32, 'historical_inputs_preserved': True}, indent=2))
