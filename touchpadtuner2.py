#! /usr/bin/python3
# -= encoding=utf-8 =-
'''
Copyright (c) 2018, 2017, shimoda as kuri65536 _dot_ hot mail _dot_ com
                    ( email address: convert _dot_ to . and joint string )

This Source Code Form is subject to the terms of the Mozilla Public License,
v.2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
'''
from __future__ import print_function
import sys
import os
import subprocess
import logging
from logging import debug as debg, info, warning as warn, error as eror

import common
from common import (BoolVar, CmbVar, FltVar, IntVar,
                    open_file, )
from xprops import NProp as NProp1, NPropDb
from xprops2 import NProp1804 as NProp
from xconf import XConfFile
import wraptk as draw

NProp1

try:
    from typing import (Any, Callable, Dict, IO, Iterable, List, Optional,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, Iterable, List, Optional, Text, Tuple, Union
except:
    pass


if sys.version_info[0] == 3:
    import tkinter as tk
    import tkinter.messagebox as messagebox
    from tkinter import ttk
else:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox


def allok(seq):
    # type: (List[Text]) -> bool
    return True


def apply_none(cmd):  # {{{1
    # type: (List[Text]) -> bool
    return False


class NPropGui(object):  # {{{1
    def __init__(self, prop):  # {{{1
        # type: (NProp1) -> None
        self.prop = prop
        self.typ = "32"
        self.vars = []  # type: List[Any]
        self._cache = []  # type: List[Text]

    def is_loaded(self):  # {{{1
        # type: () -> bool
        return len(self._cache) > 0

    def is_changed(self):  # {{{1
        # type: () -> bool
        if not self.is_loaded():
            self.load()
        cur = self.compose()
        for n, a in enumerate(cur):
            b = self._cache[n]
            if not self.cmp(a, b):
                return True
        return False

    def load(self):  # {{{1
        # type: () -> List[Text]
        ret = self._cache = xi.prop_get(self.prop.prop_id)
        return ret

    def compose(self):  # {{{1
        # type: () -> List[Text]
        ret = []
        for var in self.vars:
            n = var.get()
            ret.append(Text(n))
        return ret

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        assert False, "must be override"

    def sync(self):  # {{{1
        # type: () -> bool
        args = self.compose()
        xi.prop_set_int(self.prop.prop_id, self.typ, args)
        return False

    def current(self, i):  # {{{1
        # type: (int) -> Text
        if i < len(self.vars):
            var = self.vars[i]
            ret = var.get()
            txt = Text(ret)
            return txt
        if not self.is_loaded():
            self.load()
        txt = self._cache[i]
        return txt


class NPropGuiInt(NPropGui):  # {{{1
    def __init__(self, prop, typ):  # {{{1
        # type: (NProp1, int) -> None
        NPropGui.__init__(self, prop)
        self.vars = []  # type: List[IntVar]
        self.typ = Text(typ)

    def append(self, var):  # {{{1
        # type: (IntVar) -> 'NPropGuiInt'
        self.vars.append(var)
        return self

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        return a == b


class NPropGuiFlt(NPropGui):   # {{{1
    def __init__(self, prop):  # {{{1
        # type: (NProp1) -> None
        NPropGui.__init__(self, prop)
        self.vars = []  # type: List[FltVar]

    def append(self, var):  # {{{1
        # type: (FltVar) -> 'NPropGuiFlt'
        self.vars.append(var)
        return self

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        af = float(a)
        bf = float(b)
        df = af - bf
        df = df if df >= 0 else -df
        dgt = self.prop.fmts.dgts[0]  # TODO: determine index.
        if df < 10 ** -dgt:
            return True
        return False

    def sync(self):  # {{{1
        # type: () -> bool
        args = self.compose()
        # TODO: 8 or 32
        xi.prop_set_flt(self.prop.prop_id, args)
        return False


class NPropGuiBol(NPropGui):   # {{{1
    def __init__(self, prop):  # {{{1
        # type: (NProp1) -> None
        NPropGui.__init__(self, prop)
        self.typ = "8"
        self.vars = []  # type: List[BoolVar]

    def append(self, var):  # {{{1
        # type: (BoolVar) -> 'NPropGuiBol'
        self.vars.append(var)
        return self

    def compose(self):  # {{{1
        # type: () -> List[Text]
        ret = []
        for var in self.vars:
            n = var.get()
            v = "1" if n else "0"
            ret.append(v)
        return ret

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        af = a.lower() in ("1", "true")
        bf = b.lower() in ("1", "true")
        return af == bf


class NPropGuiCmb(NPropGui):   # {{{1
    def __init__(self, prop, typ):  # {{{1
        # type: (NProp1, int) -> None
        NPropGui.__init__(self, prop)
        self.typ = Text(typ)
        self.vars = []  # type: List[CmbVar]

    def append(self, var):  # {{{1
        # type: (CmbVar) -> 'NPropGuiCmb'
        self.vars.append(var)
        return self

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        return a == b


class XInputDB(object):  # {{{1
    # {{{1
    dev = 11

    f_section = False
    n_section = 0
    cur_section = ""
    sections = {}  # type: Dict[int, Text]

    propsdb = {}  # type: Dict[str, int]
    cmd_bin = u"/usr/bin/xinput"
    cmd_shw = [cmd_bin, u"list-props"]
    cmd_int = [cmd_bin, u"set-prop", u"--type=int"]
    cmd_flt = [cmd_bin, u"set-prop", u"--type=float"]
    cmd_atm = [cmd_bin, u"set-prop", u"--type=atom"]

    cmd_wat = "query-state"

    def __init__(self):  # {{{1
        # type: () -> None
        NProp.auto_id()
        self._callback = apply_none  # type: Callable[[List[Text]], bool]

        self._edges = NPropGuiInt(NProp.edges, 32)  # 274
        self._finger = NPropGuiInt(NProp.finger, 32)  # 275
        self._taptime = NPropGuiInt(NProp.tap_time, 32)  # 276
        self._tapmove = NPropGuiInt(NProp.tap_move, 32)  # 277
        self._tapdurs = NPropGuiInt(NProp.tap_durations, 32)  # 278
        self._twoprs = NPropGuiInt(NProp.two_finger_pressure, 32)  # 281
        self._twowid = NPropGuiInt(NProp.two_finger_width, 32)  # 282
        self._scrdist = NPropGuiInt(NProp.scrdist, 32)  # 283
        self._edgescrs = NPropGuiBol(NProp.edgescrs)  # 284
        self._twofingerscroll = NPropGuiBol(NProp.two_finger_scrolling)
        self._movespd = NPropGuiFlt(NProp.move_speed)  # 286
        self._lckdrags = NPropGuiBol(NProp.locked_drags)  # 288
        self._lckdragstimeout = NPropGuiInt(NProp.locked_drags_timeout, 32)
        self._taps = NPropGuiCmb(NProp.tap_action, 8)  # 290
        self._clks = NPropGuiCmb(NProp.click_action, 8)  # 291
        self._cirscr = NPropGuiBol(NProp.cirscr)  # 292
        self._cirdis = NPropGuiFlt(NProp.cirdis)  # 293
        self._cirtrg = NPropGuiCmb(NProp.cirtrg, 8)  # 294
        self._cirpad = NPropGuiBol(NProp.cirpad)  # 295
        self._palmDetect = NPropGuiBol(NProp.palm_detection)  # 296
        self._palmDims = NPropGuiInt(NProp.palm_dimensions, 32)  # 297
        self._cstspd = NPropGuiFlt(NProp.coasting_speed)  # 298
        self._prsmot = NPropGuiInt(NProp.pressure_motion, 32)  # 299 ???
        self._prsfct = NPropGuiFlt(NProp.pressure_motion_factor)
        self._gestures = NPropGuiBol(NProp.gestures)  # 303
        self._softareas = NPropGuiInt(NProp.softareas, 32)  # 307
        self._noise = NPropGuiInt(NProp.noise_cancellation, 32)  # 308

    def check_vars(self):  # {{{1
        # type: () -> bool
        f = False
        for k, v in self.__dict__.items():
            if not isinstance(v, NPropGui):
                continue
            info("{:3}-with {} args - {} gui {}".format(
                v.prop.prop_id, len(v.prop.vals), len(v.vars), v.prop.key))
            if len(v.vars) != len(v.prop.vals):
                f = True
        assert not f
        return f

    @classmethod
    def determine_devid(cls):  # cls {{{2
        # type: () -> int
        seq = common.check_output([cls.cmd_bin, "list"]).splitlines()
        seq = [s for s in seq if "touchpad" in s.lower()]
        if len(seq) < 1:
            return True
        curs = seq[0].strip()
        if "id=" not in curs:
            return True
        curs = curs[curs.find("id="):]
        curs = curs[3:]
        curs = curs.split("\t")[0]  # TODO: use regex for more robust operation
        ret = int(curs)
        return ret

    @classmethod
    def createpropsdb_defaults(cls):  # cls {{{2
        # type: () -> bool
        for name in dir(NProp):
            if name.startswith("_"):
                continue
            v = getattr(NProp, name)
            if not isinstance(v, int):
                continue
            cls.propsdb[name] = v
        return False

    @classmethod
    def createpropsdb(cls):  # cls {{{2
        # type: () -> bool
        if False:
            cls.createpropsdb_defaults()
        propnames = []
        for name in dir(NProp):
            if name.startswith("_"):
                continue
            propnames.append(name)
        n = 0
        cmd = [cls.cmd_bin, "list-props", str(cls.dev)]
        curs = common.check_output(cmd)
        for line in curs.splitlines():
            if "(" not in line:
                continue
            line = line.strip()
            # print("createdb: {}".format(line))
            n = line.index("(")
            name = line[:n]  # type: ignore  ## TODO: fix for python2
            line = line[n:]
            if ")" not in line:
                continue
            n = line.index(")")
            line = line[:n].strip("( )")
            # print("createdb: {}".format(line))
            if not line.isdigit():
                warn("createpropsdb: can't parse: " + line + "\n")
                continue
            prop = NProp.prop_get_by_key(name)
            if prop is None:
                warn("createpropsdb: can't parse: {} is not "
                     "the name of props".format(name))
                continue
            # print("{:20s}: {:3d}".format(name, int(line)))
            n += 1
            cls.propsdb[name] = int(line)
        return n < 1

    @classmethod
    def textprops(cls):  # cls {{{2
        # type: () -> str
        ret = ""
        for name in cls.propsdb:
            ret += "\n{:20s} = {:3d}".format(name, cls.propsdb[name])
        if len(ret) > 0:
            ret = ret[1:]
        return ret

    def prop_enum(self):  # {{{1
        # type: () -> Iterable[NPropGui]
        for k, v in self.__dict__.items():
            if not isinstance(v, NPropGui):
                continue
            yield v

    def prop_get(self, key):  # {{{1
        # type: (int) -> List[Text]
        curs = common.check_output(self.cmd_shw + [Text(self.dev)])
        for line in curs.splitlines():
            if "({}):".format(key) in line:
                curs = line
                break
        else:
            return []
        assert key > 0
        seq = curs.split(":")[1].split(",")
        return [i.strip() for i in seq]

    def prop_set_int(self, key, typ, seq):  # {{{1
        # type: (int, Text, List[Text]) -> bool
        cmd = self.cmd_int + [
                "--format=" + typ, Text(self.dev), Text(key)] + seq
        return self._callback(cmd)

    def prop_set_flt(self, key, seq):  # {{{1
        # type: (int, List[Text]) -> bool
        cmd = self.cmd_flt + [Text(self.dev), Text(key)] + seq
        return self._callback(cmd)

    def clks(self, i):  # {{{2
        # type: (int) -> int
        txt = self._clks.current(i)
        ret = int(txt)
        return ret

    def taps(self, i):  # {{{2
        # type: (int) -> int
        txt = self._taps.current(i)
        ret = int(txt)
        return ret

    def tapdurs(self, i):  # {{{2
        # type: (int) -> int
        txt = self._tapdurs.current(i)
        ret = int(txt)
        return ret

    def taptime(self):  # {{{2
        # type: () -> int
        txt = self._taptime.current(0)
        ret = int(txt)
        return ret

    def tapmove(self):  # {{{2
        # type: () -> int
        txt = self._tapmove.current(0)
        ret = int(txt)
        return ret

    def finger(self, i):  # {{{2
        # type: (int) -> int
        def limit(seq):  # TODO: add to NPropGui
            # type: (List[Text]) -> bool
            low = int(seq[0])
            hig = int(seq[1])
            return low < hig
        txt = self._finger.current(i)
        ret = int(txt)
        return ret

    def twofingerscroll(self, i):  # {{{2
        # type: (int) -> bool
        txt = self._twofingerscroll.current(i)
        ret = bool(txt)
        return ret

    def movespd(self, i):  # {{{2
        # type: (int) -> float
        txt = self._movespd.current(i)
        ret = float(txt)
        return ret

    def lckdrags(self):  # {{{2
        # type: () -> bool
        txt = self._lckdrags.current(0)
        ret = bool(txt)
        return ret

    def lckdragstimeout(self):  # {{{2
        # type: () -> int
        txt = self._lckdragstimeout.current(0)
        ret = int(float(txt))
        return ret

    def cirscr(self):  # {{{2
        # type: () -> bool
        txt = self._cirscr.current(0)
        ret = bool(txt)
        return ret

    def cirtrg(self):  # {{{2
        # type: () -> int
        def limit(seq):  # TODO: impl.
            # type: (List[Text]) -> bool
            cur = int(seq[0])
            return 0 <= cur <= 8
        txt = self._cirtrg.current(0)
        ret = int(float(txt))
        return ret

    def cirpad(self):  # {{{2
        # type: () -> bool
        txt = self._cirpad.current(0)
        ret = bool(txt)
        return ret

    def cirdis(self):  # {{{2
        # type: () -> float
        txt = self._cirdis.current(0)
        ret = float(txt)
        return ret

    def edges(self, i):  # {{{2
        # type: (int) -> int
        txt = self._edges.current(i)
        ret = int(txt)
        return ret

        """
        assert len(v) in (0, 4)
        n = NProp.edges
        prop = db.get(n)
        if len(v) > 0:
            pass
        elif prop.is_changed():
            pass
        return self.prop_i32(n, i, v)
        """

    def edgescrs(self, i):  # {{{2
        # type: (int) -> bool
        txt = self._edgescrs.current(i)
        ret = bool(txt)
        return ret

    def cstspd(self, i):  # {{{2
        # type: (int) -> float
        txt = self._cstspd.current(i)
        ret = float(txt)
        return ret

    def prsmot(self, i):  # {{{2
        # type: (int) -> int
        txt = self._prsmot.current(i)
        try:
            n = float(txt)
            ret = int(n)
        except ValueError:
            ret = 0
        return ret

    def prsfct(self, i):  # {{{2
        # type: (int) -> float
        prop = NProp.pressure_motion_factor
        if not prop.is_valid():
            return 0.0
        txt = self._prsfct.current(i)
        ret = float(txt)
        return ret

    def palmDetect(self):  # {{{2
        # type: () -> bool
        txt = self._palmDetect.current(0)
        ret = bool(txt)
        return ret

    def palmDims(self, i):  # {{{2
        # type: (int) -> int
        txt = self._palmDims.current(i)
        ret = int(txt)
        return ret

    def softareas(self, i):  # {{{2
        # type: (int) -> int
        txt = self._softareas.current(i)
        ret = int(txt)
        return ret

    def twoprs(self):  # {{{2
        # type: () -> int
        txt = self._twoprs.current(0)
        ret = int(txt)
        return ret

    def twowid(self):  # {{{2
        # type: () -> int
        txt = self._twowid.current(0)
        ret = int(txt)
        return ret

    def scrdist(self, i):  # {{{2
        # type: (int) -> int
        txt = self._scrdist.current(i)
        ret = int(txt)
        return ret

    def gestures(self):  # {{{2
        # type: () -> bool
        txt = self._gestures.current(0)
        ret = bool(txt)
        return ret

    def noise(self, i):  # {{{2
        # type: (int) -> int
        txt = self._noise.current(i)
        ret = int(txt)
        return ret

    def props(self):  # {{{2
        # type: () -> Tuple[List[bool], List[int]]
        cmd = [self.cmd_bin, self.cmd_wat, str(self.dev)]
        curs = common.check_output(cmd)

        _btns = {}  # type: Dict[int, bool]
        _vals = {}  # type: Dict[int, int]
        for line in curs.splitlines():
            line = line.strip()
            if line.startswith("button"):
                try:
                    l, r = line.split("=")
                    idx = int(line.split("[")[1].split("]")[0]) - 1
                    _btns[idx] = True if r == "down" else False
                except:
                    pass
                continue
            if line.startswith("valuator"):
                try:
                    l, r = line.split("=")
                    idx = int(line.split("[")[1].split("]")[0])
                    _vals[idx] = int(r)
                except:
                    pass
                continue
        btns = [_btns.get(i, False) for i in range(max(_btns.keys()) + 1)]
        vals = [_vals.get(i, 0) for i in range(max(_vals.keys()) + 1)]
        return btns, vals

    def apply(self, fn, f_changed):  # {{{1
        # type: (Callable[[List[Text]], bool], bool) -> bool
        info("-------- start apply() function -------------------------------")
        self._callback = fn

        for prop in self.prop_enum():
            if not f_changed:
                pass
            elif prop.prop.prop_id < 1:
                eror("did not found: {}-{}".format(
                        prop.prop.prop_id, prop.prop.key))
                continue
            elif not prop.is_changed():
                continue
            info("syncing {}...".format(prop.prop.prop_id))
            prop.sync()

        return False

    @classmethod  # apply_cmd # {{{1
    def apply_cmd(cls, cmd):
        # type: (List[Text]) -> bool
        if common.opts.fDryrun:
            return False
        info("command invoked: " + Text(cmd))
        ret = subprocess.call(cmd)
        if ret != 0:
            eror("ng: with: " + Text(cmd))
        else:
            warn("ok: with: " + Text(cmd))
        return False

    def dump(self):  # {{{2
        # type: () -> List[List[Text]]
        # from GUI.
        ret = []  # type: List[List[Text]]

        def apply_log(cmd):
            # type: (List[Text]) -> bool
            ret.append(cmd)
            return False

        self.apply(apply_log, False)
        return ret

    def dumpdb(self):  # {{{2
        # type: () -> NPropDb
        ret = NPropDb()

        def apply(cmd):
            # type: (List[Text]) -> bool
            prop = NProp.from_cmd(cmd)
            if prop is None:
                return False
            ret.put("xinput", prop)
            return False

        self.apply(apply, False)
        return ret

    def dumps(self):  # {{{2
        # type: () -> Text
        # from GUI.
        cmds = []  # type: List[List[Text]]

        def apply_log(cmd):
            # type: (List[Text]) -> bool
            cmds.append(cmd)
            return False

        self.apply(apply_log, False)

        ret = u""
        for line in cmds:
            ret += u'\n' + u' '.join(line)
        if len(ret) > 0:
            ret = ret[1:]

        return ret


# {{{1
xi = XInputDB()
cmdorg = []  # type: List[List[Text]]


# options {{{1
def options():  # {{{1
    # type: () -> Any
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--verbose', '-v', type=int, default=logging.WARNING,
                   choices=[logging.DEBUG, logging.INFO, logging.WARNING,
                            logging.ERROR, logging.CRITICAL, ])
    p.add_argument('--device-id', '-d', type=int, default=0)
    p.add_argument('--file-encoding', '-e', type=str, default="utf-8")
    p.add_argument('--dry-run', '-n', action="store_true")
    p.add_argument("-o", '--output', dest="fnameOut", type=str,
                   default="99-synaptics.conf")
    p.add_argument("-i", '--input', dest="fnameIn", type=str,
                   default="/usr/share/X11/xorg.conf.d/70-synaptics.conf")
    opts = p.parse_args()

    logging.getLogger().setLevel(opts.verbose)
    logging.getLogger().name = "touchpad"
    if opts.device_id == 0:
        ret = XInputDB.determine_devid()
        if ret is True:
            return None
        warn("synaptics was detected as {} device".format(ret))
        xi.dev = ret
    common.opts.fDryrun = opts.dry_run
    common.opts.file_encoding = opts.file_encoding
    common.opts.fnameIn = opts.fnameIn
    common.opts.fnameOut = opts.fnameOut
    return opts


