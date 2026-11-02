import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('workflow', Path(__file__).parents[1] / 'scripts/workflow.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bridge = module.Bridge(self.root)
        self.key = 0

    def event(self, kind, **data):
        self.key += 1
        return self.bridge.event(kind, {'key': str(self.key), 'revision': self.bridge.state()['revision'], **data})

    def request(self):
        return self.event('request.submitted', text='Build a booking tool', files=[])

    def test_request_is_durable_and_duplicate_retry_is_idempotent(self):
        data = {'key': 'request-1', 'revision': 0, 'text': 'hello', 'files': []}
        result = self.bridge.event('request.submitted', data)
        again = module.Bridge(self.root)
        self.assertEqual(result['id'], again.event('request.submitted', data)['id'])
        self.assertEqual(again.state()['route'], '/grill')
        self.assertEqual(again.wait(0)['payload']['skill'], 'grill-workflow')
        self.assertEqual(again.wait(0)['id'], result['id'])

    def test_ack_and_response_are_atomic(self):
        event = self.request()
        self.bridge.publish({'message': 'working'}, event['id'])
        self.assertEqual(self.bridge.wait(0), {'status': 'timeout'})
        revision = self.bridge.state()['revision']
        with self.assertRaises(ValueError):
            self.bridge.publish({'message': 'must roll back'}, event['id'])
        self.assertEqual(self.bridge.state()['revision'], revision)
        self.assertEqual(self.bridge.state()['message'], 'working')

    def test_questions_reject_stale_missing_and_invalid_answers(self):
        event = self.request()
        self.bridge.publish({'stage': 'grill-workflow', 'questions': [
            {'id': 'x', 'type': 'checkbox', 'label': 'Features', 'options': ['Search'], 'required': True},
            {'id': 'y', 'type': 'select', 'label': 'Platform', 'options': ['Web'], 'required': True}
        ]}, event['id'])
        question_set = self.bridge.state()['questionSet']
        for answers in ({}, {'x': ['Other'], 'y': 'Web'}, {'x': ['Search'], 'y': 'Unknown'}):
            with self.assertRaises(ValueError):
                self.event('answers.submitted', questionSet=question_set, answers=answers)
        with self.assertRaises(ValueError):
            self.event('answers.submitted', questionSet='old', answers={'x': ['Search'], 'y': 'Web'})
        self.event('answers.submitted', questionSet=question_set, answers={'x': ['Search'], 'y': 'Web'})
        self.assertEqual(self.bridge.wait(0)['payload']['answers'], {'x': ['Search'], 'y': 'Web'})

    def test_upload_is_saved_and_payload_contains_only_paths(self):
        self.event('request.submitted', text='hello', files=[{'name': 'ref.txt', 'data': 'aGVsbG8='}])
        files = self.bridge.wait(0)['payload']['files']
        self.assertTrue(files[0].startswith('docs/ref/'))
        self.assertEqual((self.root / files[0]).read_text(), 'hello')

    def test_traversal_and_symlink_escape_are_rejected(self):
        with self.assertRaises(ValueError):
            self.event('request.submitted', text='hello', files=[{'name': '../secret', 'data': 'aA=='}])
        with self.assertRaises(ValueError):
            module.inside(self.root, '../secret')
        (self.root / 'docs').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.event('request.submitted', text='hello', files=[{'name': 'ref.txt', 'data': 'aA=='}])

    def test_action_requires_offer_and_prototype_feedback_carries_page(self):
        event = self.request()
        path = self.root / 'docs/assets/prototype/index.html'
        path.parent.mkdir(parents=True)
        path.write_text('<h1>Prototype</h1>')
        self.bridge.publish({'stage': 'to-prototype', 'status': 'waiting', 'questions': [],
                             'pages': [{'id': 'UI-1', 'title': 'Home', 'path': 'docs/assets/prototype/index.html'}],
                             'actions': [{'id': 'accept', 'label': 'Accept', 'skill': 'spec-with-prototype'}]}, event['id'])
        self.assertEqual(self.bridge.state()['route'], '/prototype')
        with self.assertRaises(ValueError):
            self.event('action.requested', action='execute-shell')
        with self.assertRaises(ValueError):
            self.event('prototype.feedback', page='old-page', text='change')
        self.event('prototype.feedback', page='UI-1', text='make title larger')
        payload = self.bridge.wait(0)['payload']
        self.assertEqual(payload['skill'], 'edit-prototype')
        self.assertEqual(payload['page'], 'UI-1')

    def test_old_revision_and_second_active_request_are_rejected(self):
        self.request()
        with self.assertRaises(ValueError):
            self.bridge.event('request.submitted', {'key': 'stale', 'revision': 0, 'text': 'again'})
        with self.assertRaises(ValueError):
            self.event('request.submitted', text='again')

    def test_absolute_or_noncanonical_prototype_paths_are_rejected(self):
        path = self.root / 'docs/assets/prototype/index.html'
        path.parent.mkdir(parents=True)
        path.write_text('<h1>Home</h1>')
        for raw in [str(path), './docs/assets/prototype/index.html']:
            with self.assertRaises(ValueError):
                self.bridge.publish({'pages': [{'id': 'x', 'title': 'Home', 'path': raw}]})

    def test_completed_workflow_accepts_next_request(self):
        first = self.request()
        self.bridge.publish({'stage': 'code-review', 'status': 'complete', 'message': 'Verified'}, first['id'])
        self.event('request.submitted', text='Next feature')
        self.assertEqual(self.bridge.wait(0)['payload']['text'], 'Next feature')
        self.assertEqual(self.bridge.state()['route'], '/grill')

    def test_invalid_published_page_cannot_expose_project_files(self):
        with self.assertRaises(ValueError):
            self.bridge.publish({'pages': [{'id': 'x', 'title': 'Secrets', 'path': '.env'}]})


if __name__ == '__main__':
    unittest.main()
