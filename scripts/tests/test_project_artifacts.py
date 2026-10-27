import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[2] / '.agents/skills/to-tasks/scripts/check_project_artifacts.py'
spec = importlib.util.spec_from_file_location('artifacts', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = 'Agreement: v2\n| AC-01 | Navigation |\n| AC-02 | Layout |\n'
        (self.root / 'spec.md').write_text(self.source)
        (self.root / 'task.md').write_text('- Status: todo\n- Agreement: v2\n## Blocked by\nNone.\n## Todo\n- [ ] AC-01 AC-02\n')
        (self.root / 'style.css').write_text('body { color: blue; }')
        self.data = {'version': 1, 'specs': [{'id': 'SPEC-001', 'path': 'spec.md', 'agreement': 'v2', 'sha256': hashlib.sha256(self.source.encode()).hexdigest(), 'acs': ['AC-01', 'AC-02']}], 'tasks': [{'id': 'TASK-001', 'path': 'task.md', 'spec': 'SPEC-001', 'status': 'todo', 'agreement': 'v2', 'acs': ['AC-01', 'AC-02'], 'dependencies': []}], 'baselines': [{'id': 'v2', 'files': {'style.css': hashlib.sha256((self.root / 'style.css').read_bytes()).hexdigest()}}]}
    def errors(self):
        return module.check(self.root, self.data)
    def test_valid(self):
        self.assertEqual([], self.errors())
    def test_missing_coverage(self):
        self.data['tasks'][0]['acs'].remove('AC-02')
        self.assertTrue(any('uncovered' in e for e in self.errors()))
    def test_cycle(self):
        self.data['tasks'][0]['dependencies'] = ['TASK-001']
        (self.root / 'task.md').write_text('- Status: todo\n- Agreement: v2\n## Blocked by\nTASK-001\n## Todo\nAC-01 AC-02\n')
        self.assertTrue(any('cycle' in e for e in self.errors()))
    def test_stale_agreement(self):
        self.data['tasks'][0]['agreement'] = 'v1'
        self.assertTrue(any('stale runnable' in e for e in self.errors()))
    def test_shared_css_hash(self):
        (self.root / 'style.css').write_text('body { color: red; }')
        self.assertTrue(any('hash mismatch' in e for e in self.errors()))
    def test_stale_spec_index(self):
        (self.root / 'spec.md').write_text(self.source + '| AC-03 | New |\n')
        self.assertTrue(any('fingerprint' in e for e in self.errors()))
        self.assertTrue(any('AC index' in e for e in self.errors()))
    def test_status_mismatch(self):
        self.data['tasks'][0]['status'] = 'done'
        self.assertTrue(any('status differs' in e for e in self.errors()))
    def test_dependency_mismatch(self):
        self.data['tasks'][0]['dependencies'] = ['TASK-999']
        self.assertTrue(any('missing dependency' in e for e in self.errors()))
        self.assertTrue(any('dependency index' in e for e in self.errors()))
    def test_historical_delivery_needs_delta(self):
        self.data['tasks'][0].update(status='done', agreement='v1')
        (self.root / 'task.md').write_text('- Status: done\n- Agreement: v1\n## Blocked by\nNone.\n## Todo\nAC-01 AC-02\n')
        self.assertTrue(any('historical evidence' in e for e in self.errors()))
    def test_unchanged_historical_evidence_can_carry_forward(self):
        self.data['tasks'][0].update(status='done', agreement='v1', valid_for=['v2'], evidence_basis='change record: criteria unchanged')
        (self.root / 'task.md').write_text('- Status: done\n- Agreement: v1\n## Blocked by\nNone.\n## Todo\nAC-01 AC-02\n')
        self.assertEqual([], self.errors())
    def test_repeat_does_not_write(self):
        before = {p.name:p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(self.errors(), self.errors())
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.root.iterdir()})
    def test_path_escape(self):
        self.data['tasks'][0]['path'] = '../outside.md'
        with self.assertRaises(module.InvalidIndex): self.errors()
    def test_missing_baseline(self):
        self.data["specs"][0]["baselines"] = ["missing"]
        self.assertTrue(any("missing baseline" in e for e in self.errors()))
    def test_source_agreement_mismatch(self):
        self.data["tasks"][0]["agreement"] = "v9"
        self.assertTrue(any("agreement differs" in e for e in self.errors()))
    def test_duplicate_task(self):
        self.data['tasks'].append(copy.deepcopy(self.data['tasks'][0]))
        self.assertTrue(any('duplicate task' in e for e in self.errors()))

if __name__ == '__main__': unittest.main()