# gui {{{1
class Gui(object):  # {{{1
    # {{{1
    # hint numbers {{{2
    hintnums = {}  # type: Dict[Text, int]

    def checkbox(self, parent, title, cur):  # {{{2
        # type: (tk.Widget, str, bool) -> BoolVar
        ret = draw.var_int()
        draw.set_int(ret, 1 if cur else 0)
        draw.chkbtn(parent, title, ret).pack(side=tk.LEFT)
        _ret = BoolVar(ret)
        return _ret

    def slider(self, parent, from_, to, cur):  # {{{2
        # type: (tk.Widget, int, int, int) -> IntVar
        ret = draw.var_int()
        draw.set_int(ret, cur)
        wid = draw.scale(parent, from_, to, tk.HORIZONTAL,
                         variable=ret)
        wid.pack(side=tk.LEFT)
        self.lastwid = wid
        _ret = IntVar(ret)
        return _ret

    def slider_flt(self, parent, from_, to, cur):  # {{{2
        # type: (tk.Widget, float, float, float) -> FltVar
        ret = FltVar(cur)
        draw.scale(parent, from_, to, tk.HORIZONTAL,
                   variable=ret.get_var(), resolution=0.01).pack(side=tk.LEFT)
        return ret

    def combobox(self, parent, seq, cur):  # {{{2
        # type: (tk.Widget, List[str], int) -> CmbVar
        ret = draw.cmbbox(parent, seq, cur)
        ret.pack(side=tk.LEFT)
        _ret = CmbVar(ret)
        return _ret

    def label2(self, parent, txt, prop, **kw):  # {{{2
        # type: (tk.Widget, str, NProp1, **Any) -> None
        if len(kw) < 1:
            kw["anchor"] = tk.W
        if "width" in kw:
            ret = draw.label(parent, txt, width=kw["width"])
            del kw["width"]
        else:
            ret = draw.label(parent, txt)
        ret.pack(**kw)
        draw.bind(ret, "<Button-1>", self.hint)
        _id = Text(repr(ret))
        self.hintnums[_id] = prop.prop_id

    def label3(self, parent, txt, prop, **kw):  # {{{2
        # type: (tk.Widget, str, NProp1, **Any) -> None
        if "side" not in kw:
            kw["side"] = tk.LEFT
        self.label2(parent, txt, prop, **kw)

    def hint(self, ev):  # {{{2
        # type: (tk.Event) -> None
        wid = getattr(ev, "widget")
        assert isinstance(wid, tk.Widget)
        _id = Text(repr(wid))
        if _id not in self.hintnums:
            return
        n = self.hintnums[_id]
        prop = NProp.prop_get(n)
        txt = prop.hint if prop is not None else ""
        txt = "property id:" + Text(n) + txt
        draw.text_delete(self.test, "1.0", tk.END)
        draw.text_insert(self.test, tk.END, txt)

    def callback_idle(self):  # {{{2
        # type: () -> None
        btns, vals = xi.props()
        draw.enty_delete(self.txt1, 0, tk.END)
        draw.enty_delete(self.txt2, 0, tk.END)
        draw.enty_delete(self.txt3, 0, tk.END)
        draw.enty_delete(self.txt4, 0, tk.END)
        draw.text_insert(self.txt1, 0, "{}".format(vals[0]))
        draw.text_insert(self.txt2, 0, "{}".format(vals[1]))
        draw.text_insert(self.txt3, 0, "{}".format(vals[2]))
        draw.text_insert(self.txt4, 0, "{}".format(vals[3]))
        _btns = ["black" if i else "white" for i in btns]
        gui_canvas(self.mouse, _btns, vals, [])
        self.root.after(100, self.callback_idle)  # type: ignore # for Tk

    def cmdfingerlow(self, ev):  # {{{2
        # type: (tk.Event) -> None
        vl = draw.scale_get(self.fingerlow)
        vh = draw.scale_get(self.fingerhig)
        if vl < vh:
            return
        draw.scale_set(self.fingerlow, vh - 1)

    def cmdfingerhig(self, ev):  # {{{2
        # type: (tk.Event) -> None
        vl = draw.scale_get(self.fingerlow)
        vh = draw.scale_get(self.fingerhig)
        if vl < vh:
            return
        draw.scale_set(self.fingerhig, vl + 1)

    def cmdrestore(self):  # {{{2
        # type: () -> None
        for cmd in cmdorg:
            warn("restore: " + str(cmd))
            subprocess.call(cmd)

    def cmdapply(self):  # {{{2
        # type: () -> None
        xi.apply(xi.apply_cmd, True)

    def cmdsave(self):  # {{{2
        # type: () -> None
        opts = common.opts
        xf = XConfFile()
        db = xf.read(opts.fnameIn)
        for n, p in xi.dumpdb().items("xinput"):
            try:
                prop = db.get("xinput", p)
                prop.update_by_prop(p)
            except KeyError:
                db.put("input", p)
        warn("output saved to {}".format(opts.fnameOut))
        xf.save(opts.fnameOut, opts.fnameIn, db)

    def cmdquit(self):  # {{{2
        # type: () -> None
        draw.root_quit(self.root)

    def cmdreport(self):  # {{{2
        # type: () -> None
        import sys
        import platform
        from datetime import datetime

        fname = datetime.now().strftime("report-%Y%m%d-%H%M%S.txt")
        fp = open_file(fname, "a")
        msg = common.check_output(["uname", "-a"])
        fp.write(msg + "\n")
        msg = common.check_output(["python3", "-m", "platform"])
        fp.write(msg + "\n")
        fp.write("Python: {}\n".format(str(sys.version_info)))
        if sys.version_info[0] == 2:
            sbld = platform.python_build()  # type: ignore
            scmp = platform.python_compiler()  # type: ignore
        else:
            sbld = platform.python_build()
            scmp = platform.python_compiler()
        fp.write("Python: {} {}\n".format(sbld, scmp))
        msg = common.check_output(["xinput", "list"])
        fp.write(msg + u"\n")
        msg = common.check_output(["xinput", "list-props", Text(xi.dev)])
        fp.write(msg + u"\n")
        fp.write(u"\n\n--- current settings (in app)---\n")
        fp.write(xi.dumps())
        fp.write(u"\n\n--- initial settings (at app startup)---")
        cmds = u""
        for i in cmdorg:
            cmds += u"\n" + u" ".join(i)
        fp.write(cmds + "\n")
        fp.close()

        msg = u"Report: {} was made,\n" \
              u"use this file to report a issue.".format(fname)
        messagebox.showinfo(u"Make a Report", msg)

    def __init__(self, root):  # {{{2
        # type: (tk.Tk) -> None
        self.root = root
        self.fingerlow = self.fingerhig = draw.scale(root)
        self.mouse = draw.canvas(root)
        self.test = draw.text(root)
        self.txt1 = self.txt2 = self.txt3 = self.txt4 = draw.entry(root)

        self.ex1 = self.ey1 = 0
        self.ex2 = self.ey2 = 0
        self.s1x1 = self.s1y1 = self.s1x2 = self.s1y2 = 0
        self.s2x1 = self.s2y1 = self.s2x2 = self.s2y2 = 0


