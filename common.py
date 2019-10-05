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
import subprocess as sp
import sys

try:
    from typing import (Any, IO, List, Optional,
                        Text, Tuple, Union, )
    Any, IO, List, Optional, Text, Tuple, Union
except:
    pass


if sys.version_info[0] == 3:
    import tkinter as tk
    from tkinter import ttk
else:
    import Tkinter as tk
    import ttk
    import codecs

tk, ttk


class opts(object):  # {{{1
    fDryrun = True
    file_encoding = "utf-8"
    fnameIn = "/usr/share/X11/xorg.conf.d/70-synaptics.conf"
    fnameOut = "99-synaptics.conf"
    xsection = "touchpad catchall"


def allok(seq):
    # type: (List[Text]) -> bool
    return True


class Percent(object):
    def __init__(self, rate):  # {{{1
        # type: (float) -> None
        self.rate = rate  # FIXME: decimal?

    def __repr__(self):  # {{{1
        # type: () -> Text
        return "{}%".format(self.rate)


def parseInt(src):  # {{{1
    # type: (str) -> Optional[int]
    src = src.strip()
    try:
        ret = int(src)
    except:
        return None
    return ret


def parseIntOrPercent(src):  # {{{1
    # type: (str) -> Union[None, int, Percent]
    src = src.strip()
    if src.endswith("%"):
        try:
            ret = float(src[:-1])
            return Percent(ret)
        except:
            pass
        return None
    try:
        return int(src)
    except:
        pass
    return None


def parseBool(src):
    # type: (str) -> Optional[bool]
    ret = parseInt(src)
    if ret is None:
        return None
    if ret == 1:
        return True
    return False


def parseFloat(src):
    # type: (str) -> Optional[float]
    src = src.strip()
    try:
        ret = float(src)
    except:
        return None
    return ret


def compose_format(fmt, vals):  # {{{2
    # type: (Text, List[Any]) -> Tuple[Text, List[Text]]
    class Term(object):
        def __init__(self):
            # type: () -> None
            self.type = u"undefined"
            self.sArg = u""
            self.nArg = -2

        def compose(self, arg):
            # type: (Any) -> Text
            return str(arg)

    ret1 = u""
    chEscape = u""
    seq = []
    for ch in fmt:
        if chEscape != u"":
            chEscape = u""
            ret1 = ret1 + chEscape + ch
            continue
        if ch == u"{":
            term = Term()
            ret1 += ch
            continue
        if term is None:
            ret1 += ch
            continue
        if term.nArg == -2:  # not parsed
            if ch == u":":
                if not term.sArg.isdigit():
                    term.nArg = -1  # invalid
                else:
                    term.nArg = int(term.sArg)
                continue
            if ch.isdigit():
                term.sArg += ch
                continue
            term.nArg = -1  # not set
        if ch == u"}":
            ret1 += ch
            seq.append(term)
            continue
        if ch == u"P":
            term.type = "int or percent"
        elif ch == u"d":
            term.type = u"int"
        elif ch == u"f":
            term.type = u"float"
        elif ch == u"b":
            term.type = u"bool"
        else:
            assert False, u"new type of compose: {}".format(ch)

    terms = ["" for i in range(len(vals))]
    for n, term in enumerate(seq):
        if term.nArg > 0:
            i = term.nArg
        else:
            i = n
        if i >= len(terms):
            assert False, u"format arguments too much than params->{}".format(
                    fmt)
        terms[i] = term.compose(vals[i])
    import pdb
    pdb.set_trace()
    return ret1, terms


# wrapper for mypy {{{1
class GuiVar(object):  # {{{1
    def get(self):  # {{{1
        # type: () -> Text
        assert False


class IntVar(GuiVar):  # {{{1
    def __init__(self, v):
        # type: (tk.IntVar) -> None
        self._val = v

    def get(self):
        # type: () -> Text
        ret = int(self._val.get())  # type: ignore # for Tk
        return Text(ret)


class FltVar(GuiVar):  # {{{1
    def __init__(self, v):
        # type: (float) -> None
        self._val = tk.DoubleVar()  # type: ignore # for Tk
        self._val.set(v)  # type: ignore

    def get(self):
        # type: () -> Text
        assert self._val is not None
        ret = float(self._val.get())  # type: ignore # for Tk
        return Text(ret)

    def get_var(self):
        # type: () -> tk.DoubleVar
        return self._val  # type: ignore # for Tk


class BoolVar(GuiVar):  # {{{1
    def __init__(self, v):
        # type: (Optional[tk.IntVar]) -> None
        self._val = v

    def get(self):
        # type: () -> Text
        assert self._val is not None
        return int(self._val.get()) == 1  # type: ignore # for Tk

    def set(self, v):
        # type: (bool) -> bool
        assert self._val is not None
        self._val.set(1 if v else 0)  # type: ignore # for Tk
        return v


class CmbVar(GuiVar):  # {{{1
    def __init__(self, v):
        # type: (Optional[ttk.Combobox]) -> None
        self._val = v

    def get(self):
        # type: () -> Text
        assert self._val is not None
        ret = int(self._val.current())  # type: ignore # for Tk
        return Text(ret)


def open_file(fname, mode):  # {{{2
    # type: (str, str) -> IO[Any]
    enc = opts.file_encoding
    if sys.version_info[0] == 2:
        return codecs.open(fname, mode, enc)
    else:
        return open(fname, mode + "t", encoding=enc)


def check_output(args):  # {{{1
    # type: (List[Text]) -> Text
    enc = opts.file_encoding
    curb = sp.check_output(args)
    curs = curb.decode(enc)
    return curs  # type: ignore


# main {{{1
def main():  # {{{1
    # type: () -> int
    pass  # TODO: launch test


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
