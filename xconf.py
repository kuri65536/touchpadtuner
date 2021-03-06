#! env python
# -= encoding=utf-8 =-
'''
Copyright (c) 2018, 2017, shimoda as kuri65536 _dot_ hot mail _dot_ com
                    ( email address: convert _dot_ to . and joint string )

This Source Code Form is subject to the terms of the Mozilla Public License,
v.2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
'''
from __future__ import print_function
from logging import info

import common
from xprops import NProp
from xprops2 import NPropDb

try:
    from typing import (Any, Callable, Dict, IO, Iterable, List, Optional,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, Iterable, List, Optional, Text, Tuple, Union
except:
    pass


def allok(seq):
    # type: (List[Text]) -> bool
    return True


class XSectionSynaptics(object):  # {{{1
    def __init__(self):
        # type: () -> None
        self.f_synaptics = False
        self.f_touchpad = False
        self.f_devicepath = False
        self.f_bcm5974 = False

    @classmethod  # is: Identifier "something" {{{1
    def is_identifier(self, line):
        # type: (Text) -> Text
        line = line.strip().lower()
        if not line.startswith("identifier"):
            return ""
        seq = line.split('"')
        ret = seq[1]
        return ret

    @classmethod  # is: Driver "synaptics"  {{{1
    def is_driver_synaptics(self, line):
        # type: (Text) -> bool
        line = line.strip().lower()
        if not line.startswith('driver '):
            return False
        line = line[7:].strip()
        if not line.startswith('"synaptics"'):
            return False
        return True

    @classmethod  # is: MatchIsTouchpad "on"  {{{1
    def is_touchpad(self, line):
        # type: (Text) -> bool
        line = line.strip().lower()
        if not line.startswith('matchistouchpad '):
            return False
        line = line[16:].strip()
        if not line.startswith('"on"'):
            return False
        return True

    @classmethod  # is: MatchProduct "bcm5974"  {{{1
    def is_match_product_bcm5974(cls, line):
        # type: (Text) -> bool
        line = line.strip().lower()
        if not line.startswith('matchproduct '):
            return False
        line = line[13:].strip()
        if "bcm5974" not in line:
            return False
        return True

    @property  # is_enabled {{{1
    def is_enabled(self):
        # type: () -> bool
        return all([self.f_synaptics, self.f_touchpad,
                    not self.f_bcm5974])

    def parse_line(self, line):  # {{{1
        # type: (Text) -> None
        if (not self.f_bcm5974 and
                self.is_match_product_bcm5974(line)):
            self.f_bcm5974 = True
            return
        if (not self.f_synaptics and
                self.is_driver_synaptics(line)):
            self.f_synaptics = True
            return
        if (not self.f_touchpad and
                self.is_touchpad(line)):
            self.f_touchpad = True
            return


class XConfFile(object):  # {{{1
    # {{{1
    def __init__(self):  # {{{1
        # type: () -> None
        self.section_parser_clear()

    def section_parser_clear(self):  # {{{1
        # type: () -> None
        self.f_section = False
        self.f_endofsection = False
        self.n_section = 0
        self.cur_section = ""
        self.sections = {}  # type: Dict[Text, int]

    def xconf_iter(self, fname):  # {{{1
        # type: (Text) -> Iterable[Tuple[int, Text, Text]]
        self.section_parser_clear()
        flagsSyn = XSectionSynaptics()
        with common.open_file(fname, "r") as fp:
            for i, line in enumerate(fp):
                sec = self.section_parser(line)
                if sec >= 0:
                    flagsSyn.parse_line(line)
                    yield (i, self.cur_section, line)
                else:
                    flagsSyn = XSectionSynaptics()
                    yield (i, "", line)

    def read(self, fname):  # {{{1
        # type: (str) -> NPropDb
        ret = NPropDb()
        for i, sec, line in self.xconf_iter(fname):
            if len(sec) < 1:
                continue
            info("xconf-read: section '{}'".format(self.cur_section))
            prop = NProp.parse_xconfline(line)
            if prop is None:
                continue  # just ignore that line could not be parsed.
            ret.put(sec, prop[1])
        ret.report()
        return ret

    def save(self, fname, fnameIn, db):  # {{{1
        # type: (Text, Text, NPropDb) -> bool
        '''sample output {{{3
            # Example xorg.conf.d snippet that assigns the touchpad driver
            # ...
            Section "InputClass"
                    Identifier "touchpad catchall"
                    Driver "synaptics"
                    MatchIsTouchpad "on"
                    Option "TapButton3" "2"
                    Option "FingerLow" "50"
                    Option "FingerHigh" "100"
                    Option "VertTwoFingerScroll" "on"
                    Option "HorizTwoFingerScroll" "on"
            # This option is recommend on all Linux systems using evdev,
            # ...
                  MatchDevicePath "/dev/input/event*"
            EndSection

            # This option enables the bottom right corner to be a right button
            # ...
            Section "InputClass"
                    Identifier "Default clickpad buttons"
                    MatchDriver "synaptics"
                    Option "SoftButtonAreas" "50% 0 82% 0 0 0 0 0"
                    Option "SecondarySoftButtonAreas"
                        "58% 0 0 15% 42% 58% 0 15%"
            EndSection  # }}}
        '''
        fp = common.open_file(fname, "w")
        prv_sec = ""
        done = []  # type: List[Text]
        for i, sec, line in self.xconf_iter(fnameIn):
            if len(sec) < 1:
                if len(prv_sec) > 0:
                    self.save_remains(fp, db, prv_sec, done)
                prv_sec, done = "", []
                fp.write(line)
                continue
            prv_sec = sec
            for i in range(1):
                tup = NProp.parse_xconfline(line)
                if tup is None:
                    continue  # write through
                prop = tup[1]
                cur = db.get(sec, prop, NProp("", None, ""))
                if cur.key == "":
                    done.append(tup[0])
                    continue  # write thruogh
                if prop.same_prop(cur):
                    done.append(tup[0])
                    continue  # write thruogh
                # just update props, write at save_remains().
                cur.update_by_prop_passive(prop)
                break
            else:
                fp.write(line)

        # did not close section...
        fp.close()
        return False

    def is_begin_of_section(self, line):  # {{{2
        # type: (Text) -> Text
        line = line.strip().lower()
        if not line.startswith('section '):
            return ""
        seq = line.split('"')
        ret = seq[1]
        return ret

    def is_end_section(self, line):  # {{{2
        # type: (Text) -> bool
        line = line.strip().lower()
        return line.startswith("endsection")

    def section_parser(self, line):  # {{{1
        # type: (Text) -> int
        if self.f_endofsection:
            return -1
        if self.is_end_section(line):
            self.f_endofsection = True
            return -1
        if not self.f_section:
            # secname is lower-case
            secname = self.is_begin_of_section(line)
            if secname == "":
                return -1
            if secname != "inputclass":
                return -1
            self.n_section += 1
            self.f_section = True
            return self.n_section
        if self.cur_section == "":
            id_name = XSectionSynaptics.is_identifier(line)
            if id_name != "":
                self.cur_section = id_name
                self.sections[id_name] = self.n_section
                return self.n_section
        return self.n_section

    def save_remains(self, fp, db, sec, done):  # {{{1
        # type: (IO[Text], NPropDb, Text, List[Text]) -> bool
        for n, prop in db.items(sec):
            info("xconf.save_remains: {}".format(prop.key))
            for key, line in prop.compose_xconf():
                # TODO(Shimoda): check v is default
                # if is_default(prop):
                #    continue
                info("xconf.save_remains: {}".format(key))
                if key in done:
                    continue
                if '"nnn"' in line:
                    continue
                fp.write(line)
        return False


# main {{{1
def main():  # {{{1
    # type: () -> int
    # TODO(shimoda): more tests and move to a test folder.
    import logging
    from common import opts
    from xprops2 import NProp1804
    logging.basicConfig(format="%(levelname)-8s:%(asctime)s:%(message)s",
                        level=logging.DEBUG)
    info("xconf:main: start...")
    NProp1804.auto_id()
    NProp1804.props_copy(NProp)
    xf = XConfFile()
    db = xf.read(opts.fnameIn)
    p = db.get(opts.xsection, NProp1804.tap_action)
    p.vals[5] = "3"
    db.put(opts.xsection, p)
    xf.save("test-xconf-save.conf", opts.fnameIn, db)
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