def buildgui(opts):  # {{{1
    # type: (Any) -> Gui
    global cmdorg
    root = tk.Tk()
    gui = Gui(root)

    root.title("{}".format(
        os.path.splitext(os.path.basename(__file__))[0]))

    # 1st: pad, mouse and indicator {{{2
    frm1 = draw.frame(root, 5)

    ''' +--root--------------------+
        |+--frm1------------------+|
        ||+-frm11-+-mouse-+-frm13-+|
        |+--tab-------------------+|
        |+--frm3------------------+|
        +--------------------------+
    '''
    frm11 = draw.frame(frm1)
    gui.mouse = draw.canvas(frm1, _100, _100)
    frm13 = draw.frame(frm1)

    # gui_canvas(gui.mouse, ["white"] * 7, [0] * 4,
    #            [[xi.edges(i) for i in range(4)],
    #             [xi.softareas(i) for i in range(8)]])

    draw.label(frm11, "Information (update to click labels, "
               "can be used for scroll test)").pack(anchor=tk.W)
    gui.test = draw.text(frm11, 10)
    gui.test.pack(padx=5, pady=5, expand=True, fill="x")
    draw.text_insert(gui.test, tk.END,
                     "Test field\n\n  and click title labels to show "
                     "description of properties.")

    draw.label(frm13, "Current", width=7).pack(anchor=tk.W)
    gui.txt1 = draw.entry(frm13, 6)
    gui.txt1.pack()
    gui.txt2 = draw.entry(frm13, 6)
    gui.txt2.pack()
    gui.txt3 = draw.entry(frm13, 6)
    gui.txt3.pack()
    gui.txt4 = draw.entry(frm13, 6)
    gui.txt4.pack()

    gui.mouse.pack(side=tk.LEFT, anchor=tk.N)
    frm13.pack(side=tk.LEFT, anchor=tk.N)
    frm11.pack(side=tk.LEFT, anchor=tk.N, expand=True, fill="x")

    # 2nd: tab control
    nb = ttk.Notebook(root)  # type: ignore
    page1 = draw.frame(nb)
    nb.add(page1, text="Tap/Click")
    page4 = draw.frame(nb)
    nb.add(page4, text="Area")
    page2 = draw.frame(nb)
    nb.add(page2, text="Two-Fingers")
    page5 = draw.frame(nb)
    nb.add(page5, text="Misc.")
    page6 = draw.frame(nb)
    nb.add(page6, text="Information")
    page3 = draw.frame(nb)
    nb.add(page3, text="About")

    # 3rd: main button
    frm3 = draw.frame(root)

    btn3 = draw.button(frm3, "Quit", command=gui.cmdquit)
    btn3.pack(side=tk.RIGHT, padx=10)
    btn2 = draw.button(frm3, "Save", command=gui.cmdsave)
    btn2.pack(side=tk.RIGHT, padx=10)
    btn1 = draw.button(frm3, "Apply", command=gui.cmdapply)
    btn1.pack(side=tk.RIGHT, padx=10)
    btn0 = draw.button(frm3, "Restore", command=gui.cmdrestore)
    btn0.pack(side=tk.RIGHT, padx=10)

    frm1.pack(expand=1, fill="both")
    nb.pack(expand=1, fill="both")
    frm3.pack(expand=1, fill="both")

    # sub pages {{{2
    # page1 - basic {{{2
    # Click Action
    seq = (["Disabled", "Left-Click", "Middel-Click", "Right-Click"] +
           [str(i) for i in range(4, 10)])
    gui.label2(page1, "Click actions", NProp.click_action)
    frm = draw.frame(page1)
    frm.pack()
    draw.label(frm, "1-Finger").pack(side=tk.LEFT, padx=10)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(0)))
    draw.label(frm, "2-Finger").pack(side=tk.LEFT)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(1)))
    draw.label(frm, "3-Finger").pack(side=tk.LEFT)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(2)))

    # Tap Action
    gui.label2(page1, "Tap actions", NProp.tap_action)
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "RT", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(0)))
    draw.label(frm, "RB").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(1)))
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "LT", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(2)))
    draw.label(frm, "LB").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(3)))
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "1-Finger", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(4)))
    draw.label(frm, "2-Finger").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(5)))
    draw.label(frm, "3-Finger").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(6)))

    # Tap Threshold
    w = 10
    frm_ = draw.frame(page1)
    gui.label3(frm_, "FingerLow", NProp.finger, width=w)
    xi._finger.append(gui.slider(frm_, 1, 255, cur=xi.finger(0)))
    gui.fingerlow = gui.lastwid
    draw.bind(gui.lastwid, "<ButtonRelease-1>", gui.cmdfingerlow)
    # xii.fingerlow.pack(side=tk.LEFT, expand=True, fill="x")
    # frm_.pack(fill="x")
    # frm_ = draw.frame(page1)
    draw.label(frm_, "FingerHigh", width=10).pack(side=tk.LEFT)
    xi._finger.append(gui.slider(frm_, 1, 255, cur=xi.finger(1)))
    gui.fingerhig = gui.lastwid
    draw.bind(gui.lastwid, "<ButtonRelease-1>", gui.cmdfingerhig)
    # gui.fingerhig.pack(side=tk.LEFT, expand=True, fill="x")
    frm_.pack(fill="x", anchor=tk.W)
    v = IntVar(None)
    xi._finger.append(v)  # dummy

    frm = draw.frame(page1)
    gui.label3(frm, "Tap Time", NProp.tap_time, width=w)
    xi._taptime.append(gui.slider(frm, 1, 255, xi.taptime()))
    draw.label(frm, "Tap Move", width=10).pack(side=tk.LEFT)
    xi._tapmove.append(gui.slider(frm, 1, 255, xi.tapmove()))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page1)
    gui.label3(frm, "Tap Durations", NProp.tap_durations, width=w)
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(0)))
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(1)))
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(2)))
    frm.pack(anchor=tk.W)

    # page4 - Area {{{2
    frm = draw.frame(page4)
    gui.label3(frm, "Palm detect", NProp.palm_detection)
    xi._palmDetect.append(gui.checkbox(frm, "on", xi.palmDetect()))
    gui.label3(frm, "Palm dimensions", NProp.palm_dimensions)
    xi._palmDims.append(gui.slider(frm, 0, 3100, xi.palmDims(0)))
    xi._palmDims.append(gui.slider(frm, 0, 3100, xi.palmDims(1)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page4)
    gui.label3(frm, "Edge-x", NProp.edges)
    xi._edges.append(gui.slider(frm, 0, 3100, xi.edges(0)))
    xi._edges.append(gui.slider(frm, 0, 3100, xi.edges(1)))
    draw.label(frm, "Edge-y").pack(side=tk.LEFT)
    xi._edges.append(gui.slider(frm, 0, 1800, xi.edges(2)))
    xi._edges.append(gui.slider(frm, 0, 1800, xi.edges(3)))
    frm.pack(anchor=tk.W)

    gui.label2(page4, "Soft Button Areas "
               "(RB=Right Button, MB=Middle Button)", NProp.softareas,
               anchor=tk.W)
    frm = draw.frame(page4)
    draw.label(frm, "RB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(0)))
    draw.label(frm, "RB-Right", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(1)))
    draw.label(frm, "RB-Top", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(2)))
    draw.label(frm, "RB-Bottom", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(3)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page4)
    draw.label(frm, "MB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(4)))
    draw.label(frm, "MB-Right", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(5)))
    draw.label(frm, "MB-Top", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(6)))
    draw.label(frm, "MB-Bottom", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(7)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page4)
    gui.label3(frm, "Edge scroll", NProp.edgescrs)
    xi._edgescrs.append(gui.checkbox(frm, "Vert", xi.edgescrs(0)))
    xi._edgescrs.append(gui.checkbox(frm, "Horz", xi.edgescrs(1)))
    xi._edgescrs.append(gui.checkbox(frm, "Corner Coasting", xi.edgescrs(2)))
    frm.pack(anchor=tk.W)

    # page2 - two-fingers {{{2
    frm = draw.frame(page2)
    gui.label3(frm, "Two-Finger Scrolling", NProp.two_finger_scrolling)
    xi._twofingerscroll.append(
            gui.checkbox(frm, "Vert", xi.twofingerscroll(0)))
    xi._twofingerscroll.append(
            gui.checkbox(frm, "Horz", xi.twofingerscroll(1)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page2)
    gui.label3(frm, "Two-Finger Pressure", NProp.two_finger_pressure)
    xi._twoprs.append(gui.slider(frm, 1, 1000, xi.twoprs()))
    gui.label3(frm, "Two-Finger Width", NProp.two_finger_width)
    xi._twowid.append(gui.slider(frm, 1, 1000, xi.twowid()))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page2)
    gui.label3(frm, "Scrolling Distance", NProp.scrdist)
    xi._scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist(0)))
    xi._scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist(1)))
    frm.pack(anchor=tk.W)

    # page5 - Misc {{{2
    w = 13
    frm = draw.frame(page5)
    gui.label3(frm, "Noise Cancel (x-y)", NProp.noise_cancellation, width=w)
    xi._noise.append(gui.slider(frm, 1, 1000, xi.noise(0)))
    xi._noise.append(gui.slider(frm, 1, 1000, xi.noise(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Move speed", NProp.move_speed, width=w)
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(0)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(1)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(2)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(3)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Pressure Motion", NProp.pressure_motion, width=w)
    xi._prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot(0)))
    xi._prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot(1)))
    draw.label(frm, "Factor").pack(side=tk.LEFT)
    xi._prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct(0)))
    xi._prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Coasting speed", NProp.coasting_speed, width=w)
    xi._cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd(0)))
    xi._cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Locked Drags", NProp.locked_drags, width=w)
    xi._lckdrags.append(gui.checkbox(frm, "on", xi.lckdrags()))
    draw.label(frm, "timeout").pack(side=tk.LEFT)
    xi._lckdragstimeout.append(
            gui.slider(frm, 1, 100000, xi.lckdragstimeout()))
    xi._gestures.append(gui.checkbox(frm, "gesture", xi.gestures()))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Circular scrolling", NProp.cirscr, width=w)
    xi._cirscr.append(gui.checkbox(frm, "on", xi.cirscr()))
    xi._cirpad.append(gui.checkbox(frm, "Circular-pad", xi.cirpad()))
    gui.label3(frm, "  Distance", NProp.cirdis)
    xi._cirdis.append(gui.slider_flt(frm, 0.01, 100, xi.cirdis()))
    gui.label3(frm, "  Trigger", NProp.cirtrg)
    xi._cirtrg.append(gui.combobox(frm, ["0: All Edges",
                                         "1: Top Edge",
                                         "2: Top Right Corner",
                                         "3: Right Edge",
                                         "4: Bottom Right Corner",
                                         "5: Bottom Edge",
                                         "6: Bottom Left Corner",
                                         "7: Left Edge",
                                         "8: Top Left Corner"], xi.cirtrg()))
    frm.pack(anchor=tk.W)

    # page6 - Information {{{2
    frm = draw.frame(page6)
    draw.label(frm, "Capability", width=20).pack(side=tk.LEFT)
    draw.label(frm, "...").pack(side=tk.LEFT)
    frm.pack(anchor=tk.W)
    frm = draw.frame(page6)
    draw.label(frm, "Resolution [unit/mm]", width=20).pack(side=tk.LEFT)
    draw.label(frm, "...").pack(side=tk.LEFT)
    frm.pack(anchor=tk.W)
    frm = draw.frame(page6)
    draw.label(frm, "XInput2 Keywords", width=20).pack(side=tk.LEFT)
    txt = draw.text(frm, 3)
    draw.text_insert(txt, tk.END, XInputDB.textprops())
    txt.pack(side=tk.LEFT, fill="both", expand=True)
    frm.pack(anchor=tk.W)
    frm = draw.frame(page6)
    draw.label(frm, "Restore", width=20).pack(side=tk.LEFT)
    txt = draw.text(frm, 3)
    draw.text_insert(txt, tk.END, xi.dumps())
    txt.pack(side=tk.LEFT, fill="both", expand=True)
    frm.pack(anchor=tk.W)

    # page3 - About (License information) {{{2
    draw.label(page3, "TouchPad Tuner").pack()
    draw.label(page3, "Shimoda (kuri65536@hotmail.com)").pack()
    draw.label(page3, "License: Mozilla Public License 2.0").pack()
    draw.button(page3, "Make log for the report",  # TODO: align right
                command=gui.cmdreport).pack()  # .pack(anchor=tk.N)

    # pad.config(height=4)
    xi.check_vars()
    cmdorg = xi.dump()
    return gui


