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
from logging import (debug as debg, error as eror, )

from common import (Percent, )

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

    def count_1fmt(self, fmt):  # {{{1
        # type: (Tuple[Text, Text]) -> int
        args = fmt[1]
        count = len(args) - len(args.replace("{", ""))
        return count

    def count_props(self):  # {{{1
        # type: () -> int
        sum = 0
        for fmt in self.fmts:
            sum += self.count_1fmt(fmt)
        return sum


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

        # number of xinput property-id
        self.prop_id = -1

        # formatter for .xconf output
        fmts = fmts if fmts is not None else PropFormat(("dummy", ""))
        self.fmts = fmts
        # loaded values from xinput
        self.vals = [""] * fmts.count_props()   # type: List[Text]
        # keyword in xinput list-props
        self.key = key
        # text for this property in man synaptic
        self.hint = self.format_hint(hint)

    def copy(self, clear_vals=False):  # {{{1
        # type: (bool) -> 'NProp'
        ret = NProp(self.key, self.fmts, self.hint)
        ret.prop_id = self.prop_id
        if clear_vals:
            vals = []
            for val in self.vals:
                vals.append("")
            self.vals = vals
        return ret

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
        # type: (Text, Text) -> Text
        # TODO(shimoda): more complex conversion.
        fmt = fmt.replace("{:P}", "{}")
        if not isinstance(v, (tuple, list)):
            return v
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
        # type: (int) -> Tuple[Text, Text]
        opts = self.fmts
        assert 0 <= idx < len(opts)
        opt, fmt = opts[idx]
        fmt = ((" " * 8) + 'Option "' + opt + '" "' +
               fmt + '"  # by touchpadtuner\n')
        val = self.vals[idx]
        return opt, self.compose_format(fmt, val)

    def compose_all(self):  # {{{1
        # type: () -> Text
        ret = ""
        for n, val in enumerate(self.vals):
            if len(val) < 1:
                continue
            key, line = self.compose(n)
            ret += line
        return ret

    def compose_xconf(self):  # {{{1
        # type: () -> Iterable[Tuple[Text, Text]]
        n = 0
        for key, fmt in self.fmts:
            params = ""
            m = self.fmts.count_1fmt((key, fmt))
            vals = self.vals[n: n + m]
            n += m
            for val in vals:
                if len(val) < 1:
                    # TODO(shimoda): take default for missing parts.
                    eror("missing parameter: {}".format(key))
                    params += ' "nnn"'
                else:
                    params += ' "' + val + '"'
            line = ((" " * 8) + 'Option "' + key + '"' +
                    params + '  # by touchpadtuner\n')
            yield (key, line)

    @classmethod
    def parse_xconfline(cls, src):  # cls {{{1
        # type: (Text) -> Optional[Tuple[Text, NProp]]
        _src = src.strip()
        if _src.startswith("#"):
            return None  # comment line
        if not _src.lower().startswith("option "):
            return None  # not option line.
        _src = _src[8:].strip()  # remove 'Option' with starting '"'.
        debg("NProp.xconf-parse: {}".format(_src))
        for key, prop in cls.props():
            idx = 0
            for n, (opt, fmt) in enumerate(prop.fmts):
                o = opt.lower() + '" '
                if not _src.lower().startswith(o):
                    idx += prop.fmts.count_1fmt((opt, fmt))
                    continue
                debg("NProp.xconf-parse: match with {}".format(o))
                _src = _src[len(o):]
                _src = cls.parse_quote(_src)
                ret = prop.copy(clear_vals=True)
                for n, v in cls.parse_xconfopt(idx, fmt, _src):
                    ret.vals[n] = v
                return opt, ret
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
    def parse_xconfopt(self, idx, fmt, _src):  # {{{1
        # type: (int, Text, Text) -> Iterable[Tuple[int, Text]]
        # TODO(Shimoda): remove the inline comment or ends '"'.
        if fmt == "{:d}":
            yield (idx, _src)
            return
        elif fmt == "{:b}":
            yield (idx, _src)
            return
        elif fmt == "{:f}":
            yield (idx, _src)
            return
        # else:
        #     assert False, "xconfs fmt {} not implemented".format(fmt)

        seq = fmt.split(" ")
        for n, term in enumerate(_src.split(" ")):
            if n >= len(seq):
                return
            yield (idx + n, term)

    def update(self, prop, idx):  # {{{1
        # type: ('NProp', int) -> 'NProp'
        self.vals[idx] = prop.vals[idx]
        return self

    @classmethod  # props {{{1
    def props(cls):
        # type: () -> Iterator[Tuple[Text, 'NProp']]
        n = 0
        for k, v in cls.__dict__.items():
            if not isinstance(v, NProp):
                continue
            n += 1
            yield (k, v)
        assert n > 0, "use NPropDb.auto_id() before use NProp."

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
        for n, val in enumerate(inp.vals):
            if len(val) < 1:
                continue  # skip no input.
            self.vals[n] = val  # always override.

    def update_by_prop_passive(self, inp):  # {{{1
        # type: (NProp) -> None
        assert self.prop_id == inp.prop_id
        assert len(self.vals) > 0
        for n, val in enumerate(inp.vals):
            if len(val) < 1:
                continue  # skip no input.
            cur = self.vals[n]
            if len(cur) > 0:
                continue  # skip, the current value is remained.
            self.vals[n] = val  # override if the current value is none.

    def same_prop(self, b):  # {{{1
        # type: (NProp) -> bool
        assert self.prop_id == b.prop_id
        assert len(self.vals) > 0
        for va, vb in zip(self.vals, b.vals):
            if len(va) < 1:
                continue  # ignore (not set.)
            if va != vb:
                return False
        return True


# main {{{1
def main():  # {{{1
    # type: () -> int
    pass  # TODO: launch test


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
