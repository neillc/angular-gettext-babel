import unittest

from babel._compat import StringIO

from angular_gettext_babel.extract import extract_angular

default_keys = []


class ExtractAngularTestCase(unittest.TestCase):

    def test_extract_no_tags(self):
        buf = StringIO('<html></html>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([], messages)

    def test_simple_string(self):
        buf = StringIO(
            """<html><translate>hello world!</translate>'
            <div translate>hello world!</div></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world!', []),
                (2, u'gettext', 'hello world!', [])
            ],
            messages)

    def test_interpolation(self):
        buf = StringIO(
            """<html>
            <translate>hello {$name$}!</translate>
            <div translate>hello {$name$}!</div>
            </html>
            """
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (2, u'gettext', 'hello %(name)!', []),
                (3, u'gettext', 'hello %(name)!', [])
            ], messages)

    def test_interpolation_func_call(self):
        buf = StringIO(
            """<html><div translate>hello {$func(name)$}!</div>
            '<translate>hello {$func(name)$}!</translate>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello %(func(name))!', []),
                (2, u'gettext', 'hello %(func(name))!', [])
            ],
            messages)

    def test_interpolation_list(self):
        buf = StringIO(
            """<html><div translate>hello {$name[1]$}!</div>
            <translate>hello {$name[1]$}!</translate></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello %(name[1])!', []),
                (2, 'gettext', 'hello %(name[1])!', [])
            ],
            messages)

    def test_interpolation_dict(self):
        buf = StringIO(
            """<html><div translate>hello {$name['key']$}!</div>
            <translate>hello {$name['key']$}!</translate></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', r"hello %(name['key'])!", []),
                (2, 'gettext', r"hello %(name['key'])!", [])
            ],
            messages)

    def test_interpolation_dict_double_quote(self):
        buf = StringIO(
            """<html><div translate>hello {$name["key"]$}!</div>
            <translate>hello {$name["key"]$}!</translate></html>""")

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', r'hello %(name["key"])!', []),
                (2, 'gettext', r'hello %(name["key"])!', [])
            ],
            messages)

    def test_interpolation_object(self):
        buf = StringIO(
            """<html><div translate>hello {$name.attr$}!</div>
            <translate>hello {$name.attr$}!</translate></html>""")

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello %(name.attr)!', []),
                (2, 'gettext', 'hello %(name.attr)!', [])
            ],
            messages)

    def test_interpolation_spaces(self):
        """Spaces are not valid in interpolation expressions, but we don't
        currently complain about them
        """
        buf = StringIO("""<html><div translate>hello {$name attr$}!</div>
        <translate>hello {$name attr$}!</translate></html>""")

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello {$name attr$}!', []),
                (2, 'gettext', 'hello {$name attr$}!', [])
            ],
            messages)

    def test_attr_value(self):
        """We should not translate tags that have translate as the value of an
        attribute.
        """
        buf = StringIO('<html><div id="translate">hello world!</div>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([], messages)

    def test_attr_value_plus_directive(self):
        """Unless they also have a translate directive.
        """
        buf = StringIO(
            '<html><div id="translate" translate>hello world!</div>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_translate_tag(self):
        buf = StringIO('<html><translate>hello world!</translate>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_plural_form(self):
        buf = StringIO(
            (
                '<html><translate translate-plural="hello {$count$} worlds!">'
                'hello one world!</translate>'
            ))

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'ngettext',
                 ('hello one world!',
                  'hello %(count) worlds!'
                  ),
                 [])
            ], messages)

    def test_translate_tag_comments(self):
        buf = StringIO(
            '<html><translate translate-comment='
            '"What a beautiful world">hello world!</translate>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_comments(self):
        buf = StringIO(
            '<html><div translate translate-comment='
            '"What a beautiful world">hello world!</translate>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_multiple_comments(self):
        buf = StringIO(
            '<html><div translate '
            'translate-comment="What a beautiful world"'
            'translate-comment="Another comment"'
            '>hello world!</translate>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!',
                 [
                     'What a beautiful world',
                     'Another comment'
                 ])
            ],
            messages)

