#
# Copyright (c) 2013-2014 Kevin Steves <kevin.steves@pobox.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import logging
import xml.etree.ElementTree as etree

from . import DEBUG1


class PanCommit:
    def __init__(self,
                 validate=False,
                 force=False,
                 commit_all=False,
                 merge_with_candidate=False):
        self._log = logging.getLogger(__name__).log
        self._validate = validate
        self._force = force
        self._commit_all = commit_all
        self._merge_with_candidate = merge_with_candidate
        self.partial = set()
        self._vsys = set()
        self._device = None
        self._device_group = None

    def validate(self):
        self._validate = True

    def force(self):
        self._force = True

    def commit_all(self):
        self._commit_all = True

    def merge_with_candidate(self):
        self._merge_with_candidate = True

    def device_and_network_excluded(self):
        part = 'device-and-network-excluded'
        self.partial.add(part)

    def policy_and_objects_excluded(self):
        part = 'policy-and-objects-excluded'
        self.partial.add(part)

    def shared_object_excluded(self):
        part = 'shared-object-excluded'
        self.partial.add(part)

    def no_vsys(self):
        part = 'no-vsys'
        self.partial.add(part)

    def vsys(self, vsys):
        if not self._commit_all:
            part = 'vsys'
            self.partial.add(part)

        if isinstance(vsys, str):
            vsys = [vsys]
        for name in vsys:
            self._vsys.add(name)

    def device(self, serial):
        self._device = serial

    def device_group(self, device_group):
        self._device_group = device_group

    def cmd(self):
        if self._commit_all:
            return self.__commit_all()
        else:
            return self.__commit()

    def __commit_all(self):
        root = etree.Element('commit-all')
        shared_policy = etree.SubElement(root, 'shared-policy')

        if self._device:
            etree.SubElement(
                shared_policy, 'device').text = self._device

        if self._device_group:
            etree.SubElement(
                shared_policy, 'device-group').text = self._device_group

        # default when no <merge-with-candidate-cfg/> is 'yes'
        # we default to 'no' like the Web UI
        if self._merge_with_candidate:
            merge = 'yes'
        else:
            merge = 'no'
        etree.SubElement(
            shared_policy, 'merge-with-candidate-cfg').text = merge

        if self._vsys:
            etree.SubElement(
                shared_policy, 'vsys').text = self._vsys.pop()

        s = etree.tostring(root, encoding='unicode')
        self._log(DEBUG1, 'commit-all cmd: %s', s)

        return s

    def __commit(self):
        root = etree.Element('commit')
        parent = root

        if self._validate:
            parent = etree.SubElement(parent, 'validate')

        if self._force:
            parent = etree.SubElement(parent, 'force')

        if self.partial:
            partial = etree.SubElement(parent, 'partial')

            for part in self.partial:
                if part == 'vsys':
                    vsys = etree.SubElement(partial, 'vsys')
                    for name in self._vsys:
                        etree.SubElement(vsys, 'member').text = name
                elif part == 'device-and-network-excluded':
                    x = etree.SubElement(partial, 'device-and-network')
                    x.text = 'excluded'
                elif part == 'policy-and-objects-excluded':
                    x = etree.SubElement(partial, 'policy-and-objects')
                    x.text = 'excluded'
                elif part == 'shared-object-excluded':
                    x = etree.SubElement(partial, 'shared-object')
                    x.text = 'excluded'
                elif part == 'no-vsys':
                    etree.SubElement(partial, 'no-vsys')

        s = etree.tostring(root, encoding='unicode')
        self._log(DEBUG1, 'commit cmd: %s', s)

        return s


if __name__ == '__main__':
    # python3 -m pan.commit
    import pan.commit

    c = pan.commit.PanCommit()
    c.force()
    c.device_and_network_excluded()
    c.policy_and_objects_excluded()
    c.shared_object_excluded()
    c.vsys(['vsys4', 'vsys5'])
    print('cmd:', c.cmd())

    c = pan.commit.PanCommit(commit_all=True,
                             merge_with_candidate=True)
    c.device_group('pan-device-group')
    print('cmd:', c.cmd())
