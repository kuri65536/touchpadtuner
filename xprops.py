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
# from logging import info

from common import (Percent,
                    parseBool, parseFloat, parseInt, parseIntOrPercent, )

try:
    from typing import (Any, Callable, Dict, IO, Iterable, Iterator,
                        List, Optional, Sized, Text, Tuple, Union, )
    Any, Callable, Dict, IO, Iterable, List, Optional, Text, Tuple, Union
    Iterator
except:
    pass


def allok(seq):
    # type: (List[Text]) -> bool
    return True


class PropFormat(Sized):  # {{{1
    def __init__(self, *args):  # {{{1
        # type: (Tuple[Text, ...]) -> None
        self.dgts = []  # type: List[int]
        if args[0][0] == "dummy":
            self.fmts = ()  # type: Tuple[Tuple[Text, Text], ...]
            return
        src = []  # type: List[Tuple[Text, Text]]
        for arg in args:
            n = 0
            if len(arg) >= 3:
                n = int(arg[2])
            src.append((arg[0], arg[1]))
            self.dgts.append(n)
        self.fmts = tuple(src)

    def __len__(self):  # {{{1
        # type: () -> int
        return len(self.fmts)

    def __getitem__(self, idx):  # {{{1
        # type: (Any) -> Tuple[Text, Text]
        assert isinstance(idx, int)
        seq = self.fmts[idx]
        return (seq[0], seq[1])

    def __iter__(self):  # {{{1
        # type: () -> Iterator[Tuple[Text, Text]]
        for fmt in self.fmts:
            yield fmt


