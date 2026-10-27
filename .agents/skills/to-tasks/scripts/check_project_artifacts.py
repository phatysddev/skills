#!/usr/bin/env python3
"""Read-only validation of an explicit project artifact index (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re

class InvalidIndex(ValueError):
    pass

def check(root, data):
    root = Path(root).resolve()
    errors = []
    def source(name):
        p = (root / name).resolve()
        if not p.is_relative_to(root):
            raise InvalidIndex(f'path escapes project: {name}')
        try:
            return p.read_bytes()
        except OSError as exc:
            raise InvalidIndex(f'cannot read {name}: {exc}') from exc
    def unique(rows, label):
        result = {}
        for row in rows:
            key = row['id']
            if key in result:
                errors.append(f'duplicate {label}: {key}')
            result[key] = row
        return result
    if not isinstance(data, dict):
        raise InvalidIndex('index must be an object')
    if data.get('version') != 1:
        raise InvalidIndex('version must be 1')
    specs = unique(data['specs'], 'spec')
    tasks = unique(data['tasks'], 'task')
    for sid, spec in specs.items():
        content = source(spec['path'])
        if hashlib.sha256(content).hexdigest() != spec['sha256']:
            errors.append(f'{sid}: stale spec fingerprint')
        text = content.decode('utf-8')
        if not re.search(r'(?m)^(?:- )?Agreement: ' + re.escape(spec['agreement']) + r'\s*$', text):
            errors.append(f'{sid}: agreement differs from source')
        declared = set(re.findall(r'(?m)^\|\s*(AC-[\w-]+)\s*\||^(AC-[\w-]+):', text))
        declared = {a or b for a, b in declared}
        if not declared:
            errors.append(f'{sid}: no supported AC declarations; review format manually')
        if set(spec['acs']) != declared:
            errors.append(f'{sid}: AC index differs from source declarations')
        for ac in spec['acs']:
            owners = [t for t in tasks.values() if t['spec'] == sid and ac in t['acs'] and not t.get('retired', False)]
            if not owners:
                errors.append(f'{sid}/{ac}: uncovered')
    for tid, task in tasks.items():
        text = source(task['path']).decode('utf-8')
        if not re.search(r'(?m)^(?:- )?Agreement: ' + re.escape(task['agreement']) + r'\s*$', text):
            errors.append(f'{tid}: agreement differs from source')
        status = re.search(r'(?m)^- Status:\s*(\S+)', text)
        if not status or status.group(1) != task['status']:
            errors.append(f'{tid}: status differs from source')
        if task['status'] not in {'todo', 'in_progress', 'in_review', 'blocked', 'done'}:
            errors.append(f'{tid}: invalid status')
        spec = specs.get(task['spec'])
        if spec is None:
            errors.append(f'{tid}: unknown spec')
            continue
        if task['status'] != 'done' and not task.get('retired', False) and task['agreement'] != spec['agreement']:
            errors.append(f'{tid}: stale runnable agreement')
        if task.get('retired', False) and task['status'] != 'blocked':
            errors.append(f'{tid}: retired task remains runnable')
        for ac in task['acs']:
            if ac not in spec['acs']:
                errors.append(f'{tid}: unknown AC {ac}')
            if ac not in text:
                errors.append(f'{tid}: AC {ac} absent from task source')
        body = re.search(r'(?ms)^## Blocked by\s*\n(.*?)(?=^## |\Z)', text)
        deps = set(re.findall(r'TASK-\d+', body.group(1))) if body else set()
        if deps != set(task['dependencies']):
            errors.append(f'{tid}: dependency index differs from source')
        for dep in task['dependencies']:
            if dep not in tasks:
                errors.append(f'{tid}: missing dependency {dep}')
        if task['status'] == 'done' and task['agreement'] != spec['agreement']:
            # Historical delivery is retained, but cannot alone cover the new contract.
            for ac in task['acs']:
                if ac in spec['acs'] and not any(t['spec'] == task['spec'] and (t['agreement'] == spec['agreement'] or (spec['agreement'] in t.get('valid_for', []) and bool(t.get('evidence_basis')))) and ac in t['acs'] and not t.get('retired', False) for t in tasks.values()):
                    errors.append(f'{tid}/{ac}: historical evidence lacks current coverage')
    active, visited = set(), set()
    def visit(tid):
        if tid in active:
            errors.append(f'dependency cycle: {tid}')
            return
        if tid in visited or tid not in tasks:
            return
        active.add(tid)
        for dep in tasks[tid]['dependencies']:
            visit(dep)
        active.remove(tid)
        visited.add(tid)
    for tid in tasks:
        visit(tid)
    baselines = unique(data['baselines'], 'baseline')
    for sid, spec in specs.items():
        for bid in spec.get('baselines', []):
            if bid not in baselines:
                errors.append(f'{sid}: missing baseline {bid}')
    for baseline in baselines.values():
        for name, digest in baseline['files'].items():
            if hashlib.sha256(source(name)).hexdigest() != digest:
                errors.append(f"{baseline['id']}: baseline hash mismatch: {name}")
        if not baseline['files']:
            errors.append(f"{baseline['id']}: empty baseline inventory")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    try:
        errors = check(args.root, json.loads(args.index.read_text()))
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(f'INVALID: {exc}')
        return 2
    for error in errors:
        print(f'FAIL: {error}')
    if errors:
        return 1
    print('Artifact index checks passed; semantic coverage and rendered fidelity require review.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
