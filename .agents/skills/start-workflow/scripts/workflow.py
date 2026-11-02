#!/usr/bin/env python3
"""Local web/event bridge for Phat Skills v2. Python 3.10+, no dependencies."""
import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import secrets
import sqlite3
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
STAGES = {'start-workflow', 'ask-workflow', 'grill-workflow', 'grill-design', 'setup-project',
          'write-spec', 'to-tasks', 'implement-task', 'auto-implement', 'code-review',
          'change-scope', 'verify-feature', 'release-check', 'code-to-context',
          'compact-context', 'ui-design', 'debug-task', 'agent-security', 'to-prototype',
          'edit-prototype', 'spec-with-prototype', 'unit-test', 'integration-test', 'e2e-test'}
MAX_BODY = 28 * 1024 * 1024


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path escapes project boundary')
    return path


class Bridge:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.directory = inside(self.root, '.phat-workflow')
        self.directory.mkdir(exist_ok=True, mode=0o700)
        self.database = self.directory / 'events.sqlite3'
        with self.connect() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, body TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT,
              key TEXT UNIQUE NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL,
              created REAL NOT NULL, acknowledged INTEGER NOT NULL DEFAULT 0);''')
            db.execute('INSERT OR IGNORE INTO state VALUES(1,?)', (json.dumps({
                'version': 2, 'project': str(self.root), 'revision': 0, 'stage': 'start-workflow',
                'route': '/', 'status': 'idle', 'message': 'พร้อมเริ่มงาน', 'questions': [],
                'pages': [], 'history': []}),))

    def connect(self):
        db = sqlite3.connect(self.database, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def state(self):
        with self.connect() as db:
            return json.loads(db.execute('SELECT body FROM state WHERE id=1').fetchone()[0])

    def save(self, db, state):
        state['revision'] += 1
        db.execute('UPDATE state SET body=? WHERE id=1', (json.dumps(state, ensure_ascii=False),))

    def event(self, kind, data):
        if kind not in {'request.submitted', 'answers.submitted', 'action.requested', 'prototype.feedback'}:
            raise ValueError('Unknown browser event')
        key = data.get('key')
        if not isinstance(key, str) or not 1 <= len(key) <= 100:
            raise ValueError('A unique event key is required')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT id FROM events WHERE key=?', (key,)).fetchone()
            if old:
                return {'id': old[0], 'duplicate': True}
            state = json.loads(db.execute('SELECT body FROM state WHERE id=1').fetchone()[0])
            if data.get('revision') != state['revision']:
                raise ValueError('หน้านี้มีข้อมูลใหม่แล้ว กรุณาลองอีกครั้ง')
            payload = dict(data)
            if kind == 'request.submitted':
                if state['status'] not in {'idle', 'complete'}:
                    raise ValueError('มี workflow ที่กำลังทำงานอยู่')
                text = data.get('text', '').strip()
                if not text:
                    raise ValueError('กรุณาระบุสิ่งที่ต้องการทำ')
                files = data.get('files', [])
                if not isinstance(files, list) or len(files) > 10:
                    raise ValueError('Maximum 10 reference files')
                decoded = []
                for item in files:
                    name = item.get('name', '')
                    if not name or '/' in name or '\\' in name or name in {'.', '..'}:
                        raise ValueError('Invalid reference filename')
                    content = base64.b64decode(item['data'], validate=True)
                    decoded.append((name, content))
                if sum(len(content) for _, content in decoded) > 20 * 1024 * 1024:
                    raise ValueError('Maximum total upload size is 20 MB')
                refs = []
                for name, content in decoded:
                    relative = 'docs/ref/' + uuid.uuid4().hex + '-' + name
                    path = inside(self.root, relative)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with path.open('xb') as stream:
                        stream.write(content)
                    refs.append(relative)
                payload = {'text': text, 'files': refs, 'skill': 'grill-workflow'}
                state.update(stage='grill-workflow', route='/grill', status='working',
                             message='รอ agent อ่านคำขอและจัดคำถาม', questions=[], pages=[], actions=[])
            elif kind == 'answers.submitted':
                if state['status'] != 'waiting' or data.get('questionSet') != state.get('questionSet'):
                    raise ValueError('This question set is no longer waiting for answers')
                answers = data.get('answers')
                if not isinstance(answers, dict):
                    raise ValueError('Answers must be an object')
                for q in state['questions']:
                    value = answers.get(q['id'])
                    if q.get('required') and (value is None or value == '' or value == []):
                        raise ValueError('กรุณาตอบ: ' + q['label'])
                    if value is None:
                        continue
                    if q['type'] == 'checkbox':
                        if not isinstance(value, list) or any(v not in q['options'] for v in value):
                            raise ValueError('Invalid checkbox answer')
                    elif not isinstance(value, str) or (q['type'] == 'select' and value not in q['options'] and value != ''):
                        raise ValueError('Invalid answer')
                payload = {'questionSet': state['questionSet'], 'answers': answers, 'skill': state['stage']}
                state.update(status='working', questions=[], message='ส่งคำตอบแล้ว รอ agent ดำเนินงานต่อ')
            else:
                if state['status'] == 'working':
                    raise ValueError('รอ agent ทำงานรอบปัจจุบันก่อน')
                if kind == 'action.requested':
                    action = next((a for a in state.get('actions', []) if a['id'] == data.get('action')), None)
                    if not action:
                        raise ValueError('Action is no longer available')
                    payload = {'action': action['id'], 'skill': action['skill']}
                    state['stage'] = action['skill']
                else:
                    if state['route'] != '/prototype' or not data.get('text', '').strip():
                        raise ValueError('Prototype feedback requires a message in the prototype workspace')
                    if data.get('page') not in [p['id'] for p in state['pages']]:
                        raise ValueError('Select a current prototype page')
                    payload = {'text': data['text'].strip(), 'page': data['page'], 'skill': 'edit-prototype'}
                    state['stage'] = 'edit-prototype'
                state.update(status='working', actions=[], questions=[], message='ส่งคำขอให้ agent แล้ว')
            row = db.execute('INSERT INTO events(key,kind,payload,created) VALUES(?,?,?,?)',
                             (key, kind, json.dumps(payload, ensure_ascii=False), time.time()))
            state['history'] = (state['history'] + [{'kind': kind, 'text': payload.get('text', kind)}])[-100:]
            self.save(db, state)
            return {'id': row.lastrowid}

    def publish(self, update, event_id=None):
        allowed = {'stage', 'status', 'message', 'questions', 'questionSet', 'pages', 'actions'}
        if set(update) - allowed:
            raise ValueError('Unknown state fields')
        if update.get('stage', 'start-workflow') not in STAGES:
            raise ValueError('Unknown skill')
        if update.get('status', 'waiting') not in {'working', 'waiting', 'complete', 'blocked', 'idle'}:
            raise ValueError('Unknown status')
        questions = update.get('questions', [])
        ids = set()
        for q in questions:
            if not isinstance(q.get('id'), str) or q['id'] in ids or not q.get('label') or q.get('type') not in {'checkbox', 'select', 'input', 'textarea'}:
                raise ValueError('Invalid or duplicate question')
            ids.add(q['id'])
            if q['type'] in {'checkbox', 'select'} and (not isinstance(q.get('options'), list) or not q['options'] or not all(isinstance(x, str) for x in q['options'])):
                raise ValueError('Choice questions need string options')
        for a in update.get('actions', []):
            if not a.get('id') or not a.get('label') or a.get('skill') not in STAGES:
                raise ValueError('Invalid next action')
        ids = set()
        for page in update.get('pages', []):
            path = inside(self.root, page['path'])
            prototype_root = inside(self.root, 'docs/assets/prototype')
            if Path(page['path']).is_absolute() or page['path'] != path.relative_to(self.root).as_posix() or not path.is_relative_to(prototype_root) or not path.is_file() or path.suffix.lower() != '.html':
                raise ValueError('Prototype pages must be existing HTML under docs/assets/prototype')
            if not page.get('id') or page['id'] in ids or not page.get('title'):
                raise ValueError('Prototype pages require unique IDs and titles')
            ids.add(page['id'])
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            state = json.loads(db.execute('SELECT body FROM state WHERE id=1').fetchone()[0])
            state.update(update)
            if questions:
                state['questionSet'] = uuid.uuid4().hex
                state['status'] = 'waiting'
            if state['stage'] in {'to-prototype', 'edit-prototype', 'spec-with-prototype'}:
                state['route'] = '/prototype'
            elif state['stage'] in {'grill-workflow', 'grill-design'}:
                state['route'] = '/grill'
            else:
                state['route'] = '/workflow'
            state['history'] = (state['history'] + [{'kind': 'agent.updated', 'text': state['message']}])[-100:]
            if event_id is not None:
                if not db.execute('SELECT id FROM events WHERE id=? AND acknowledged=0', (event_id,)).fetchone():
                    raise ValueError('Event missing or already acknowledged')
                db.execute('UPDATE events SET acknowledged=1 WHERE id=?', (event_id,))
            db.execute('INSERT INTO events(key,kind,payload,created,acknowledged) VALUES(?,?,?,?,1)',
                       (uuid.uuid4().hex, 'agent.updated', json.dumps(update, ensure_ascii=False), time.time()))
            self.save(db, state)
        return state

    def wait(self, timeout):
        deadline = time.monotonic() + timeout
        while True:
            with self.connect() as db:
                event = db.execute('SELECT * FROM events WHERE acknowledged=0 ORDER BY id LIMIT 1').fetchone()
            if event:
                return dict(event) | {'payload': json.loads(event['payload'])}
            if time.monotonic() >= deadline:
                return {'status': 'timeout'}
            time.sleep(.25)


def serve(bridge, port):
    token = secrets.token_urlsafe(32)
    hosts = {f'localhost:{port}', f'127.0.0.1:{port}'}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, status, content, mime='application/json; charset=utf-8', prototype=False):
            if not isinstance(content, bytes):
                content = json.dumps(content, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy',
                             "sandbox allow-scripts; default-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'" if prototype else
                             "default-src 'self'; script-src 'self'; style-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'")
            self.end_headers()
            self.wfile.write(content)

        def valid_host(self):
            if self.headers.get('Host') not in hosts:
                self.send(403, {'error': 'Loopback host required'})
                return False
            return True

        def do_GET(self):
            if not self.valid_host():
                return
            path = unquote(urlsplit(self.path).path)
            if path == '/api/state':
                return self.send(200, bridge.state() | {'sessionToken': token})
            if path in {'/', '/grill', '/prototype', '/workflow'}:
                html = (ASSETS / 'index.html').read_text().replace('__TOKEN__', token)
                return self.send(200, html.encode(), 'text/html; charset=utf-8')
            if path in {'/app.js', '/style.css'}:
                file = ASSETS / path[1:]
                return self.send(200, file.read_bytes(), 'text/javascript; charset=utf-8' if path.endswith('.js') else 'text/css; charset=utf-8')
            if path.startswith('/preview/'):
                try:
                    file = inside(inside(bridge.root, 'docs/assets/prototype'), path[len('/preview/'):])
                    if file.suffix.lower() not in {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.woff', '.woff2'}:
                        raise ValueError('Unsupported preview asset')
                    return self.send(200, file.read_bytes(), mimetypes.guess_type(str(file))[0] or 'application/octet-stream', prototype=True)
                except (ValueError, OSError):
                    pass
            self.send(404, {'error': 'Not found'})

        def do_POST(self):
            if not self.valid_host():
                return
            if self.headers.get('X-Workflow-Token') != token or self.headers.get('Origin') not in {'http://' + h for h in hosts}:
                return self.send(403, {'error': 'Invalid local session'})
            if self.path != '/api/events':
                return self.send(404, {'error': 'Not found'})
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if size <= 0 or size > MAX_BODY:
                    return self.send(413, {'error': 'Request exceeds upload limit'})
                data = json.loads(self.rfile.read(size))
                self.send(200, bridge.event(data['kind'], data))
            except (ValueError, KeyError, TypeError, AttributeError) as error:
                self.send(400, {'error': str(error)})
            except OSError:
                self.send(500, {'error': 'Cannot persist workflow data'})

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(json.dumps({'url': f'http://localhost:{port}', 'project': str(bridge.root)}), flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    start = sub.add_parser('serve')
    start.add_argument('--port', type=int, default=9909)
    wait = sub.add_parser('wait')
    wait.add_argument('--timeout', type=float, default=25)
    sub.add_parser('state')
    publish = sub.add_parser('publish')
    publish.add_argument('--file', required=True, type=Path)
    publish.add_argument('--event', type=int)
    args = parser.parse_args()
    bridge = Bridge(args.project)
    try:
        if args.command == 'serve':
            serve(bridge, args.port)
        elif args.command == 'wait':
            print(json.dumps(bridge.wait(min(max(args.timeout, 0), 50)), ensure_ascii=False))
        elif args.command == 'state':
            print(json.dumps(bridge.state(), ensure_ascii=False))
        else:
            print(json.dumps(bridge.publish(json.loads(args.file.read_text()), args.event), ensure_ascii=False))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
