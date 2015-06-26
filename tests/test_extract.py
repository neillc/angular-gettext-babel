import unittest

#import pytest

from babel.messages import extract
from babel._compat import StringIO

from angular_gettext_babel.extract import extract_angular

default_keys = [] #extract.DEFAULT_KEYWORDS.keys()


class ExtractAngularTestCase(unittest.TestCase):

    def test_extract_no_tags(self):
        buf = StringIO('<html></html>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([], messages)

    def test_simple_string(self):
        buf = StringIO('<html><div translate>hello world!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_interpolation(self):
        buf = StringIO('<html><div translate>hello {$name$}!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello %(name)!', [])], messages)

    def test_interpolation_func_call(self):
        buf = StringIO('<html><div translate>hello {$func(name)$}!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello %(func(name))!', [])], messages)

    def test_interpolation_list(self):
        buf = StringIO('<html><div translate>hello {$name[1]$}!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello %(name[1])!', [])], messages)

    def test_interpolation_dict(self):
        buf = StringIO(r"<html><div translate>hello {$name['key']$}!</div>")

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', r"hello %(name['key'])!", [])], messages)

    def test_interpolation_dict_double_quote(self):
        buf = StringIO(r"""<html><div translate>hello {$name["key"]$}!</div>""")

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', r'hello %(name["key"])!', [])], messages)

    def test_interpolation_object(self):
        buf = StringIO('<html><div translate>hello {$name.attr$}!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello %(name.attr)!', [])], messages)

    def test_interpolation_spaces(self):
        """
        Spaces are not valid in interpolation expressions, but we don't
        currently complain about them
        """
        buf = StringIO('<html><div translate>hello {$name attr$}!</div>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello {$name attr$}!', [])], messages)

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
        buf = StringIO('<html><div id="translate" translate>hello world!</div>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)


