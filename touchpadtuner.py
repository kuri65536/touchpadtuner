#! env python3
'''License: Modified BSD
Copyright (c) 2017, shimoda as kuri65536 _dot_ hot mail _dot_ com
                    ( email address: convert _dot_ to . and joint string )

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the <ORGANIZATION> nor the names of its contributors
  may be used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
from typing import Any, Callable, List, Optional, Tuple
import os
import subprocess

import tkinter as tk
from tkinter import Tk, ttk


# xinput {{{1
class XInputDB(object):  # {{{1
    cmd_bin = "/usr/bin/xinput"
    cmd_shw = cmd_bin + " list-props {} | grep '({}):'"
    cmd_int = "set-int-prop"
    cmd_flt = cmd_bin + " set-float-prop {} {} {} {}"
    cmd_atm = cmd_bin + " set-atomt-prop {} {} {} {}"

    cmd_wat = "query-state"

    def __init__(self):
        self.dev = 11

    def prop_get(self, key) -> List[str]:  # {{{2
        cmd = self.cmd_shw.format(self.dev, key)
        curb = subprocess.check_output(cmd, shell=True)
        curs = curb.decode("utf-8").strip()
        seq = curs.split(":")[1].split(",")
        return [i.strip() for i in seq]

    def prop_bool(self, key: int, idx: int,  # {{{2
                  v: Optional[bool]=None) -> bool:
        seq = self.prop_get(key)
        if v is not None:
            seq[idx] = "1" if v else "0"
            cmd = [self.cmd_bin, self.cmd_int, str(self.dev), str(key), "8"]
            print("prop_bool: " + str(cmd + seq))
            subprocess.call(cmd + seq)
            seq = self.prop_get(key)
        return True if seq[idx] == "1" else False

    def prop_i32(self, key: int, idx: int,  # {{{2
                 v: Optional[int]=None,
                 func=Callable[[List[str]], bool]) -> bool:
        seq = self.prop_get(key)
        if v is not None:
            org = seq[idx]
            seq[idx] = "{}".format(v)
            if func(seq):
                cmd = [self.cmd_bin, self.cmd_int, str(self.dev),
                       str(key), "32"]
                print("prop_i32: " + str(cmd + seq))
                subprocess.call(cmd + seq)
                seq = self.prop_get(key)
            else:
                seq[idx] = org
        return int(seq[idx])

    def fingerlow(self, v: Optional[int]=None) -> int:  # {{{2
        def limit(seq: List[str]) -> bool:
            low = int(seq[0])
            hig = int(seq[1])
            return low < hig
        return self.prop_i32(275, 0, v, limit)

    def fingerhig(self, v: Optional[int]=None) -> int:  # {{{2
        def limit(seq: List[str]) -> bool:
            low = int(seq[0])
            hig = int(seq[1])
            return low > hig
        return self.prop_i32(275, 1, v, limit)

    def vert2fingerscroll(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(285, 0, v)

    def horz2fingerscroll(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(285, 1, v)

    def props(self) -> Tuple[List[bool], List[str]]:  # {{{2
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

    def fetch(self) -> 'XInputDB':  # {{{2
        self.db = {}
        self.db["fingerlow"] = self.fingerlow()
        self.db["fingerhig"] = self.fingerhig()
        self.db["vert2fingerscroll"] = self.vert2fingerscroll()
        self.db["horz2fingerscroll"] = self.horz2fingerscroll()
        return self

    def dump(self, fname: str, fnameIn: str) -> str:  # {{{2
        '''sample output {{{3
            # Example xorg.conf.d snippet that assigns the touchpad driver
            # to all touchpads. See xorg.conf.d(5) for more information on
            # InputClass.
            # DO NOT EDIT THIS FILE, your distribution will likely overwrite
            # it when updating. Copy (and rename) this file into
            # /etc/X11/xorg.conf.d first.
            # Additional options may be added in the form of
            #   Option "OptionName" "value"
            #
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
            # but cannot be
            # enabled by default. See the following link for details:
            # http://who-t.blogspot.com/2010/11/
            #                           how-to-ignore-configuration-errors.html
                  MatchDevicePath "/dev/input/event*"
            EndSection

            # This option enables the bottom right corner to be a right button
            # on clickpads
            # and the right and middle top areas to be right / middle buttons
            # on clickpads
            # with a top button area.
            # This option is only interpreted by clickpads.
            Section "InputClass"
                    Identifier "Default clickpad buttons"
                    MatchDriver "synaptics"
                    Option "SoftButtonAreas" "50% 0 82% 0 0 0 0 0"
                    Option "SecondarySoftButtonAreas"
                        "58% 0 0 15% 42% 58% 0 15%"
            EndSection }}}
        '''
        db = XInputDB.read(fname)
        db.merge(self)

        ret = ""
        ret += self.dump_line_int("FingerLow", db.fingerlow())
        ret += self.dump_line_int("FingerHigh", db.fingerhig())
        ret += self.dump_line_bool("VertTwoFingerScroll",
                                   db.vert2fingerscroll())
        ret += self.dump_line_bool("HorizTwoFingerScroll",
                                   db.horz2fingerscroll())
        return ret


# {{{2
xi = XInputDB()
xiorg = XInputDB().fetch()


# options {{{1
def options() -> Any:  # {{{1
    from argparse import ArgumentParser
    p = ArgumentParser()
    opts = p.parse_args()
    return opts


# gui {{{1
class Gui(object):  # {{{1
    def callback_idle(self):  # {{{2
        btns, vals = xi.props()
        self.txt1.delete(0, tk.END)
        self.txt2.delete(0, tk.END)
        self.txt3.delete(0, tk.END)
        self.txt4.delete(0, tk.END)
        self.txt1.insert(0, "{}".format(vals[0]))
        self.txt2.insert(0, "{}".format(vals[1]))
        self.txt3.insert(0, "{}".format(vals[2]))
        self.txt4.insert(0, "{}".format(vals[3]))
        self.root.after(100, self.callback_idle)

    def cmdfingerlow(self, ev: tk.Event) -> None:  # {{{2
        vl = self.fingerlow.get()
        vh = self.fingerhig.get()
        if vl < vh:
            return
        self.fingerlow.set(vh - 1)

    def cmdfingerhig(self, ev: tk.Event) -> None:  # {{{2
        vl = self.fingerlow.get()
        vh = self.fingerhig.get()
        if vl < vh:
            return
        self.fingerhig.set(vl + 1)

    def cmdrestore(self) -> None:  # {{{2
        xi.fingerlow(xiorg.db["fingerlow"])
        self.fingerlow.set(xiorg.db["fingerlow"])
        xi.fingerhig(xiorg.db["fingerhig"])
        self.fingerhig.set(xiorg.db["fingerhig"])

        xi._horz2fingerscroll.set(1 if xiorg.db["horz2fingerscroll"] else 0)
        xi._vert2fingerscroll.set(1 if xiorg.db["vert2fingerscroll"] else 0)

    def cmdapply(self) -> None:  # {{{2
        xi.fingerlow(self.fingerlow.get())
        xi.fingerhig(self.fingerhig.get())
        xi.horz2fingerscroll(xi._horz2fingerscroll.get() == 1)
        xi.vert2fingerscroll(xi._vert2fingerscroll.get() == 1)

    def cmdsave(self) -> None:  # {{{2
        xi.dump(opts.fnameOut, opts.fnameIn)

    def cmdquit(self) -> None:  # {{{2
        self.root.quit()


def buildgui(opts: Any) -> Tk:  # {{{1
    global gui
    gui = Gui()

    root = gui.root = Tk()
    root.title("{}".format(
        os.path.splitext(os.path.basename(__file__))[0]))

    # 1st: pad, mouse and indicator {{{2
    frm1 = ttk.Frame(root, height=5)

    ''' +--root--------------------+
        |+--frm1------------------+|
        ||+-frm11-+-mouse-+-frm13-+|
        |+--tab-------------------+|
        |+--frm3------------------+|
        +--------------------------+
    '''
    frm11 = ttk.Frame(frm1)
    mouse = tk.Canvas(frm1, width=200, height=200)
    frm13 = ttk.Frame(frm1)

    gui_canvas(mouse, ["white", "white", "white"])

    pad = tk.Button(frm11, width=23, height=4)
    pad.pack()
    btn1 = tk.Button(frm11, width=10)
    btn1.pack(side=tk.LEFT)
    btn2 = tk.Button(frm11, width=10)
    btn2.pack(side=tk.LEFT)

    gui.txt1 = tk.Entry(frm13, width=10)
    gui.txt1.pack()
    gui.txt2 = tk.Entry(frm13, width=10)
    gui.txt2.pack()
    gui.txt3 = tk.Entry(frm13, width=10)
    gui.txt3.pack()
    gui.txt4 = tk.Entry(frm13, width=10)
    gui.txt4.pack()

    frm11.pack(side=tk.LEFT, anchor=tk.N)
    mouse.pack(side=tk.LEFT, anchor=tk.N)
    frm13.pack(side=tk.LEFT, anchor=tk.N)

    # 2nd: tab control
    nb = ttk.Notebook(root)
    page1 = ttk.Frame(nb)
    nb.add(page1, text="Tap/Click")
    page2 = ttk.Frame(nb)
    nb.add(page2, text="Detail")
    page3 = ttk.Frame(nb)
    nb.add(page3, text="About")

    # 3rd: main button
    frm3 = ttk.Frame(root)

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
    '''xinput list-props 11
        Device 'ELAN1201:00 04F3:3054 Touchpad':
        Device Enabled (140):                     1
        Coordinate Transformation Matrix (142):   1.0, 0.0, 0.0,
                                                  0.0, 1.0, 0.0,
                                                  0.0, 0.0, 1.0
        Device Accel Profile (270):               1
        Device Accel Constant Deceleration (271): 2.500000
        Device Accel Adaptive Deceleration (272): 1.000000
        Device Accel Velocity Scaling (273):      12.500000
        Synaptics Edges (274):                    127, 3065, 98, 1726
        Synaptics Finger (275):                   50, 100, 0
        Synaptics Tap Time (276):                 180
        Synaptics Tap Move (277):                 161
        Synaptics Tap Durations (278):            180, 180, 100
        Synaptics ClickPad (279):                 1
        Synaptics Middle Button Timeout (280):    0
        Synaptics Two-Finger Pressure (281):      282
        Synaptics Two-Finger Width (282):         7
        Synaptics Scrolling Distance (283):       73, 73
        Synaptics Edge Scrolling (284):           1, 0, 0
        Synaptics Two-Finger Scrolling (285):     1, 1
        Synaptics Move Speed (286):               1.0, 1.75, 0.054407, 0.000000
        Synaptics Off (287):                      1
        Synaptics Locked Drags (288):             0
        Synaptics Locked Drags Timeout (289):     5000
        Synaptics Tap Action (290):               2, 3, 0, 0, 1, 3, 2
        Synaptics Click Action (291):             1, 3, 0
        Synaptics Circular Scrolling (292):       0
        Synaptics Circular Scrolling Distance (293): 0.100000
        Synaptics Circular Scrolling Trigger (294):  0
        Synaptics Circular Pad (295):             0
        Synaptics Palm Detection (296):           0
        Synaptics Palm Dimensions (297):          10, 200
        Synaptics Coasting Speed (298):           20.000000, 50.000000
        Synaptics Pressure Motion (299):          30, 160
        Synaptics Pressure Motion Factor (300):   1.000000, 1.000000
        Synaptics Resolution Detect (301):        1
        Synaptics Grab Event Device (302):        0
        Synaptics Gestures (303):                 1
        Synaptics Capabilities (304):             1, 0, 0, 1, 1, 0, 0
        Synaptics Pad Resolution (305):           31, 31
        Synaptics Area (306):                     0, 0, 0, 0
        Synaptics Soft Button Areas (307):        1596, 0, 1495, 0, 0, 0, 0, 0
        Synaptics Noise Cancellation (308):       18, 18
        Device Product ID (267):                  1267, 12372
        Device Node (266):                        "/dev/input/event8"
    '''

    # page1 - basic {{{2
    # Click Action
    seq = ["Left-Click", "Right-Click", "Middel-Click"]
    tk.Label(page1, text="Click actions").pack(anchor=tk.W)
    frm = tk.Frame(page1)
    frm.pack()
    tk.Label(frm, text="1-Finger").pack(side=tk.LEFT, padx=10)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)
    tk.Label(frm, text="2-Finger").pack(side=tk.LEFT)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)
    tk.Label(frm, text="3-Finger").pack(side=tk.LEFT)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)

    # Tap Action
    tk.Label(page1, text="Tap actions").pack(anchor=tk.W)
    frm = tk.Frame(page1)
    frm.pack()
    tk.Label(frm, text="1-Finger").pack(side=tk.LEFT, padx=10)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)
    tk.Label(frm, text="2-Finger").pack(side=tk.LEFT)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)
    tk.Label(frm, text="3-Finger").pack(side=tk.LEFT)
    ttk.Combobox(frm, values=seq).pack(side=tk.LEFT)

    # Tap Threshold
    frm_ = tk.Frame(page1)
    tk.Label(frm_, text="FingerLow").pack(side=tk.LEFT)
    gui.fingerlow = tk.Scale(frm_, from_=1, to=255, orient=tk.HORIZONTAL)
    gui.fingerlow.pack()
    frm_.pack()
    frm_ = tk.Frame(page1)
    tk.Label(frm_, text="FingerHigh").pack(side=tk.LEFT)
    gui.fingerhig = tk.Scale(frm_, from_=1, to=255, orient=tk.HORIZONTAL)
    gui.fingerhig.pack()
    frm_.pack()
    gui.fingerlow.set(xi.fingerlow())
    gui.fingerhig.set(xi.fingerhig())
    gui.fingerlow.bind("<ButtonRelease-1>", gui.cmdfingerlow)
    gui.fingerhig.bind("<ButtonRelease-1>", gui.cmdfingerhig)

    # page2 - detail {{{2
    xi._vert2fingerscroll = tk.IntVar()
    xi._horz2fingerscroll = tk.IntVar()
    xi._vert2fingerscroll.set(1 if xi.vert2fingerscroll() else 0)
    xi._horz2fingerscroll.set(1 if xi.vert2fingerscroll() else 0)
    tk.Checkbutton(page2, text="2-Finger Scroll(Vert)",
                   variable=xi._vert2fingerscroll).pack()
    tk.Checkbutton(page2, text="2-Finger Scroll(Horz)",
                   variable=xi._horz2fingerscroll).pack()

    # page3 - About (License information) {{{2
    tk.Label(page3, text="TouchPad Tuner").pack()
    tk.Label(page3, text="Shimoda (kuri65536@hotmail.com)").pack()
    tk.Label(page3, text="License: Modified BSD, 2017").pack()

    # pad.config(height=4)
    return root


def gui_canvas(inst: tk.Canvas, btns: List[str]) -> None:  # {{{2
    _20 = 20
    _35 = 35
    _45 = 45
    _55 = 55
    _65 = 65
    _80 = 80
    _100 = 100

    # +-++++++-+
    # | |||||| |  (60 - 30) / 3 = 10
    inst.create_rectangle(0, 0, _100, _100, fill='white')  # ,stipple='gray25')
    inst.create_rectangle(_20, _20, _80, _80, fill='white')
    inst.create_rectangle(_35, _20, _45, _45, fill=btns[0])
    inst.create_rectangle(_45, _20, _55, _45, fill=btns[1])
    inst.create_rectangle(_55, _20, _65, _45, fill=btns[2])
    # inst.create_arc(_20, _20, _80, _40, style='arc', fill='white')
    # inst.create_line(_20, _40, _20, _80, _80, _80, _80, _40)


# main {{{1
def main() -> int:  # {{{1
    global opts
    opts = options()
    root = buildgui(opts)
    root.after_idle(gui.callback_idle)
    root.mainloop()
    return 0


if __name__ == "__main__":
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
