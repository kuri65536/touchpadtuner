import sys
from typing import Any, Callable, List, Text, Union

if sys.version_info[0] == 3:
    import tkinter as tk
    # import tkinter.messagebox as messagebox
    from tkinter import ttk
else:
    import Tkinter as tk
    import ttk
    # import tkMessageBox as messagebox

if False:
    tk
    Any, Callable, List, Text, Union


def canvas(par, *args):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], int) -> tk.Canvas
    if len(args) > 1:
        return tk.Canvas(par, width=args[0], height=args[1])  # type: ignore
    return tk.Canvas(par)  # type: ignore  # for Tk


def rectangle(inst, x1, y1, x2, y2, **kw):  # {{{1
    # type: (tk.Canvas, int, int, int, int, Any) -> None
    inst.create_rectangle(x1, y1, x2, y2, **kw)  # type: ignore # for Tk


def oval(inst, x1, y1, x2, y2, **kw):  # {{{1
    # type: (tk.Canvas, int, int, int, int, Any) -> None
    inst.create_oval(x1, y1, x2, y2, **kw)  # type: ignore # for Tk


def bind(par, ev, fn):  # {{{1
    # type: (tk.Widget, Text, Callable[[tk.Event], None]) -> tk.Widget
    return par.bind(ev, fn)  # type: ignore # for Tk


def label(par, t, **kw):  # {{{1
    # type: (tk.Widget, Text, Any) -> tk.Widget
    return tk.Label(par, text=t, **kw)  # type: ignore # for Tk


def frame(par, *args):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], int) -> tk.Frame
    if len(args) > 0:
        return tk.Frame(par, height=args[0])  # type: ignore # for Tk
    return tk.Frame(par)  # type: ignore # for Tk


def button(par, t, **kw):  # {{{1
    # type: (tk.Widget, Text, Any) -> tk.Button
    return tk.Button(par, text=t, **kw)  # type: ignore # for Tk


def chkbtn(par, t, v):  # {{{1
    # type: (tk.Widget, Text, tk.IntVar) -> tk.Button
    return tk.Checkbutton(par, text=t, variable=v)  # type: ignore # for Tk


def scale(par, *args, **kw):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], float, Any) -> tk.Scale
    if len(args) < 1:
        return tk.Scale(par)  # type: ignore # for Tk
    return tk.Scale(par, from_=args[0], to=args[1],  # type: ignore
                    orient=args[2], **kw)  # type: ignore # for Tk


def scale_get(scl):  # {{{1
    # type: (tk.Scale) -> int
    return scl.get()  # type: ignore


def scale_set(scl, n):  # {{{1
    # type: (tk.Scale, Union[int, float]) -> tk.Scale
    scl.set(n)  # type: ignore
    return scl


def entry(par, *args):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], int) -> tk.Entry
    if len(args) > 0:
        return tk.Entry(par, width=args[0])  # type: ignore # for Tk
    return tk.Entry(par)  # type: ignore # for Tk


def text(par, *args):  # {{{1
    # type: (Union[tk.Tk, tk.Widget], int) -> tk.Text
    if len(args) > 0:
        return tk.Text(par, height=args[0])  # type: ignore # for Tk
    return tk.Text(par)  # type: ignore # for Tk


def text_insert(txt, n, t):  # {{{1
    # type: (Union[tk.Text, tk.Entry], int, Text) -> None
    txt.insert(n, t)  # type: ignore # for Tk


def text_delete(txt, n1, n2):  # {{{1
    # type: (tk.Text, Text, Text) -> None
    txt.delete(n1, n2)  # type: ignore # for Tk


def enty_delete(txt, n1, n2):  # {{{1
    # type: (tk.Entry, Union[int, Text], Text) -> None
    txt.delete(n1, n2)  # type: ignore # for Tk


def cmbbox(par, items, cur):  # {{{1
    # type: (tk.Widget, List[Text], int) -> ttk.Combobox
    ret = ttk.Combobox(par, values=items)  # type: ignore # for Tk
    ret.current(cur)  # type: ignore
    return ret  # type: ignore


def var_int():  # {{{1
    # type: () -> tk.IntVar
    return tk.IntVar()  # type: ignore # for Tk


def set_int(_var, n):  # {{{1
    # type: (tk.IntVar, int) -> None
    _var.set(n)  # type: ignore # for Tk


def root_quit(root):  # {{{1
    # type: (tk.Tk) -> None
    root.quit()  # type: ignore # for Tk


# end of file {{{1
# vi: ft=python:et:fdm=marker:nowrap:tw=80
