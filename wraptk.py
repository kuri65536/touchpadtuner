import sys
from typing import Any, Text, Union

if sys.version_info[0] == 3:
    import tkinter as tk
    import tkinter.messagebox as messagebox
    from tkinter import ttk
else:
    import Tkinter as tk
    # import ttk
    # import tkMessageBox as messagebox

if False:
    tk
    Any, Text, Union


def rectangle(inst, x1, y1, x2, y2, **kw):  # {{{1
    # type: (tk.Canvas, int, int, int, int, Any) -> None
    inst.create_rectangle(x1, y1, x2, y2, **kw)  # type: ignore # for Tk


def oval(inst, x1, y1, x2, y2, **kw):  # {{{1
    # type: (tk.Canvas, int, int, int, int, Any) -> None
    inst.create_oval(x1, y1, x2, y2, **kw)  # type: ignore # for Tk


def label(par, t, **kw):  # {{{1
    # type: (tk.Widget, Text, Any) -> tk.Widget
    return tk.Label(par, text=t, **kw)  # type: ignore # for Tk


def frame(par):  # {{{1
    # type: (Union[tk.Tk, tk.Widget]) -> tk.Frame
    return tk.Frame(par)  # type: ignore # for Tk


def button(par, t, **kw):  # {{{1
    # type: (tk.Widget, Text, Any) -> tk.Button
    return tk.Button(par, text=t, **kw)  # type: ignore # for Tk


def entry(par, *args):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], int) -> tk.Entry
    if len(args) > 0:
        return tk.Entry(par, width=args[0])  # type: ignore # for Tk
    return tk.Entry(par)  # type: ignore # for Tk


def text(par, *args):  # {{{1
    # type: (tk.Widget, int) -> tk.Entry
    if len(args) > 0:
        return tk.Text(par, height=args[0])  # type: ignore # for Tk
    return tk.Text(par)  # type: ignore # for Tk


def var_int():  # {{{1
    # type: () -> tk.IntVar
    return tk.IntVar()  # type: ignore # for Tk


# end of file {{{1
# vi: ft=python:et:fdm=marker:nowrap:tw=80
