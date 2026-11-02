"""Real loopback HTTP contract checks; require local socket permission."""
import http.client
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import unittest


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            cls.port = sock.getsockname()[1]
        script = Path(__file__).parents[1] / 'scripts/workflow.py'
        cls.process = subprocess.Popen([sys.executable, str(script), '--project', str(cls.root), 'serve', '--port', str(cls.port)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        cls.addClassCleanup(cls.stop)
        for _ in range(80):
            try:
                status, _, body = cls.request('GET', '/')
                if status == 200:
                    cls.token = re.search(b'name="workflow-token" content="([^"]+)"', body)[1].decode()
                    return
            except OSError:
                time.sleep(.05)
        raise RuntimeError('Server failed to start')

    @classmethod
    def stop(cls):
        cls.process.terminate()
        cls.process.wait(timeout=5)
        cls.process.stderr.close()

    @classmethod
    def request(cls, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', cls.port, timeout=5)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        result = (response.status, dict(response.getheaders()), response.read())
        connection.close()
        return result

    def test_state_refresh_exposes_current_same_origin_session_token(self):
        status, _, body = self.request('GET', '/api/state')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['sessionToken'], self.token)

    def test_shell_routes_and_assets(self):
        for path in ['/', '/grill', '/prototype', '/workflow', '/app.js', '/style.css']:
            status, headers, body = self.request('GET', path)
            self.assertEqual(status, 200, path)
            self.assertIn('Content-Security-Policy', headers)
            self.assertTrue(body)

    def test_foreign_host_and_unauthenticated_mutations_rejected(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'evil.invalid'})[0], 403)
        for origin, token in [('http://evil.invalid', self.token), (f'http://localhost:{self.port}', 'wrong')]:
            status, _, _ = self.request('POST', '/api/events', '{}', {'Origin': origin, 'X-Workflow-Token': token})
            self.assertEqual(status, 403)

    def test_valid_event_and_preview_confinement(self):
        payload = json.dumps({'kind': 'request.submitted', 'key': 'test', 'revision': 0, 'text': 'test', 'files': []})
        headers = {'Origin': f'http://localhost:{self.port}', 'X-Workflow-Token': self.token}
        self.assertEqual(self.request('POST', '/api/events', payload, headers)[0], 200)
        self.assertEqual(self.request('POST', '/api/events', payload, headers)[0], 200)
        self.assertEqual(json.loads(self.request('GET', '/api/state')[2])['route'], '/grill')
        directory = self.root / 'docs/assets/prototype'
        directory.mkdir(parents=True)
        (directory / 'index.html').write_text('<h1>test</h1>')
        status, response_headers, _ = self.request('GET', '/preview/index.html')
        self.assertEqual(status, 200)
        self.assertIn('sandbox allow-scripts;', response_headers['Content-Security-Policy'])
        for path in ['/preview/../../../../etc/passwd', '/preview/%2e%2e/%2e%2e/secret.html', '/preview/.env', '/.phat-workflow/events.sqlite3']:
            self.assertEqual(self.request('GET', path)[0], 404)
        self.assertEqual(self.request('POST', '/api/events', '{', headers)[0], 400)


if __name__ == '__main__':
    unittest.main()
