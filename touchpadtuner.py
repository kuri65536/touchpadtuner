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
from typing import Any
import os

import tkinter as tk
from tkinter import Tk, ttk


# options {{{1
def options() -> Any:  # {{{1
    from argparse import ArgumentParser
    p = ArgumentParser()
    opts = p.parse_args()
    return opts


# gui {{{1
def buildgui(opts: Any) -> Tk:  # {{{1
    root = Tk()
    root.title("{}".format(
        os.path.splitext(os.path.basename(__file__))[0]))

    # 1st: pad, mouse and indicator
    frm = ttk.Frame(root)
    frm.pack(expand=1, fill="both")

    #
    frm2 = ttk.Frame(frm)
    frm2.pack(side=tk.LEFT)
    mouse = tk.Canvas(frm, width=100, height=100)
    mouse.pack(side=tk.LEFT)
    frm3 = ttk.Frame(frm)
    frm3.pack(side=tk.LEFT)

    pad = tk.Button(frm2)
    pad.pack()
    btn1 = tk.Button(frm2)
    btn1.pack(side=tk.LEFT)
    btn2 = tk.Button(frm2)
    btn2.pack(side=tk.LEFT)

    txt1 = tk.Text(frm3, height=1, width=10)
    txt1.pack()
    txt1 = tk.Text(frm3, height=1, width=10)
    txt1.pack()
    txt1 = tk.Text(frm3, height=1, width=10)
    txt1.pack()

    # 2nd: tab control
    frm = ttk.Frame(root)
    nb = ttk.Notebook(root)
    page1 = ttk.Frame(nb)
    nb.add(page1, text="Basic")
    page2 = ttk.Frame(nb)
    nb.add(page2, text="Detail")
    page3 = ttk.Frame(nb)
    nb.add(page3, text="About")
    nb.pack(expand=1, fill="both")

    # 3rd: main button
    frm = ttk.Frame(root)
    frm.pack(expand=1, fill="both")

    btn1 = tk.Button(frm, text="Save")
    btn1.pack(side=tk.LEFT)
    btn2 = tk.Button(frm, text="Quit")
    btn2.pack(side=tk.LEFT)

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

    # page1 - basic

    # page2 - detail

    # page3 - About (License information)
    tk.Label(page3, text="TouchPad Tuner").pack()
    tk.Label(page3, text="Shimoda (kuri65536@hotmail.com)").pack()
    tk.Label(page3, text="License: Modified BSD, 2017").pack()

    return root


# main {{{1
def main() -> int:  # {{{1
    opts = options()
    root = buildgui(opts)
    root.mainloop()
    return 0


if __name__ == "__main__":
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
