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
import re


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

    regex = r"""(<[\w-]+ translate>)([\w\d\s\.A\?\!$}{\[\]'"\)\(]+)(</[\w-]+>)"""
    interpolation_regex = r"""{\$([\w\."'\]\[\(\)]+)\$}"""

    for line_no, line in enumerate(fileobj):
        matches = re.findall(regex, line)
        for match in matches:
            interpolated = re.sub(interpolation_regex, r'%(\1)', match[1])

            yield (line_no + 1, u'gettext', interpolated, [])