_100 = 150


def gui_scale(x, y):
    # type: (float, float) -> Tuple[int, int]
    rx = int(x) * _100 / 3192
    ry = int(y) * _100 / 1822
    return int(rx), int(ry)


def gui_softarea(seq):
    # type: (List[int]) -> Tuple[int, int, int, int]
    x1, y1 = seq[0], seq[2]
    x2, y2 = seq[1], seq[3]
    if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
        pass
    else:
        if x1 == 0:
            x1 = 0
        if y1 == 0:
            y1 = 0
        if x2 == 0:
            x2 = 3192
        if y2 == 0:
            y2 = 1822
    x1, y1 = gui_scale(x1, y1)
    x2, y2 = gui_scale(x2, y2)
    return x1, y1, x2, y2


def gui_canvas(inst, btns,  # {{{2
               vals, prms):
    # type: (tk.Canvas, List[str], List[int], List[List[int]]) -> None
    if gui is None:
        return
    _20 = 20
    _35 = 35
    _40 = 40
    _45 = 45
    _55 = 55
    _60 = 60
    _65 = 65
    _80 = 80

    draw.rectangle(inst, 0, 0, _100, _100, fill='white')  # ,stipple='gray25')
    if len(prms) > 0:
        edges = prms[0]
        gui.ex1, gui.ey1 = gui_scale(edges[0], edges[2])
        gui.ex2, gui.ey2 = gui_scale(edges[1], edges[3])
        # print("gui_canvas: edge: ({},{})-({},{})".format(x1, y1, x2, y2))
        areas = prms[1]
        gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2 = gui_softarea(areas[0:4])
        gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2 = gui_softarea(areas[4:8])
        debg("gui_canvas: RB: ({},{})-({},{})".format(
             gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2))
        debg("gui_canvas: MB: ({},{})-({},{})".format(
             gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2))

    if gui.s1x1 != gui.s1x2 and gui.s1y1 != gui.s1y2:
        draw.rectangle(inst, gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2,
                       fill="green")  # area for RB
    if gui.s2x1 != gui.s2x2 and gui.s2y1 != gui.s2y2:
        draw.rectangle(inst, gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2,
                       fill="blue")  # area for MB
    draw.rectangle(inst, gui.ex1, gui.ey1, gui.ex2, gui.ey2, width=2)

    # +-++++++-+
    # | |||||| |  (60 - 30) / 3 = 10
    draw.rectangle(inst, _20, _20, _80, _80, fill='white')
    draw.rectangle(inst, _35, _20, _45, _45, fill=btns[0])
    draw.rectangle(inst, _45, _20, _55, _45, fill=btns[1])
    draw.rectangle(inst, _55, _20, _65, _45, fill=btns[2])
    # inst.create_arc(_20, _20, _80, _40, style='arc', fill='white')
    # inst.create_line(_20, _40, _20, _80, _80, _80, _80, _40)
    draw.rectangle(inst, _40, _55, _60, _60, fill=btns[5])
    draw.rectangle(inst, _40, _60, _60, _65, fill=btns[6])

    x, y = gui_scale(vals[0], vals[1])
    draw.oval(inst, x - 2, y - 2, x + 2, y + 2, fill="black")
    x, y = gui_scale(vals[2], vals[3])
    x, y = x % _100, y % _100
    draw.oval(inst, x - 2, y - 2, x + 2, y + 2, fill="red")


# globals {{{1
gui = None  # type: Optional[Gui]


# main {{{1
def main():  # {{{1
    # type: () -> int
    logging.basicConfig(format="%(levelname)-8s:%(asctime)s:%(message)s")

    NProp.auto_id()
    global gui
    debg("fetch settings, options and arguments...")
    opts = options()
    if opts is None:
        eror("can't found Synaptics in xinput.")
        return 1
    debg("create properties DB...")
    if XInputDB.createpropsdb():
        eror("can't found Synaptics properties in xinput.")
        return 2
    debg("build GUI...")
    gui = buildgui(opts)
    gui.root.after_idle(gui.callback_idle)  # type: ignore # for Tk
    debg("start gui...")
    gui.root.mainloop()  # type: ignore # for Tk
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
