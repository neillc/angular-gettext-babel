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

    def test_plural_string(self):
        buf = StringIO('<span translate translate-n="msgCount" translate-plural="{{$count}} new messages">1 new message</span>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)


