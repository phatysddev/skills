import importlib.util
from pathlib import Path
import tempfile
import unittest

p = Path(__file__).resolve().parents[1] / 'scripts' / 'inspect_html.py'
spec = importlib.util.spec_from_file_location('inspect_html', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class HTMLInspection(unittest.TestCase):
    def errors(self, source):
        return [i['code'] for i in m.inspect(source)['issues'] if i['level'] == 'error']

    def test_missing_option_cannot_silently_drop_pending_status(self):
        self.assertIn('select-text-outside-option', self.errors('<select><option>All</option>Pending</option></select>'))

    def test_attributes_on_closing_tag(self):
        self.assertIn('closing-tag-attributes', self.errors('<select><option>All</option value="unassigned">Unassigned</option></select>'))

    def test_omitted_option_ends_are_valid(self):
        self.assertEqual(self.errors('<select><option>A<option>B<optgroup label="More"><option>C</optgroup></select>'), [])

    def test_optional_option_and_optgroup_ends_at_each_valid_boundary(self):
        sources = [
            '<select aria-label="Status"><option>All</select>',
            '<select aria-label="Status"><option>All<option>Pending</select>',
            '<select aria-label="Status"><optgroup label="One"><option>A</optgroup></select>',
            '<select aria-label="Status"><optgroup label="One"><option>A<optgroup label="Two"><option>B</select>',
        ]
        for source in sources:
            with self.subTest(source=source):
                self.assertEqual(m.inspect(source)['issues'], [])

    def test_definite_defects_and_source_observations_have_distinct_levels(self):
        result = m.inspect('<div id="same"></div>\n<div id="same"></div>\n<input>\n<img src="photo.jpg">')
        self.assertCountEqual(
            [(issue['code'], issue['level']) for issue in result['issues']],
            [('duplicate-id', 'error'), ('control-name-review', 'review'),
             ('image-alt-review', 'review')],
        )
        duplicate = next(issue for issue in result['issues'] if issue['code'] == 'duplicate-id')
        self.assertEqual(duplicate['line'], 2)

    def test_named_controls_are_not_reported(self):
        result = m.inspect('<label for="s">Status</label><select id="s"><option>All</option></select><label>Name<input></label><span id="n">Other</span><textarea aria-labelledby="n"></textarea><input type="hidden"><input type="submit">')
        self.assertEqual(result['issues'], [])

    def test_dynamic_labels_are_only_review_candidates(self):
        result = m.inspect('<input placeholder="Name"><textarea aria-labelledby="dynamic"></textarea>')
        self.assertEqual(len(result['issues']), 2)
        self.assertTrue(all(i['level'] == 'review' for i in result['issues']))

    def test_duplicate_id_and_inert_template_coverage(self):
        self.assertIn('duplicate-id', self.errors('<div id="x"></div><div id="x"></div>'))
        result = m.inspect('<div id="x"></div><template><div id="x"></div><input></template>')
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['excluded_templates'], 1)

    def test_script_strings_are_not_parsed_as_markup(self):
        self.assertEqual(self.errors('<script>const s="<select>bad</option value=x>";</script>'), [])

    def test_script_strings_cannot_create_labels_ids_or_review_candidates(self):
        result = m.inspect('<script>const view = `<label for="name">Name</label><div id="name"></div><input><img>`;</script><input id="name">')
        self.assertEqual(
            [(issue['code'], issue['level']) for issue in result['issues']],
            [('control-name-review', 'review')],
        )

    def test_textarea_closing_option_text_is_not_a_structural_defect(self):
        result = m.inspect('<textarea aria-label="HTML example">Choose </option value="pending"> literally</textarea>')
        self.assertEqual(result['issues'], [])

    def test_textarea_apparent_inner_id_does_not_collide_with_live_id(self):
        result = m.inspect('<textarea aria-label="HTML example"><div id="example">Sample</div></textarea><div id="example">Actual content</div>')
        self.assertEqual(result['issues'], [])

    def test_title_apparent_tags_remain_text(self):
        result = m.inspect('<title><div id="example"></div><input><img></option value="pending"></title><div id="example">Actual content</div>')
        self.assertEqual(result['issues'], [])

    def test_real_errors_after_rcdata_are_detected_despite_script_like_text(self):
        for element in ('textarea', 'title'):
            opening = '<textarea aria-label="HTML example">' if element == 'textarea' else '<title>'
            source = (
                opening + '<script>const sample = "<div id=example>";'
                + '</' + element + '>\n'
                + '<div id="example"></div><div id="example"></div></option>'
            )
            with self.subTest(element=element):
                result = m.inspect(source)
                self.assertCountEqual(
                    [(issue['code'], issue['level'], issue['line']) for issue in result['issues']],
                    [('duplicate-id', 'error', 2), ('orphan-option-end', 'error', 2)],
                )

    def test_nested_templates_are_inert_and_scanning_resumes_after_them(self):
        result = m.inspect('<div id="live"></div><template><template><input><img></template><div id="live"></div><select>bad</option></select></template>\n<div id="live"></div>')
        self.assertEqual(result['excluded_templates'], 2)
        self.assertEqual(
            [(issue['code'], issue['level'], issue['line']) for issue in result['issues']],
            [('duplicate-id', 'error', 2)],
        )

    def test_valueless_attributes_do_not_crash(self):
        self.assertEqual(self.errors('<meta name><input type aria-label title><textarea aria-labelledby></textarea>'), [])

    def test_fragment_and_document_viewport(self):
        self.assertEqual(m.inspect('<div>Fragment</div>')['issues'], [])
        self.assertIn('viewport-review', [i['code'] for i in m.inspect('<html><body>Hello</body></html>')['issues']])

    def test_directory_excludes_dependencies_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'page.html').write_text('<input>', encoding='utf-8')
            (root / 'node_modules').mkdir()
            (root / 'node_modules' / 'bad.html').write_text('<select>bad</select>', encoding='utf-8')
            result, code = m.run([root])
            self.assertEqual(code, 0)
            self.assertEqual(result['summary']['files'], 1)
            self.assertEqual(result['summary']['review_candidates'], 1)
            (root / 'page.html').write_text('<select>bad</select>', encoding='utf-8')
            self.assertEqual(m.run([root])[1], 1)
            self.assertEqual(m.run([root / 'missing.html'])[1], 2)
            (root / 'alias.html').symlink_to(root / 'page.html')
            self.assertEqual(m.run([root / 'alias.html'])[1], 2)


if __name__ == '__main__':
    unittest.main()
