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
from logging import info

import common
from common import (BoolVar, CmbVar, FltVar, IntVar,
                    open_file, )
from xprops import NProp, NPropDb
from xconf import XConfFile

try:
    from typing import (Any, Callable, Dict, IO, List, Optional,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, List, Optional, Text, Tuple, Union
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


class XInputDB(object):  # {{{1
    # {{{1
    dev = 11

    f_section = False
    n_section = 0
    cur_section = ""
    sections = {}  # type: Dict[int, Text]

    propsdb = {}  # type: Dict[str, int]
    cmd_bin = u"/usr/bin/xinput"
    cmd_shw = cmd_bin + u" list-props {} | grep '({}):'"
    cmd_int = u"set-int-prop"
    cmd_flt = u"set-float-prop"
    cmd_atm = cmd_bin + u" set-atomt-prop {} {} {} {}"

    cmd_wat = "query-state"

    def __init__(self):
        # type: () -> None
        def apply(cmd):
            # type: (List[Text]) -> bool
            return False

        self._callback = apply  # type: Callable[[List[Text]], bool]

        self.fDryrun = True
        self._palmDims = []  # type: List[IntVar]
        self._edges = []  # type: List[IntVar]
        self._edgescrs = []  # type: List[BoolVar]
        self._movespd = []  # type: List[FltVar]
        self._scrdist = []  # type: List[IntVar]
        self._tapdurs = []  # type: List[IntVar]
        self._cstspd = []  # type: List[FltVar]
        self._prsmot = []  # type: List[IntVar]
        self._prsfct = []  # type: List[FltVar]
        self._noise = []  # type: List[IntVar]
        self._softareas = []  # type: List[IntVar]
        self._finger = []  # type: List[IntVar]
        self._twofingerscroll = []  # type: List[BoolVar]
        self._clks = []  # type: List[CmbVar]
        self._taps = []  # type: List[CmbVar]
        self._taptime = IntVar(None)
        self._tapmove = IntVar(None)
        self._twoprs = IntVar(None)
        self._twowid = IntVar(None)
        self._lckdrags = BoolVar(None)
        self._lckdragstimeout = IntVar(None)
        self._cirscr = BoolVar(None)
        self._cirdis = FltVar(None)
        self._cirtrg = CmbVar(None)
        self._cirpad = BoolVar(None)
        self._palmDetect = BoolVar(None)
        self._gestures = BoolVar(None)

    @classmethod
    def determine_devid(cls):  # cls {{{2
        # type: () -> int
        cmd = cls.cmd_bin + u" list | grep -i TouchPad"
        curb = subprocess.check_output(cmd, shell=True)
        curs = curb.decode("utf-8").strip()
        if curs == "":
            return True
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
        curb = subprocess.check_output(cmd)
        curs = curb.decode("utf-8").strip()
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
                print("createprops: can't parse: " + line + "\n")
                continue
            name = name.strip("( ").lower()
            name = name.replace(" ", "_")
            name = name.replace("-", "_")
            if name.startswith("synaptics_"):
                name = name[10:]
            if name not in propnames:  # cls.propsdb:
                print("createprops: can't parse: {} is not "
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

    def prop_get(self, key):  # {{{2
        # type: (int) -> List[Text]
        cmd = self.cmd_shw.format(self.dev, key)
        curb = subprocess.check_output(cmd, shell=True)
        curs = curb.decode("utf-8").strip()
        seq = curs.split(":")[1].split(",")
        return [i.strip() for i in seq]

    def prop_bool(self, key, idx,  # {{{2
                  v=[]):
        # type: (int, int, List[bool]) -> bool
        if len(v) > 0:
            seq = [u"1" if i else u"0" for i in v]
            cmd = [self.cmd_bin, self.cmd_int, Text(self.dev), Text(key), u"8"]
            info("prop_bool: {}".format(str(cmd + seq)))
            self._callback(cmd + seq)
        seq = self.prop_get(key)
        return True if seq[idx] == "1" else False

    def prop_int(self,  # {{{2
                 typ,  # type: Text
                 key,  # type: int
                 idx,  # type: int
                 v=[],  # type: List[int]
                 func=allok  # type: Callable[[List[Text]], bool]
                 ):
        # type: (...) -> int
        seq = [Text(i) for i in v]
        assert len(seq) == 0 or (len(seq) > 0 and len(seq) > idx)
        if len(v) < 1:
            pass
        elif func(seq):
            cmd = [self.cmd_bin, self.cmd_int, Text(self.dev),
                   Text(key), typ] + seq
            info("prop_i{}: ".format(typ) + Text(cmd))
            self._callback(cmd + seq)
        seq = self.prop_get(key)
        return int(seq[idx])

    def prop_i32(self,  # {{{2
                 key,  # type: int
                 idx,  # type: int
                 v,  # type: List[int]
                 func=allok  # type: Callable[[List[Text]], bool]
                 ):
        # type: (...) -> int
        return self.prop_int("32", key, idx, v, func)

    def prop_i8(self,  # {{{2
                key,  # type: int
                idx,  # type: int
                v,  # type: List[int]
                func=allok  # type: Callable[[List[Text]], bool]
                ):
        # type: (...) -> int
        return self.prop_int("8", key, idx, v, func)

    def prop_flt(self, key, idx, v=[], func=allok):  # {{{2
        # type: (int, int, List[float], Callable[[List[Text]], bool]) -> float
        seq = [Text("{:f}").format(i) for i in v]
        if len(v) < 1:
            pass
        elif func(seq):
            cmd = [self.cmd_bin, self.cmd_flt, str(self.dev),
                   str(key)]
            print("prop_flt: " + str(cmd + seq))
            self._callback(cmd + seq)
        seq = self.prop_get(key)
        return float(seq[idx])

    def clks(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        assert len(v) == 0 or len(v) == 3
        return self.prop_i8(NProp.click_action, i, v)

    def taps(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        assert len(v) == 0 or len(v) == 7
        return self.prop_i8(NProp.tap_action, i, v)

    def tapdurs(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        assert len(v) == 0 or len(v) == 3
        return self.prop_i32(NProp.tap_durations, i, v)

    def taptime(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        return self.prop_i32(NProp.tap_time, 0, [] if v is None else [v])

    def tapmove(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        return self.prop_i32(NProp.tap_move, 0, [] if v is None else [v])

    def finger(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        def limit(seq):
            # type: (List[Text]) -> bool
            low = int(seq[0])
            hig = int(seq[1])
            return low < hig
        return self.prop_i32(NProp.finger, i, v, limit)

    def twofingerscroll(self, i, v=[]):  # {{{2
        # type: (int, List[bool]) -> bool
        return self.prop_bool(NProp.two_finger_scrolling, i, v)

    def movespd(self, i, v=[]):  # {{{2
        # type: (int, List[float]) -> float
        return self.prop_flt(NProp.move_speed, i, v)

    def lckdrags(self, v=None):  # {{{2
        # type: (Optional[bool]) -> bool
        return self.prop_bool(NProp.locked_drags, 0, [] if v is None else [v])

    def lckdragstimeout(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        return self.prop_i32(NProp.locked_drags_timeout, 0,
                             [] if v is None else [v])

    def cirscr(self, v=None):  # {{{2
        # type: (Optional[bool]) -> bool
        return self.prop_bool(NProp.circular_scrolling, 0,
                              [] if v is None else [v])

    def cirtrg(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        def limit(seq):
            # type: (List[Text]) -> bool
            cur = int(seq[0])
            return 0 <= cur <= 8
        return self.prop_i8(NProp.circular_scrolling_trigger, 0,
                            [] if v is None else [v], limit)

    def cirpad(self, v=None):  # {{{2
        # type: (Optional[bool]) -> bool
        return self.prop_bool(NProp.circular_pad, 0, [] if v is None else [v])

    def cirdis(self, v=None):  # {{{2
        # type: (Optional[float]) -> float
        return self.prop_flt(NProp.circular_scrolling_distance, 0,
                             [] if v is None else [v])

    def edges(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.edges, i, v)

    def edgescrs(self, i, v=[]):  # {{{2
        # type: (int, List[bool]) -> bool
        return self.prop_bool(NProp.edge_scrolling, i, v)

    def cstspd(self, i, v=[]):  # {{{2
        # type: (int, List[float]) -> float
        return self.prop_flt(NProp.coasting_speed, i, v)

    def prsmot(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.pressure_motion, i, v)

    def prsfct(self, i, v=[]):  # {{{2
        # type: (int, List[float]) -> float
        return self.prop_flt(NProp.pressure_motion_factor, i, v)

    def palmDetect(self, v=None):  # {{{2
        # type: (Optional[bool]) -> bool
        return self.prop_bool(NProp.palm_detection, 0,
                              [] if v is None else [v])

    def palmDims(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.palm_dimensions, i, v)

    def softareas(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.soft_button_areas, i, v)

    def twoprs(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        return self.prop_i32(NProp.two_finger_pressure, 0,
                             [] if v is None else [v])

    def twowid(self, v=None):  # {{{2
        # type: (Optional[int]) -> int
        return self.prop_i32(NProp.two_finger_width, 0,
                             [] if v is None else [v])

    def scrdist(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.scrolling_distance, i, v)

    def gestures(self, v=None):  # {{{2
        # type: (Optional[bool]) -> bool
        return self.prop_bool(NProp.gestures, 0, [] if v is None else [v])

    def noise(self, i, v=[]):  # {{{2
        # type: (int, List[int]) -> int
        return self.prop_i32(NProp.noise_cancellation, i, v)

    def props(self):  # {{{2
        # type: () -> Tuple[List[bool], List[int]]
        cmd = [self.cmd_bin, self.cmd_wat, str(self.dev)]
        curb = subprocess.check_output(cmd)
        curs = curb.decode("utf-8")

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

    def apply(self, fn):  # {{{1
        # type: (Callable[[List[Text]], bool]) -> bool
        self._callback = fn

        self.edges(0, [self._edges[i].get() for i in range(4)])  # 274
        self.finger(0, [self._finger[i].get() for i in range(3)])  # 275
        self.taptime(xi._taptime.get())  # 276
        self.tapmove(xi._tapmove.get())  # 277
        self.tapdurs(0, [self._tapdurs[i].get() for i in range(3)])  # 278
        self.twoprs(xi._twoprs.get())  # 281
        self.twowid(xi._twowid.get())  # 282
        self.scrdist(0, [self._scrdist[i].get() for i in range(2)])  # 283
        self.edgescrs(0, [self._edgescrs[i].get() for i in range(3)])  # 284
        self.twofingerscroll(0, [
            self._twofingerscroll[i].get() for i in range(2)])  # 285
        self.movespd(0, [self._movespd[i].get() for i in range(4)])  # 286
        self.lckdrags(self._lckdrags.get())  # 288
        self.lckdragstimeout(self._lckdragstimeout.get())  # 289
        self.clks(0, [self._clks[i].get() for i in range(3)])  # 290
        self.taps(0, [self._taps[i].get() for i in range(7)])  # 291
        self.cirscr(self._cirscr.get())  # 292
        self.cirdis(self._cirdis.get())  # 293
        self.cirtrg(self._cirtrg.get())  # 294
        self.cirpad(self._cirpad.get())  # 295
        self.palmDetect(self._palmDetect.get())  # 296
        self.palmDims(0, [self._palmDims[i].get() for i in range(2)])  # 297
        self.cstspd(0, [self._cstspd[i].get() for i in range(2)])  # 298
        # xi.prsmot(i, xi._prsmot[i].get())  # 299 TODO: ??? not work ???
        self.prsfct(0, [self._prsfct[i].get() for i in range(2)])  # 300
        self.gestures(self._gestures.get())  # 303
        self.softareas(0, [self._softareas[i].get() for i in range(8)])  # 307
        self.noise(0, [self._noise[i].get() for i in range(2)])  # 308
        return False

    def apply_cmd(self, cmd):  # {{{1
        # type: (List[Text]) -> bool
        if not self.fDryrun:
            subprocess.call(cmd)
        return False

    def dump(self):  # {{{2
        # type: () -> List[List[Text]]
        # from GUI.
        ret = []  # type: List[List[Text]]

        def apply(cmd):
            # type: (List[Text]) -> bool
            ret.append(cmd)
            return False

        self.apply(apply)
        return ret

    def dumpdb(self):  # {{{2
        # type: () -> NPropDb
        ret = NPropDb()

        def apply(cmd):
            # type: (List[Text]) -> bool
            prop = NProp.from_cmd(cmd)
            if prop is None:
                return False
            ret[prop.n] = prop
            return False

        self.apply(apply)
        return ret

    def dumps(self):  # {{{2
        # type: () -> Text
        # from GUI.
        cmds = []  # type: List[List[Text]]

        def apply(cmd):
            # type: (List[Text]) -> bool
            cmds.append(cmd)
            return False

        self.apply(apply)

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
    p.add_argument('--device-id', '-d', type=int, default=0)
    p.add_argument('--file-encoding', '-e', type=str, default="utf-8")
    p.add_argument("-o", '--output', dest="fnameOut", type=str,
                   default="99-synaptics.conf")
    p.add_argument("-i", '--input', dest="fnameIn", type=str,
                   default="/usr/share/X11/xorg.conf.d/70-synaptics.conf")
    opts = p.parse_args()

    if opts.device_id == 0:
        ret = XInputDB.determine_devid()
        if ret is True:
            return None
        print("synaptics was detected as {} device".format(ret))
        XInputDB.dev = ret
    common.opts.file_encoding = opts.file_encoding
    common.opts.fnameIn = opts.fnameIn
    common.opts.fnameOut = opts.fnameOut
    return opts


# gui {{{1
class Gui(object):  # {{{1
    def checkbox(self, parent, title, cur):  # {{{2
        # type: (tk.Widget, str, bool) -> BoolVar
        ret = tk.IntVar()
        ret.set(1 if cur else 0)
        tk.Checkbutton(parent, text=title,
                       variable=ret).pack(side=tk.LEFT)
        _ret = BoolVar(ret)
        return _ret

    def slider(self, parent, from_, to, cur):  # {{{2
        # type: (tk.Widget, int, int, int) -> IntVar
        ret = tk.IntVar()
        ret.set(cur)
        wid = tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL,
                       variable=ret)
        wid.pack(side=tk.LEFT)
        self.lastwid = wid
        _ret = IntVar(ret)
        return _ret

    def slider_flt(self, parent, from_, to, cur):  # {{{2
        # type: (tk.Widget, float, float, float) -> FltVar
        ret = tk.DoubleVar()
        ret.set(cur)
        tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL,
                 variable=ret, resolution=0.01).pack(side=tk.LEFT)
        _ret = FltVar(ret)
        return _ret

    def combobox(self, parent, seq, cur):  # {{{2
        # type: (tk.Widget, List[str], int) -> CmbVar
        ret = ttk.Combobox(parent, values=seq)
        ret.current(cur)
        ret.pack(side=tk.LEFT)
        _ret = CmbVar(ret)
        return _ret

    def label2(self, parent, txt, n, **kw):  # {{{2
        # type: (tk.Widget, str, int, **Any) -> None
        if len(kw) < 1:
            kw["anchor"] = tk.W
        if "width" in kw:
            ret = tk.Label(parent, text=txt, width=kw["width"])
            del kw["width"]
        else:
            ret = tk.Label(parent, text=txt)
        ret.pack(**kw)
        ret.bind("<Button-1>", self.hint)
        _id = Text(repr(ret))
        NProp.hintnums[_id] = n

    def label3(self, parent, txt, n, **kw):  # {{{2
        # type: (tk.Widget, str, int, **Any) -> None
        if "side" not in kw:
            kw["side"] = tk.LEFT
        self.label2(parent, txt, n, **kw)

    def hint(self, ev):  # {{{2
        # type: (tk.Event) -> None
        wid = getattr(ev, "widget")
        assert isinstance(wid, tk.Widget)
        _id = Text(repr(wid))
        if _id not in NProp.hintnums:
            return
        txt = NProp.hinttext[NProp.hintnums[_id]]
        self.test.delete(1.0, tk.END)
        self.test.insert(tk.END, txt)

    def callback_idle(self):  # {{{2
        # type: () -> None
        btns, vals = xi.props()
        self.txt1.delete(0, tk.END)
        self.txt2.delete(0, tk.END)
        self.txt3.delete(0, tk.END)
        self.txt4.delete(0, tk.END)
        self.txt1.insert(0, "{}".format(vals[0]))
        self.txt2.insert(0, "{}".format(vals[1]))
        self.txt3.insert(0, "{}".format(vals[2]))
        self.txt4.insert(0, "{}".format(vals[3]))
        _btns = ["black" if i else "white" for i in btns]
        gui_canvas(self.mouse, _btns, vals, [])
        self.root.after(100, self.callback_idle)

    def cmdfingerlow(self, ev):  # {{{2
        # type: (tk.Event) -> None
        vl = self.fingerlow.get()
        vh = self.fingerhig.get()
        if vl < vh:
            return
        self.fingerlow.set(vh - 1)

    def cmdfingerhig(self, ev):  # {{{2
        # type: (tk.Event) -> None
        vl = self.fingerlow.get()
        vh = self.fingerhig.get()
        if vl < vh:
            return
        self.fingerhig.set(vl + 1)

    def cmdrestore(self):  # {{{2
        # type: () -> None
        for cmd in cmdorg:
            print("restore: " + str(cmd))
            subprocess.call(cmd)

    def cmdapply(self):  # {{{2
        # type: () -> None
        xi.apply(xi. apply_cmd)

    def cmdsave(self):  # {{{2
        # type: () -> None
        opts = common.opts
        xf = XConfFile()
        db = xf.read(opts.fnameIn)
        for n, p in xi.dumpdb().items():
            prop = db[n]
            prop.update(p)
        xf.save(opts.fnameOut, opts.fnameIn, db)

    def cmdquit(self):  # {{{2
        # type: () -> None
        self.root.quit()

    def cmdreport(self):  # {{{2
        # type: () -> None
        import sys
        import platform
        from datetime import datetime

        opts = common.opts
        fname = datetime.now().strftime("report-%Y%m%d-%H%M%S.txt")
        enc = opts.file_encoding
        fp = open_file(fname, "a")
        bs = subprocess.check_output("uname -a", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + "\n")
        bs = subprocess.check_output("python3 -m platform", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + "\n")
        fp.write("Python: {}\n".format(str(sys.version_info)))
        if sys.version_info[0] == 2:
            sbld = platform.python_build()  # type: ignore
            scmp = platform.python_compiler()  # type: ignore
        else:
            sbld = platform.python_build()
            scmp = platform.python_compiler()
        fp.write("Python: {} {}\n".format(sbld, scmp))
        bs = subprocess.check_output("xinput list", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + u"\n")
        bs = subprocess.check_output("xinput list-props {}".format(
            XInputDB.dev), shell=True)
        msg = bs.decode(enc)
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
        self.fingerlow = self.fingerhig = tk.Scale(root)
        self.mouse = tk.Canvas(root)
        self.test = tk.Text(root)
        self.txt1 = self.txt2 = self.txt3 = self.txt4 = tk.Entry(root)

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
    frm1 = tk.Frame(root, height=5)

    ''' +--root--------------------+
        |+--frm1------------------+|
        ||+-frm11-+-mouse-+-frm13-+|
        |+--tab-------------------+|
        |+--frm3------------------+|
        +--------------------------+
    '''
    frm11 = tk.Frame(frm1)
    gui.mouse = tk.Canvas(frm1, width=_100, height=_100)
    frm13 = tk.Frame(frm1)

    gui_canvas(gui.mouse, ["white"] * 7, [0] * 4,
               [[xi.edges(i) for i in range(4)],
                [xi.softareas(i) for i in range(8)]])

    tk.Label(frm11, text="Information (update to click labels, "
                         "can be used for scroll test)").pack(anchor=tk.W)
    gui.test = tk.Text(frm11, height=10)
    gui.test.pack(padx=5, pady=5, expand=True, fill="x")
    gui.test.insert(tk.END, "Test field\n\n  and click title labels to show "
                    "description of properties.")

    tk.Label(frm13, text="Current", width=7).pack(anchor=tk.W)
    gui.txt1 = tk.Entry(frm13, width=6)
    gui.txt1.pack()
    gui.txt2 = tk.Entry(frm13, width=6)
    gui.txt2.pack()
    gui.txt3 = tk.Entry(frm13, width=6)
    gui.txt3.pack()
    gui.txt4 = tk.Entry(frm13, width=6)
    gui.txt4.pack()

    gui.mouse.pack(side=tk.LEFT, anchor=tk.N)
    frm13.pack(side=tk.LEFT, anchor=tk.N)
    frm11.pack(side=tk.LEFT, anchor=tk.N, expand=True, fill="x")

    # 2nd: tab control
    nb = ttk.Notebook(root)
    page1 = tk.Frame(nb)
    nb.add(page1, text="Tap/Click")
    page4 = tk.Frame(nb)
    nb.add(page4, text="Area")
    page2 = tk.Frame(nb)
    nb.add(page2, text="Two-Fingers")
    page5 = tk.Frame(nb)
    nb.add(page5, text="Misc.")
    page6 = tk.Frame(nb)
    nb.add(page6, text="Information")
    page3 = tk.Frame(nb)
    nb.add(page3, text="About")

    # 3rd: main button
    frm3 = tk.Frame(root)

    btn3 = tk.Button(frm3, text="Quit", command=gui.cmdquit)
    btn3.pack(side=tk.RIGHT, padx=10)
    btn2 = tk.Button(frm3, text="Save", command=gui.cmdsave)
    btn2.pack(side=tk.RIGHT, padx=10)
    btn1 = tk.Button(frm3, text="Apply", command=gui.cmdapply)
    btn1.pack(side=tk.RIGHT, padx=10)
    btn0 = tk.Button(frm3, text="Restore", command=gui.cmdrestore)
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
    frm = tk.Frame(page1)
    frm.pack()
    tk.Label(frm, text="1-Finger").pack(side=tk.LEFT, padx=10)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(0)))
    tk.Label(frm, text="2-Finger").pack(side=tk.LEFT)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(1)))
    tk.Label(frm, text="3-Finger").pack(side=tk.LEFT)
    xi._clks.append(gui.combobox(frm, seq, xi.clks(2)))

    # Tap Action
    gui.label2(page1, "Tap actions", NProp.tap_action)
    frm = tk.Frame(page1)
    frm.pack(anchor=tk.W)
    tk.Label(frm, text="RT", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(0)))
    tk.Label(frm, text="RB").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(1)))
    frm = tk.Frame(page1)
    frm.pack(anchor=tk.W)
    tk.Label(frm, text="LT", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(2)))
    tk.Label(frm, text="LB").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(3)))
    frm = tk.Frame(page1)
    frm.pack(anchor=tk.W)
    tk.Label(frm, text="1-Finger", width=10).pack(side=tk.LEFT, padx=10)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(4)))
    tk.Label(frm, text="2-Finger").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(5)))
    tk.Label(frm, text="3-Finger").pack(side=tk.LEFT)
    xi._taps.append(gui.combobox(frm, seq, xi.taps(6)))

    # Tap Threshold
    w = 10
    frm_ = tk.Frame(page1)
    gui.label3(frm_, "FingerLow", NProp.finger, width=w)
    xi._finger.append(gui.slider(frm_, 1, 255, cur=xi.finger(0)))
    gui.fingerlow = gui.lastwid
    gui.lastwid.bind("<ButtonRelease-1>", gui.cmdfingerlow)
    # xii.fingerlow.pack(side=tk.LEFT, expand=True, fill="x")
    # frm_.pack(fill="x")
    # frm_ = tk.Frame(page1)
    tk.Label(frm_, text="FingerHigh", width=10).pack(side=tk.LEFT)
    xi._finger.append(gui.slider(frm_, 1, 255, cur=xi.finger(1)))
    gui.fingerhig = gui.lastwid
    gui.lastwid.bind("<ButtonRelease-1>", gui.cmdfingerhig)
    # gui.fingerhig.pack(side=tk.LEFT, expand=True, fill="x")
    frm_.pack(fill="x", anchor=tk.W)
    v = IntVar(None)
    xi._finger.append(v)  # dummy

    frm = tk.Frame(page1)
    gui.label3(frm, "Tap Time", NProp.tap_time, width=w)
    xi._taptime = gui.slider(frm, 1, 255, xi.taptime())
    tk.Label(frm, text="Tap Move", width=10).pack(side=tk.LEFT)
    xi._tapmove = gui.slider(frm, 1, 255, xi.tapmove())
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page1)
    gui.label3(frm, "Tap Durations", NProp.tap_durations, width=w)
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(0)))
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(1)))
    xi._tapdurs.append(gui.slider(frm, 1, 255, xi.tapdurs(2)))
    frm.pack(anchor=tk.W)

    # page4 - Area {{{2
    frm = tk.Frame(page4)
    gui.label3(frm, "Palm detect", NProp.palm_detection)
    xi._palmDetect = gui.checkbox(frm, "on", xi.palmDetect())
    gui.label3(frm, "Palm dimensions", NProp.palm_dimensions)
    xi._palmDims.append(gui.slider(frm, 0, 3100, xi.palmDims(0)))
    xi._palmDims.append(gui.slider(frm, 0, 3100, xi.palmDims(1)))
    frm.pack(anchor=tk.W)

    frm = tk.Frame(page4)
    gui.label3(frm, "Edge-x", NProp.edges)
    xi._edges.append(gui.slider(frm, 0, 3100, xi.edges(0)))
    xi._edges.append(gui.slider(frm, 0, 3100, xi.edges(1)))
    tk.Label(frm, text="Edge-y").pack(side=tk.LEFT)
    xi._edges.append(gui.slider(frm, 0, 1800, xi.edges(2)))
    xi._edges.append(gui.slider(frm, 0, 1800, xi.edges(3)))
    frm.pack(anchor=tk.W)

    gui.label2(page4, "Soft Button Areas "
               "(RB=Right Button, MB=Middle Button)", NProp.soft_button_areas,
               anchor=tk.W)
    frm = tk.Frame(page4)
    tk.Label(frm, text="RB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(0)))
    tk.Label(frm, text="RB-Right", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(1)))
    tk.Label(frm, text="RB-Top", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(2)))
    tk.Label(frm, text="RB-Bottom", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(3)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page4)
    tk.Label(frm, text="MB-Left", width=10).pack(side=tk.LEFT, padx=10)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(4)))
    tk.Label(frm, text="MB-Right", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(5)))
    tk.Label(frm, text="MB-Top", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(6)))
    tk.Label(frm, text="MB-Bottom", width=10).pack(side=tk.LEFT)
    xi._softareas.append(gui.slider(frm, 0, 3100, xi.softareas(7)))
    frm.pack(anchor=tk.W)

    frm = tk.Frame(page4)
    gui.label3(frm, "Edge scroll", NProp.edge_scrolling)
    xi._edgescrs.append(gui.checkbox(frm, "Vert", xi.edgescrs(0)))
    xi._edgescrs.append(gui.checkbox(frm, "Horz", xi.edgescrs(1)))
    xi._edgescrs.append(gui.checkbox(frm, "Corner Coasting", xi.edgescrs(2)))
    frm.pack(anchor=tk.W)

    # page2 - two-fingers {{{2
    frm = tk.Frame(page2)
    gui.label3(frm, "Two-Finger Scrolling", NProp.two_finger_scrolling)
    xi._twofingerscroll.append(
            gui.checkbox(frm, "Vert", xi.twofingerscroll(0)))
    xi._twofingerscroll.append(
            gui.checkbox(frm, "Horz", xi.twofingerscroll(1)))
    frm.pack(anchor=tk.W)

    frm = tk.Frame(page2)
    gui.label3(frm, "Two-Finger Pressure", NProp.two_finger_pressure)
    xi._twoprs = gui.slider(frm, 1, 1000, xi.twoprs())
    gui.label3(frm, "Two-Finger Width", NProp.two_finger_width)
    xi._twowid = gui.slider(frm, 1, 1000, xi.twowid())
    frm.pack(anchor=tk.W)

    frm = tk.Frame(page2)
    gui.label3(frm, "Scrolling Distance", NProp.scrolling_distance)
    xi._scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist(0)))
    xi._scrdist.append(gui.slider(frm, 1, 1000, xi.scrdist(1)))
    frm.pack(anchor=tk.W)

    # page5 - Misc {{{2
    w = 13
    frm = tk.Frame(page5)
    gui.label3(frm, "Noise Cancel (x-y)", NProp.noise_cancellation, width=w)
    xi._noise.append(gui.slider(frm, 1, 1000, xi.noise(0)))
    xi._noise.append(gui.slider(frm, 1, 1000, xi.noise(1)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Move speed", NProp.move_speed, width=w)
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(0)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(1)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(2)))
    xi._movespd.append(gui.slider_flt(frm, 0, 10, xi.movespd(3)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Pressure Motion", NProp.pressure_motion, width=w)
    xi._prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot(0)))
    xi._prsmot.append(gui.slider(frm, 1, 1000, xi.prsmot(1)))
    tk.Label(frm, text="Factor").pack(side=tk.LEFT)
    xi._prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct(0)))
    xi._prsfct.append(gui.slider_flt(frm, 1, 1000, xi.prsfct(1)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Coasting speed", NProp.coasting_speed, width=w)
    xi._cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd(0)))
    xi._cstspd.append(gui.slider_flt(frm, 1, 1000, xi.cstspd(1)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Locked Drags", NProp.locked_drags, width=w)
    xi._lckdrags = gui.checkbox(frm, "on", xi.lckdrags())
    tk.Label(frm, text="timeout").pack(side=tk.LEFT)
    xi._lckdragstimeout = gui.slider(frm, 1, 100000, xi.lckdragstimeout())
    xi._gestures = gui.checkbox(frm, "gesture", xi.gestures())
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Circular scrolling", NProp.circular_scrolling, width=w)
    xi._cirscr = gui.checkbox(frm, "on", xi.cirscr())
    xi._cirpad = gui.checkbox(frm, "Circular-pad", xi.cirpad())
    gui.label3(frm, "  Distance", NProp.circular_scrolling_distance)
    xi._cirdis = gui.slider_flt(frm, 0.01, 100, xi.cirdis())
    gui.label3(frm, "  Trigger", NProp.circular_scrolling_trigger)
    xi._cirtrg = gui.combobox(frm, ["0: All Edges",
                                    "1: Top Edge",
                                    "2: Top Right Corner",
                                    "3: Right Edge",
                                    "4: Bottom Right Corner",
                                    "5: Bottom Edge",
                                    "6: Bottom Left Corner",
                                    "7: Left Edge",
                                    "8: Top Left Corner"], xi.cirtrg())
    frm.pack(anchor=tk.W)

    # page6 - Information {{{2
    frm = tk.Frame(page6)
    tk.Label(frm, text="Capability", width=20).pack(side=tk.LEFT)
    tk.Label(frm, text="...").pack(side=tk.LEFT)
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page6)
    tk.Label(frm, text="Resolution [unit/mm]", width=20).pack(side=tk.LEFT)
    tk.Label(frm, text="...").pack(side=tk.LEFT)
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page6)
    tk.Label(frm, text="XInput2 Keywords", width=20).pack(side=tk.LEFT)
    txt = tk.Text(frm, height=3)
    txt.insert(tk.END, XInputDB.textprops())
    txt.pack(side=tk.LEFT, fill="both", expand=True)
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page6)
    tk.Label(frm, text="Restore", width=20).pack(side=tk.LEFT)
    txt = tk.Text(frm, height=3)
    txt.insert(tk.END, xi.dumps())
    txt.pack(side=tk.LEFT, fill="both", expand=True)
    frm.pack(anchor=tk.W)

    # page3 - About (License information) {{{2
    tk.Label(page3, text="TouchPad Tuner").pack()
    tk.Label(page3, text="Shimoda (kuri65536@hotmail.com)").pack()
    tk.Label(page3, text="License: Mozilla Public License 2.0").pack()
    tk.Button(page3, text="Make log for the report",  # TODO: align right
              command=gui.cmdreport).pack()  # .pack(anchor=tk.N)

    # pad.config(height=4)
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

    inst.create_rectangle(0, 0, _100, _100, fill='white')  # ,stipple='gray25')
    if len(prms) > 0:
        edges = prms[0]
        gui.ex1, gui.ey1 = gui_scale(edges[0], edges[2])
        gui.ex2, gui.ey2 = gui_scale(edges[1], edges[3])
        # print("gui_canvas: edge: ({},{})-({},{})".format(x1, y1, x2, y2))
        areas = prms[1]
        gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2 = gui_softarea(areas[0:4])
        gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2 = gui_softarea(areas[4:8])
        print("gui_canvas: RB: ({},{})-({},{})".format(
              gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2))
        print("gui_canvas: MB: ({},{})-({},{})".format(
              gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2))

    if gui.s1x1 != gui.s1x2 and gui.s1y1 != gui.s1y2:
        inst.create_rectangle(gui.s1x1, gui.s1y1, gui.s1x2, gui.s1y2,
                              fill="green")  # area for RB
    if gui.s2x1 != gui.s2x2 and gui.s2y1 != gui.s2y2:
        inst.create_rectangle(gui.s2x1, gui.s2y1, gui.s2x2, gui.s2y2,
                              fill="blue")  # area for MB
    inst.create_rectangle(gui.ex1, gui.ey1, gui.ex2, gui.ey2,
                          width=2)

    # +-++++++-+
    # | |||||| |  (60 - 30) / 3 = 10
    inst.create_rectangle(_20, _20, _80, _80, fill='white')
    inst.create_rectangle(_35, _20, _45, _45, fill=btns[0])
    inst.create_rectangle(_45, _20, _55, _45, fill=btns[1])
    inst.create_rectangle(_55, _20, _65, _45, fill=btns[2])
    # inst.create_arc(_20, _20, _80, _40, style='arc', fill='white')
    # inst.create_line(_20, _40, _20, _80, _80, _80, _80, _40)
    inst.create_rectangle(_40, _55, _60, _60, fill=btns[5])
    inst.create_rectangle(_40, _60, _60, _65, fill=btns[6])

    x, y = gui_scale(vals[0], vals[1])
    inst.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
    x, y = gui_scale(vals[2], vals[3])
    x, y = x % _100, y % _100
    inst.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")


# globals {{{1
gui = None  # type: Optional[Gui]


# main {{{1
def main():  # {{{1
    # type: () -> int
    global gui
    opts = options()
    if opts is None:
        print("can't found Synaptics in xinput.")
        return 1
    if XInputDB.createpropsdb():
        print("can't found Synaptics properties in xinput.")
        return 2
    gui = buildgui(opts)
    gui.root.after_idle(gui.callback_idle)
    gui.root.mainloop()
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
