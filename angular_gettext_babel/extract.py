# Copyright 2015, Rackspace, US, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import html.parser
import re


class AngularGettextHTMLParser(html.parser.HTMLParser):
    """
    Parse HTML to find translate directives.

    Note: This will not cope with nested tags (which I don't think make any
    sense)
    """

    def __init__(self):
        super(AngularGettextHTMLParser,self).__init__()
        self.in_translate = False
        self.data = ''

    def handle_starttag(self, tag, attrs):
        print("Encounterd a start_tag:", tag, attrs, self.getpos())
        self.in_translate = False
        self.data = ''
        if attrs:
            print ([attr[0] for attr in attrs])
            if 'translate' in [attr[0] for attr in attrs]:
                print('translateable')
                self.in_translate = True

    def handle_data(self, data):
        self.data += data
        print('data', self.data)

    def handle_endtag(self, tag):
        print('end!!!!')
        if self.in_translate:
            print('this is translateable')
            print ((1, u'gettext', self.data, []))
            yield (1, u'gettext', self.data, [])
        else:
            print('not translateable')
def extract_angular(fileobj, keywords, comment_tags, options):
    """Extract messages from angular template (HTML) files that use the
    angular-gettext translate directive as per
    https://angular-gettext.rocketeer.be/ .

    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: This is a standard parameter so it isaccepted but ignored.

    :param comment_tags: This is a standard parameter so it is accepted but
                        ignored.
    :param options: Another standard parameter that is accepted but ignored.
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``

    This particular extractor is quite simple because it is intended to only
    deal with angular templates which do not need comments, or the more
    complicated forms of translations.

    A later version will address pluralization.
    """

    regex = r'(<[\w-]+ translate>)([\w\d\s\.A\?\!]+)(</[\w-]+>)'

    parser = AngularGettextHTMLParser()

    print('called')

    for line in fileobj:
        # print(line)
        parser.feed(line)

        # matches = re.findall(regex, line)
        # for match in matches:
        #     yield (line_no + 1, u'gettext', match[1], [])

import io
s = io.StringIO(initial_value="""<html>
<div translate>text</div>
</html>""")
#extract_angular(s, [], [], {})
# for ln, funcn, msg, xtra in extract_angular(s, [], [], {}):
#     print(ln, funcn, msg, xtra)
x = extract_angular(s, [], [], {})
while x:
    print('x=', x)
    x = extract_angular(s, [], [], {})
print(s)
print('done')