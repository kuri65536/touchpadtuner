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
from common import (BoolVar, CmbVar, FltVar, GuiVar, IntVar,
                    open_file, )
from xprops import NProp
from xprops2 import NPropDb
from xconf import XConfFile
import wraptk as draw

try:
    from typing import (Any, Callable, Dict, IO, Iterable, List, Optional,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, Iterable, List, Optional, Text, Tuple, Union
    GuiVar
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
        # type: (NProp) -> None
        self.prop = prop
        self.typ = "32"
        self.vars = []  # type: List[GuiVar]
        self.sets = [""] * len(prop.vals)  # type: List[Text]
        self.limit = self.limit_noop

    def is_changed(self):  # {{{1
        # type: () -> bool
        mem = self.prop.vals + []  # copy
        for n, v in enumerate(self.sets):
            if len(v) < 1:
                continue
            mem[n] = v

        cur = self.compose()
        for a, b in zip(cur, mem):
            if not self.cmp(a, b):
                return True
        return False

    def compose(self):  # {{{1
        # type: () -> List[Text]
        ret = []
        for var in self.vars:
            n = var.get()
            ret.append(n)
        return ret

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        assert False, "must be override"

    def sync(self):  # {{{1
        # type: () -> bool
        args = self.compose()
        xi.prop_set_int(self.prop.prop_id, self.typ, args)
        self.update_sets(args)
        return False

    def update_sets(self, args):  # {{{1
        # type: (List[Text]) -> None
        for n, (a, b, c) in enumerate(zip(self.prop.vals, self.sets, args)):
            if len(b) < 1:
                if a != c:
                    self.sets[n] = c
            else:
                # if a == c:
                #     self.sets[n] = ""
                if b != c:
                    self.sets[n] = c

    def limit_noop(self, seq):  # {{{1
        # type: (List[Text]) -> bool
        return True


class NPropGuiInt(NPropGui):  # {{{1
    def __init__(self, prop, typ):  # {{{1
        # type: (NProp, int) -> None
        NPropGui.__init__(self, prop)
        self.typ = Text(typ)

    def append(self, var):  # {{{1
        # type: (IntVar) -> 'NPropGuiInt'
        self.vars.append(var)
        return self

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        return a == b

    def cache(self, idx):  # {{{1
        # type: (int) -> int
        assert idx < len(self.prop.vals)
        val = self.prop.vals[idx]
        assert val is not None
        ret = int(val)
        return ret


class NPropGuiFlt(NPropGui):   # {{{1
    def __init__(self, prop):  # {{{1
        # type: (NProp) -> None
        NPropGui.__init__(self, prop)
        self.typ = "float"

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
        xi.prop_set_flt(self.prop.prop_id, args)
        self.update_sets(args)
        return False

    def cache(self, idx):  # {{{1
        # type: (int) -> float
        if not self.prop.is_valid():
            return 0.0
        assert idx < len(self.prop.vals)
        val = self.prop.vals[idx]
        assert val is not None
        ret = float(val)
        return ret


class NPropGuiBol(NPropGui):   # {{{1
    def __init__(self, prop):  # {{{1
        # type: (NProp) -> None
        NPropGui.__init__(self, prop)
        self.typ = "8"

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

    def cache(self, idx):  # {{{1
        # type: (int) -> bool
        assert idx < len(self.prop.vals)
        val = self.prop.vals[idx]
        assert val is not None
        ret = bool(val)
        return ret


class NPropGuiCmb(NPropGui):   # {{{1
    def __init__(self, prop, typ):  # {{{1
        # type: (NProp, int) -> None
        NPropGui.__init__(self, prop)
        self.typ = Text(typ)

    def append(self, var):  # {{{1
        # type: (CmbVar) -> 'NPropGuiCmb'
        self.vars.append(var)
        return self

    def cmp(self, a, b):  # {{{1
        # type: (Text, Text) -> bool
        return a == b

    def cache(self, idx):  # {{{1
        # type: (int) -> int
        assert idx < len(self.prop.vals)
        val = self.prop.vals[idx]
        assert val is not None
        ret = int(val)
        return ret


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
        NPropDb.auto_id()
        self._callback = apply_none  # type: Callable[[List[Text]], bool]

        _ = NPropDb
        self.edges = NPropGuiInt(_.edges, 32)  # 274
        self.finger = NPropGuiInt(_.finger, 32)  # 275
        self.taptime = NPropGuiInt(_.tap_time, 32)  # 276
        self.tapmove = NPropGuiInt(_.tap_move, 32)  # 277
        self.tapdurs = NPropGuiInt(_.tap_durations, 32)  # 278
        self.twoprs = NPropGuiInt(_.two_finger_pressure, 32)  # 281
        self.twowid = NPropGuiInt(_.two_finger_width, 32)  # 282
        self.scrdist = NPropGuiInt(_.scrdist, 32)  # 283
        self.edgescrs = NPropGuiBol(_.edgescrs)  # 284
        self.twoscr = NPropGuiBol(_.two_finger_scrolling)
        self.movespd = NPropGuiFlt(_.move_speed)  # 286
        self.lckdrags = NPropGuiBol(_.locked_drags)  # 288
        self.lckdrgto = NPropGuiInt(_.locked_drags_timeout, 32)
        self.taps = NPropGuiCmb(_.tap_action, 8)  # 290
        self.clks = NPropGuiCmb(_.click_action, 8)  # 291
        self.cirscr = NPropGuiBol(_.cirscr)  # 292
        self.cirdis = NPropGuiFlt(_.cirdis)  # 293
        self.cirtrg = NPropGuiCmb(_.cirtrg, 8)  # 294
        self.cirpad = NPropGuiBol(_.cirpad)  # 295
        self.palmdet = NPropGuiBol(_.palm_detection)  # 296
        self.palmdim = NPropGuiInt(_.palm_dimensions, 32)  # 297
        self.cstspd = NPropGuiFlt(_.coasting_speed)  # 298
        self.prsmot = NPropGuiInt(_.pressure_motion, 32)  # 299 ???
        self.prsfct = NPropGuiFlt(_.pressure_motion_factor)
        self.gestures = NPropGuiBol(_.gestures)  # 303
        self.softareas = NPropGuiInt(_.softareas, 32)  # 307
        self.noise = NPropGuiInt(_.noise_cancellation, 32)  # 308

        def limit(seq):
            # type: (List[Text]) -> bool
            low = int(seq[0])
            hig = int(seq[1])
            return low < hig

        self.finger.limit = limit

        def limit8(seq):
            # type: (List[Text]) -> bool
            cur = int(seq[0])
            return 0 <= cur <= 8

        self.cirtrg.limit = limit

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

    def propgui_enum(self):  # {{{1
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

        for pgui in self.propgui_enum():
            prop = pgui.prop
            if not f_changed:
                pass
            elif prop.prop_id < 1:
                eror("did not found: {}-{}".format(
                        prop.prop_id, prop.key))
                continue
            elif not pgui.is_changed():
                continue
            info("syncing {}...".format(prop.prop_id))
            pgui.sync()

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
    wid2prop = {}  # type: Dict[Text, NProp]

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
        # type: (tk.Widget, str, NProp, **Any) -> None
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
        self.wid2prop[_id] = prop

    def label3(self, parent, txt, prop, **kw):  # {{{2
        # type: (tk.Widget, str, NProp, **Any) -> None
        if "side" not in kw:
            kw["side"] = tk.LEFT
        self.label2(parent, txt, prop, **kw)

    def hint(self, ev):  # {{{2
        # type: (tk.Event) -> None
        wid = getattr(ev, "widget")
        assert isinstance(wid, tk.Widget)
        _id = Text(repr(wid))
        prop = self.wid2prop.get(_id, None)
        txt = ""
        if prop is not None:
            txt = "property id:" + Text(prop.prop_id) + prop.hint
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
        sec = opts.xsection
        xf = XConfFile()
        db = xf.read(opts.fnameIn)
        for name, p in NProp.props():
            try:
                prop = db.get(sec, p)
                prop.update_by_prop(p)
            except KeyError:
                # TODO(shimoda): check default...
                db.put(sec, p)
        for n, p in xi.dumpdb().items(sec):
            try:
                prop = db.get(sec, p)
                prop.update_by_prop(p)
            except KeyError:
                db.put(sec, p)
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
    #            [[xi.dges(i) for i in range(4)],
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
    gui.label2(page1, "Click actions", NPropDb.click_action)
    frm = draw.frame(page1)
    frm.pack()
    draw.label(frm, "1-Finger").pack(side=tk.LEFT, padx=10)
    xi.clks.append(gui.combobox(frm, seq, xi.clks.cache(0)))
    draw.label(frm, "2-Finger").pack(side=tk.LEFT)
    xi.clks.append(gui.combobox(frm, seq, xi.clks.cache(1)))
    draw.label(frm, "3-Finger").pack(side=tk.LEFT)
    xi.clks.append(gui.combobox(frm, seq, xi.clks.cache(2)))

    # Tap Action
    gui.label2(page1, "Tap actions", NPropDb.tap_action)
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "RT", width=10).pack(side=tk.LEFT, padx=10)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(0)))
    draw.label(frm, "RB").pack(side=tk.LEFT)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(1)))
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "LT", width=10).pack(side=tk.LEFT, padx=10)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(2)))
    draw.label(frm, "LB").pack(side=tk.LEFT)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(3)))
    frm = draw.frame(page1)
    frm.pack(anchor=tk.W)
    draw.label(frm, "1-Finger", width=10).pack(side=tk.LEFT, padx=10)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(4)))
    draw.label(frm, "2-Finger").pack(side=tk.LEFT)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(5)))
    draw.label(frm, "3-Finger").pack(side=tk.LEFT)
    xi.taps.append(gui.combobox(frm, seq, xi.taps.cache(6)))

    # Tap Threshold
    w = 10
    frm_ = draw.frame(page1)
    gui.label3(frm_, "FingerLow", NPropDb.finger, width=w)
    xi.finger.append(gui.slider(frm_, 1, 255, cur=xi.finger.cache(0)))
    gui.fingerlow = gui.lastwid
    draw.bind(gui.lastwid, "<ButtonRelease-1>", gui.cmdfingerlow)
    # xii.fingerlow.pack(side=tk.LEFT, expand=True, fill="x")
    # frm_.pack(fill="x")
    # frm_ = draw.frame(page1)
    draw.label(frm_, "FingerHigh", width=10).pack(side=tk.LEFT)
    xi.finger.append(gui.slider(frm_, 1, 255, cur=xi.finger.cache(1)))
    gui.fingerhig = gui.lastwid
    draw.bind(gui.lastwid, "<ButtonRelease-1>", gui.cmdfingerhig)
    # gui.fingerhig.pack(side=tk.LEFT, expand=True, fill="x")
    frm_.pack(fill="x", anchor=tk.W)
    v = IntVar(draw.var_int())
    xi.finger.append(v)  # dummy

    frm = draw.frame(page1)
    gui.label3(frm, "Tap Time", NPropDb.tap_time, width=w)
    xi.taptime.append(gui.slider(frm, 1, 255, xi.taptime.cache(0)))
    draw.label(frm, "Tap Move", width=10).pack(side=tk.LEFT)
    xi.tapmove.append(gui.slider(frm, 1, 255, xi.tapmove.cache(0)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page1)
    gui.label3(frm, "Tap Durations", NPropDb.tap_durations, width=w)
    xi.tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs.cache(0)))
    xi.tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs.cache(1)))
    xi.tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs.cache(2)))
    frm.pack(anchor=tk.W)

    # page4 - Area {{{2
    frm = draw.frame(page4)
    gui.label3(frm, "Palm detect", NPropDb.palm_detection)
    xi.palmdet.append(gui.checkbox(frm, "on", xi.palmdet.cache(0)))
    gui.label3(frm, "Palm dimensions", NPropDb.palm_dimensions)
    xi.palmdim.append(gui.slider(frm, 0, 3100, xi.palmdim.cache(0)))
    xi.palmdim.append(gui.slider(frm, 0, 3100, xi.palmdim.cache(1)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page4)
    gui.label3(frm, "Edge-x", NPropDb.edges)
    xi.edges.append(gui.slider(frm, 0, 3100, xi.edges.cache(0)))
    xi.edges.append(gui.slider(frm, 0, 3100, xi.edges.cache(1)))
    draw.label(frm, "Edge-y").pack(side=tk.LEFT)
    xi.edges.append(gui.slider(frm, 0, 1800, xi.edges.cache(2)))
    xi.edges.append(gui.slider(frm, 0, 1800, xi.edges.cache(3)))
    frm.pack(anchor=tk.W)

    gui.label2(page4, "Soft Button Areas "
               "(RB=Right Button, MB=Middle Button)", NPropDb.softareas,
               anchor=tk.W)
    frm = draw.frame(page4)
    draw.label(frm, "RB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(0)))
    draw.label(frm, "RB-Right", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(1)))
    draw.label(frm, "RB-Top", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(2)))
    draw.label(frm, "RB-Bottom", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(3)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page4)
    draw.label(frm, "MB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(4)))
    draw.label(frm, "MB-Right", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(5)))
    draw.label(frm, "MB-Top", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(6)))
    draw.label(frm, "MB-Bottom", width=10).pack(side=tk.LEFT)
    xi.softareas.append(gui.slider(frm, 0, 3100, xi.softareas.cache(7)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page4)
    gui.label3(frm, "Edge scroll", NPropDb.edgescrs)
    xi.edgescrs.append(gui.checkbox(frm, "Vert", xi.edgescrs.cache(0)))
    xi.edgescrs.append(gui.checkbox(frm, "Horz", xi.edgescrs.cache(1)))
    xi.edgescrs.append(gui.checkbox(frm, "Corner Coasting",
                                    xi.edgescrs.cache(2)))
    frm.pack(anchor=tk.W)

    # page2 - two-fingers {{{2
    frm = draw.frame(page2)
    gui.label3(frm, "Two-Finger Scrolling", NPropDb.two_finger_scrolling)
    xi.twoscr.append(gui.checkbox(frm, "Vert", xi.twoscr.cache(0)))
    xi.twoscr.append(gui.checkbox(frm, "Horz", xi.twoscr.cache(1)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page2)
    gui.label3(frm, "Two-Finger Pressure", NPropDb.two_finger_pressure)
    xi.twoprs.append(gui.slider(frm, 1, 1000, xi.twoprs.cache(0)))
    gui.label3(frm, "Two-Finger Width", NPropDb.two_finger_width)
    xi.twowid.append(gui.slider(frm, 1, 1000, xi.twowid.cache(0)))
    frm.pack(anchor=tk.W)

    frm = draw.frame(page2)
    gui.label3(frm, "Scrolling Distance", NPropDb.scrdist)
    xi.scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist.cache(0)))
    xi.scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist.cache(1)))
    frm.pack(anchor=tk.W)

    # page5 - Misc {{{2
    w = 13
    frm = draw.frame(page5)
    gui.label3(frm, "Noise Cancel (x-y)", NPropDb.noise_cancellation, width=w)
    xi.noise.append(gui.slider(frm, 1, 1000, xi.noise.cache(0)))
    xi.noise.append(gui.slider(frm, 1, 1000, xi.noise.cache(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Move speed", NPropDb.move_speed, width=w)
    xi.movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd.cache(0)))
    xi.movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd.cache(1)))
    xi.movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd.cache(2)))
    xi.movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd.cache(3)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Pressure Motion", NPropDb.pressure_motion, width=w)
    xi.prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot.cache(0)))
    xi.prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot.cache(1)))
    draw.label(frm, "Factor").pack(side=tk.LEFT)
    xi.prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct.cache(0)))
    xi.prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct.cache(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Coasting speed", NPropDb.coasting_speed, width=w)
    xi.cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd.cache(0)))
    xi.cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd.cache(1)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Locked Drags", NPropDb.locked_drags, width=w)
    xi.lckdrags.append(gui.checkbox(frm, "on", xi.lckdrags.cache(0)))
    draw.label(frm, "timeout").pack(side=tk.LEFT)
    xi.lckdrgto.append(gui.slider(frm, 1, 100000, xi.lckdrgto.cache(0)))
    xi.gestures.append(gui.checkbox(frm, "gesture", xi.gestures.cache(0)))
    frm.pack(anchor=tk.W)
    frm = draw.frame(page5)
    gui.label3(frm, "Circular scrolling", NPropDb.cirscr, width=w)
    xi.cirscr.append(gui.checkbox(frm, "on", xi.cirscr.cache(0)))
    xi.cirpad.append(gui.checkbox(frm, "Circular-pad", xi.cirpad.cache(0)))
    gui.label3(frm, "  Distance", NPropDb.cirdis)
    xi.cirdis.append(gui.slider_flt(frm, 0.01, 100, xi.cirdis.cache(0)))
    gui.label3(frm, "  Trigger", NPropDb.cirtrg)
    xi.cirtrg.append(gui.combobox(
        frm, ["0: All Edges", "1: Top Edge", "2: Top Right Corner",
              "3: Right Edge",
              "4: Bottom Right Corner", "5: Bottom Edge",
              "6: Bottom Left Corner",
              "7: Left Edge", "8: Top Left Corner"], xi.cirtrg.cache(0)))
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
    draw.text_insert(txt, tk.END, NPropDb.textprops())
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

    n_props = NPropDb.auto_id()
    global gui
    debg("fetch settings, options and arguments...")
    opts = options()
    if opts is None:
        eror("can't found Synaptics in xinput.")
        return 1
    debg("create properties DB...")
    if n_props < 3:
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
