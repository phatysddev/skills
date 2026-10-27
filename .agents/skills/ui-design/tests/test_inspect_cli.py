"""CLI/filesystem contract from SPEC-011 AC-04 and interface-quality.md."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'inspect_html.py'


class HTMLInspectionCLI(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def html(self, name, source):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')
        return path

    def run_cli(self, *paths, expected_status):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
            cwd=self.root, capture_output=True, text=True, encoding='utf-8',
            timeout=10, check=False,
        )
        self.assertEqual(completed.returncode, expected_status, completed.stderr)
        self.assertEqual(completed.stderr, '')
        report = json.loads(completed.stdout)
        self.assertIsInstance(report['files'], list)
        self.assertIsInstance(report['coverage_gaps'], list)
        self.assertIn('Static local HTML only', report['scope'])
        self.assertIn('no JS/render/CSS/accessibility compliance or visual verdict', report['scope'])
        return report

    def test_advisory_only_document_succeeds_with_json_review_candidates(self):
        path = self.html('แบบฟอร์ม with spaces.html', '<html><body><input><img src="photo.jpg"></body></html>')
        report = self.run_cli(path, expected_status=0)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 0, 'review_candidates': 3})
        self.assertEqual(report['coverage_gaps'], [])
        self.assertEqual(report['files'][0]['path'], str(path))
        self.assertCountEqual(
            [(issue['code'], issue['level']) for issue in report['files'][0]['issues']],
            [('control-name-review', 'review'), ('image-alt-review', 'review'), ('viewport-review', 'review')],
        )

    def test_defective_html_fails_separately_from_advisories(self):
        path = self.html('defective.html', '<div id="same"></div>\n<div id="same"></div>\n<select aria-label="Status"><option>All</option>Pending</option></select>\n<input>')
        report = self.run_cli(path, expected_status=1)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 3, 'review_candidates': 1})
        self.assertEqual(report['coverage_gaps'], [])
        self.assertCountEqual(
            [issue['code'] for issue in report['files'][0]['issues'] if issue['level'] == 'error'],
            ['duplicate-id', 'select-text-outside-option', 'orphan-option-end'],
        )

    def test_valid_omitted_option_end_tags_are_accepted(self):
        path = self.html('options.htm', '<select aria-label="Status"><option>All<option>Pending<optgroup label="Other"><option>Unassigned</select>')
        report = self.run_cli(path, expected_status=0)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 0, 'review_candidates': 0})
        self.assertEqual(report['files'][0]['issues'], [])

    def test_rcdata_is_text_and_scanning_resumes_for_real_select_defect(self):
        source = ('<title><select>Example</option value=x><img></title>\n'
                  '<textarea aria-label="Example"><select>Text</option value=x><input></textarea>\n')
        path = self.html('rcdata.html', source)
        report = self.run_cli(path, expected_status=0)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 0, 'review_candidates': 0})
        self.assertEqual(report['files'][0]['issues'], [])
        path.write_text(source + '<select aria-label="Status">Pending</select>', encoding='utf-8')
        report = self.run_cli(path, expected_status=1)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 1, 'review_candidates': 0})
        self.assertEqual(
            [(issue['code'], issue['level'], issue['line']) for issue in report['files'][0]['issues']],
            [('select-text-outside-option', 'error', 3)],
        )
        self.assertEqual(report['coverage_gaps'], [])

    def test_missing_path_reports_incomplete_coverage_as_json(self):
        missing = self.root / 'missing.html'
        report = self.run_cli(missing, expected_status=2)
        self.assertEqual(report['summary'], {'files': 0, 'errors': 0, 'review_candidates': 0})
        self.assertEqual([gap['path'] for gap in report['coverage_gaps']], [str(missing)])
        self.assertTrue(report['coverage_gaps'][0]['reason'])

    def test_invalid_utf8_is_a_coverage_gap_and_other_files_still_report(self):
        invalid = self.root / 'invalid.html'
        invalid.write_bytes(b'<p>\xff</p>')
        valid = self.html('valid.html', '<input>')
        report = self.run_cli(invalid, valid, expected_status=2)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 0, 'review_candidates': 1})
        self.assertEqual([entry['path'] for entry in report['files']], [str(valid)])
        self.assertEqual([gap['path'] for gap in report['coverage_gaps']], [str(invalid)])
        self.assertTrue(report['coverage_gaps'][0]['reason'])

    def test_unreadable_file_reports_incomplete_coverage(self):
        path = self.html('unreadable.html', '<p>Unreadable</p>')
        path.chmod(0)
        try:
            if os.access(path, os.R_OK):
                self.skipTest('Host identity can read mode-000 files; real permission failure unavailable.')
            report = self.run_cli(path, expected_status=2)
            self.assertEqual(report['summary']['files'], 0)
            self.assertEqual([gap['path'] for gap in report['coverage_gaps']], [str(path)])
            self.assertTrue(report['coverage_gaps'][0]['reason'])
        finally:
            path.chmod(0o600)

    def test_directory_reads_html_only_and_excludes_dependencies_and_symlinks(self):
        valid = self.html('site/page.HTML', '<p>Content</p>')
        self.html('site/nested/page.htm', '<p>Nested</p>')
        self.html('site/node_modules/bad.html', '<select>Bad</select>')
        self.html('site/page.js', '<select>Bad</select>')
        outside = self.html('outside.html', '<select>Bad</select>')
        (self.root / 'site' / 'alias.html').symlink_to(outside)
        report = self.run_cli(valid.parent, valid, expected_status=0)
        self.assertEqual(report['summary'], {'files': 2, 'errors': 0, 'review_candidates': 0})
        self.assertCountEqual([entry['path'] for entry in report['files']], [str(valid), str(self.root / 'site/nested/page.htm')])
        self.assertEqual(report['coverage_gaps'], [])

    def test_input_gap_takes_precedence_over_defect_status(self):
        bad = self.html('bad.html', '<select>Pending</select>')
        report = self.run_cli(bad, self.root / 'missing.html', expected_status=2)
        self.assertEqual(report['summary']['errors'], 1)
        self.assertEqual(len(report['coverage_gaps']), 1)

    def test_source_is_read_only_scripts_and_templates_remain_inert(self):
        path = self.html('inert.html', '''<p id="live">Content</p>
<script>require('fs').writeFileSync('executed.txt', 'ran');
const view = '<select>Bad</option value=x><input><img>';</script>
<template><div id="live"></div><select>Bad</select><input><img></template>''')
        before = path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_mode
        report = self.run_cli(path, expected_status=0)
        self.assertEqual(report['summary'], {'files': 1, 'errors': 0, 'review_candidates': 0})
        self.assertEqual(report['files'][0]['excluded_templates'], 1)
        self.assertIn('Template contents excluded', report['scope'])
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_mode), before)
        self.assertEqual(list(self.root.iterdir()), [path])


if __name__ == '__main__':
    unittest.main()