class NProp(object):  # {{{1
    # {{{1
    '''## class structure {{{2

        ```class structure
        xinput          -> NProp[NProp] -> xinput
        xconf           -> NPropDb[NProp] -> xconf
        GUI -> XInputDB[NPropGui] -> NProp
        ```


        ## xinput list-props and GUI pages {{{2
        Device 'ELAN1201:00 04F3:3054 Touchpad':
        Device Enabled (140):                     1
        Coordinate Transformation Matrix (142):   1.0, 0.0, 0.0,
                                                  0.0, 1.0, 0.0,
                                                  0.0, 0.0, 1.0
        Device Accel Profile (270):               1
        Device Accel Constant Deceleration (271): 2.500000
        Device Accel Adaptive Deceleration (272): 1.000000
   page Device Accel Velocity Scaling (273):      12.500000
      4 Synaptics Edges (274):                    127, 3065, 98, 1726
      1 Synaptics Finger (275):                   50, 100, 0
      1 Synaptics Tap Time (276):                 180
      1 Synaptics Tap Move (277):                 161
      1 Synaptics Tap Durations (278):            180, 180, 100
      x Synaptics ClickPad (279):                 1
      x Synaptics Middle Button Timeout (280):    0
      2 Synaptics Two-Finger Pressure (281):      282
      2 Synaptics Two-Finger Width (282):         7
      2 Synaptics Scrolling Distance (283):       73, 73
      4 Synaptics Edge Scrolling (284):           1, 0, 0
      2 Synaptics Two-Finger Scrolling (285):     1, 1
      5 Synaptics Move Speed (286):               1.0, 1.75, 0.054407, 0.000000
      x Synaptics Off (287):                      1
      5 Synaptics Locked Drags (288):             0
      5 Synaptics Locked Drags Timeout (289):     5000
      1 Synaptics Tap Action (290):               2, 3, 0, 0, 1, 3, 2
      1 Synaptics Click Action (291):             1, 3, 0
      5 Synaptics Circular Scrolling (292):       0
      5 Synaptics Circular Scrolling Distance (293): 0.100000
      5 Synaptics Circular Scrolling Trigger (294):  0
      5 Synaptics Circular Pad (295):             0
      4 Synaptics Palm Detection (296):           0
      4 Synaptics Palm Dimensions (297):          10, 200
      5 Synaptics Coasting Speed (298):           20.000000, 50.000000
      5 Synaptics Pressure Motion (299):          30, 160
      5 Synaptics Pressure Motion Factor (300):   1.000000, 1.000000
      x Synaptics Resolution Detect (301):        1
      x Synaptics Grab Event Device (302):        0
      5 Synaptics Gestures (303):                 1
      6 Synaptics Capabilities (304):             1, 0, 0, 1, 1, 0, 0
      6 Synaptics Pad Resolution (305):           31, 31
      x Synaptics Area (306):                     0, 0, 0, 0
      4 Synaptics Soft Button Areas (307):        1596, 0, 1495, 0, 0, 0, 0, 0
      5 Synaptics Noise Cancellation (308):       18, 18
      x Device Product ID (267):                  1267, 12372
      x Device Node (266):                        "/dev/input/event8"
    '''

    def __init__(self, key, fmts, hint):  # {{{1
        # type: (Text, Optional[PropFormat], Text) -> None
        fmts = fmts if fmts is not None else PropFormat(("dummy", ""))

        # number of xinput property-id
        self.prop_id = -1
        # loaded values from xinput
        self.vals = [None] * self.prop_num(fmts)   # type: List[Any]

        # formatter for .xconf output
        self.fmts = fmts
        # keyword in xinput list-props
        self.key = key
        # text for this property in man synaptic
        self.hint = self.format_hint(hint)

    def is_valid(self):  # {{{1
        # type: () -> bool
        return self.prop_id != -1

    @classmethod  # from_cmd {{{1
    def from_cmd(cls, cmd):
        # type: (List[Text]) -> Optional['NProp']
        if "xinput" not in cmd[0]:
            cmd = cmd[1:]
        if not cmd[0].startswith("set-") or not cmd[0].endswith("-prop"):
            return None
        if cmd[0] == "set-int-prop":
            typ = "int"
        elif cmd[0] == "set-float-prop":
            typ = "float"
        else:
            typ = "atm"
        cmd = cmd[1:]
        if not cmd[0].isdigit():
            return None
        n = int(cmd[0])
        cmd = cmd[1:]
        if typ == "int":
            if not cmd[0].isdigit() and cmd[0] in ("8", "16", "32"):
                return None
            # t2 = int(cmd[0])
            cmd = cmd[1:]
        ret = NProp.prop_get(n)  # update vals
        assert ret is not None
        ret.vals = cmd
        return ret

    @classmethod
    def compose_format(cls, fmt, v):  # cls {{{1
        # type: (Text, Any) -> Text
        # TODO: more complex conversion.
        fmt = fmt.replace("{:P}", "{}")
        if not isinstance(v, (tuple, list)):
            return fmt.format(v)
        _v = []  # type: List[Any]
        for i in v:
            if isinstance(i, Percent):
                _v.append(str(i))
            elif "{:d}" in fmt:
                _v.append(int(i))
            elif "{:f}" in fmt:
                _v.append(float(i))
            else:
                _v.append(str(i))
        return fmt.format(*_v)

    def compose(self, idx):  # {{{1
        # type: (int) -> Text
        opts = self.fmts
        assert 0 <= idx < len(opts)
        opt, fmt = opts[idx]
        fmt = ((" " * 8) + 'Option "' + opt + '" "' +
               fmt + '"  # by touchpadtuner\n')
        val = self.vals[idx]
        return self.compose_format(fmt, val)

    def compose_all(self):  # {{{1
        # type: () -> Text
        ret = ""
        for n, val in enumerate(self.vals):
            if val is None:
                continue
            ret += self.compose(n)
        return ret

    @classmethod
    def parse(cls, src):  # cls {{{1
        # type: (Text) -> Optional[NProp]
        _src = src.strip()
        if _src.startswith("#"):
            return None  # comment line
        if not _src.lower().startswith("option "):
            return None  # not option line.
        _src = _src[8:].strip()  # remove 'Option' with starting '"'.
        for key, ret in cls.props():
            for n, (opt, fmt) in enumerate(ret.fmts):
                o = opt + '" '
                if not _src.startswith(o):
                    continue
                _src = _src[len(o):]
                _src = cls.parse_quote(_src)
                v = cls.parse_xconf(fmt, _src)
                if v is None:
                    break
                ret.vals[n] = v
                return ret
        return None

    @classmethod
    def parse_quote(cls, src):  # cls {{{1
        # type: (Text) -> Text
        ret = ""
        f_quote, f_escape = False, False
        for ch in src:
            if not f_quote:
                if ch == '"':
                    f_quote = True
                continue
            if f_escape:
                f_escape = False
            elif ch == '\\':
                f_escape = True
                continue
            elif ch == '"':
                return ret
            ret += ch
        # can't parse in quote
        return src

    @classmethod
    def parse_xconf(self, fmt, _src):  # {{{1
        # type: (Text, Text) -> Any
        # TODO(Shimoda): remove the inline comment or ends '"'.
        if fmt == "{:d}":
            return parseInt(_src)
        elif fmt == "{:b}":
            return parseBool(_src)
        elif fmt == "{:f}":
            return parseFloat(_src)
        # else:
        #     assert False, "xconfs fmt {} not implemented".format(fmt)

        seq = fmt.split(" ")
        func = parseInt  # type: Callable[[Any], Any]
        if seq[0] == "{:d}":
            func = parseInt
        elif seq[0] == "{:b}":
            func = parseBool
        elif seq[0] == "{:f}":
            func = parseFloat
        elif seq[0] == "{:P}":
            func = parseIntOrPercent
        else:
            raise RuntimeError("format:{} can't be parsed".format(seq[0]))

        ret = []  # type: List[Any]
        for n, term in enumerate(_src.split(" ")):
            if n >= len(seq):
                return ret
            v = func(term)
            if v is None:
                # TODO(Shimoda): log error messsage.
                return None
            ret.append(v)
        return ret

    def update(self, prop, idx):  # {{{1
        # type: ('NProp', int) -> 'NProp'
        self.vals[idx] = prop.vals[idx]
        return self

    @classmethod  # props {{{1
    def props(cls):
        # type: () -> Iterator[Tuple[Text, 'NProp']]
        for k, v in cls.__dict__.items():
            if not isinstance(v, NProp):
                continue
            yield (k, v)

    @classmethod  # prop_get {{{1
    def prop_get(cls, n):
        # type: (int) -> Optional['NProp']
        for k, prop in cls.props():
            if prop.prop_id == n:
                return prop
        return None

    @classmethod  # prop_get_by_key {{{1
    def prop_get_by_key(cls, src):
        # type: (Text) -> Optional['NProp']
        for k, prop in cls.props():
            if prop.key in src:
                return prop
        return None

    @classmethod  # format_hint {{{1
    def format_hint(cls, src):
        # type: (Text) -> Text
        ret = src
        seq = src.splitlines()
        if len(seq) < 1:
            return "\n"
        l1 = seq[0].strip()
        if len(l1) < 1:
            return "\n" + ret
        if len(seq) < 2:
            return "\n" + l1
        l2 = seq[1:]
        n = 20
        for l in l2:
            i = len(l.lstrip())
            if i < 1:
                continue
            i = len(l) - i
            n = min((i, n))
        n = n if n < 20 else 0
        l1 = "\n" + (" " * n) + l1.lstrip()
        return l1 + "\n" + "\n".join(l2)

    def prop_num(self, fmts):  # {{{1
        # type: (Optional[PropFormat]) -> int
        if fmts is None:
            return 0
        sum = 0
        for title, args in fmts:
            title
            count = len(args) - len(args.replace("{", ""))
            sum += count
        return sum

    def update_by_prop(self, inp):  # {{{1
        # type: (NProp) -> None
        assert self.prop_id == inp.prop_id
        assert len(self.vals) > 0
        for n, val in inp.vals:
            if val is None:
                continue  # skip no input.
            self.vals[n] = val  # always override.

    def same_prop(self, b):  # {{{1
        # type: (NProp) -> bool
        assert self.prop_id == b.prop_id
        assert len(self.vals) > 0
        for va, vb in zip(self.vals, b.vals):
            if va is None:
                continue
            if vb is None:
                return False
            if va != vb:
                return False
        return True


class NPropDb(Sized):  # {{{1
    def __init__(self):  # {{{1
        # type: () -> None
        self.props = {"xinput": []}  # type: Dict[Text, List[NProp]]

    def get(self, sec, prop, fallback=None):  # {{{1
        # type: (Text, NProp, Optional[NProp]) -> NProp
        if sec not in self.props:
            pass
        else:
            seq = self.props[sec]
            for i in seq:
                if i.prop_id == prop.prop_id:
                    return i
        if fallback is not None:
            return fallback
        raise KeyError("invalid key '{}'".format())

    def put(self, sec, prop):  # {{{1
        # type: (Text, NProp) -> None
        try:
            prop_cur = self.get(sec, prop)
        except KeyError:
            if sec not in self.props:
                # TODO(shimoda): automatic section creations?
                self.props[sec] = []
            self.props[sec].append(prop)
            return
        prop_cur.update_by_prop(prop)

    def __len__(self):  # {{{1
        # type: () -> int
        return len(self.props)

    def items(self, sec):  # {{{1
        # type: (Text) -> Iterable[Tuple[int, NProp]]
        for i in self.props[sec]:
            yield (i.prop_id, i)


# main {{{1
def main():  # {{{1
    # type: () -> int
    pass  # TODO: launch test


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
