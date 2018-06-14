#! env python
# -= encoding=utf-8 =-
'''License: Modified BSD
Copyright (c) 2018, 2017, shimoda as kuri65536 _dot_ hot mail _dot_ com
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
from __future__ import print_function
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
    file_encoding = "utf-8"
    fnameIn = "/usr/share/X11/xorg.conf.d/70-synaptics.conf"
    fnameOut = "99-synaptics.conf"


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
class IntVar(object):
    def __init__(self, v):
        # type: (Optional[tk.IntVar]) -> None
        self._val = v

    def get(self):
        # type: () -> int
        if self._val is None:
            return 0
        ret = int(self._val.get())
        return ret


class FltVar(object):
    def __init__(self, v):
        # type: (Optional[tk.DoubleVar]) -> None
        self._val = v

    def get(self):
        # type: () -> float
        assert self._val is not None
        ret = float(self._val.get())
        return ret


class BoolVar(object):
    def __init__(self, v):
        # type: (Optional[tk.IntVar]) -> None
        self._val = v

    def get(self):
        # type: () -> bool
        assert self._val is not None
        return int(self._val.get()) == 1

    def set(self, v):
        # type: (bool) -> bool
        assert self._val is not None
        self._val.set(1 if v else 0)
        return v


class CmbVar(object):
    def __init__(self, v):
        # type: (Optional[ttk.Combobox]) -> None
        self._val = v

    def get(self):
        # type: () -> int
        assert self._val is not None
        ret = int(self._val.current())
        return ret


def open_file(fname, mode):  # {{{2
    # type: (str, str) -> IO[Any]
    enc = opts.file_encoding
    if sys.version_info[0] == 2:
        return codecs.open(fname, mode, enc)
    else:
        return open(fname, mode + "t", encoding=enc)


# main {{{1
def main():  # {{{1
    # type: () -> int
    pass  # TODO: launch test


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
