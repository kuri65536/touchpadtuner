#! /usr/bin/python3
"""license::

 This Source Code Form is subject to the terms of the Mozilla Public License,
 v.2.0. If a copy of the MPL was not distributed with this file,
 You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import re
import subprocess as sp
import sys
from typing import List, Optional, Text, Type

import notify2  # type: ignore

List, Optional, Text, Type  # for mypy

cmd_xrandr = "xrandr"

icons = ["notification-display-brightness-off",
         "notification-display-brightness-full",
         ]

fNotify = True  # use notify or only stdout


class status:
    names = []  # type: List[Text]
    conns = []  # type: List[int]
    actives = []  # type: List[int]
    nPrim = -1

    @classmethod
    def clear(cls):
        # type: () -> None
        cls.names = []
        cls.conns = []
        cls.actives = []
        cls.nPrim = -1


class status_none(status):
    pass


def fetch_status():
    # type: () -> Type[status]
    rex_screen = r"^(\S+)\s+(dis|)connected"
    rex_active = r"\+[0-9]+\+[0-9]+"

    try:
        _src = sp.check_output([cmd_xrandr, "-q", "--current"])
        src = _src.decode("utf-8")
    except:
        return status_none

    status.clear()
    for line in src.splitlines():
        mo = re.search(rex_screen, line)
        if mo is None:
            continue
        status.names.append(mo.group(1))
        status.conns.append(1 if (mo.group(2) != "dis") else 0)
        mo = re.search(rex_active, line)
        status.actives.append(1 if mo is not None else 0)
        if re.search("primary", line):
            status.nPrim = len(status.names) - 1
    if len(status.names) < 1:
        return status_none
    return status


def notify(nIcon, msg):
    # type: (int, Text) -> None  # type: ignore
    print("notify: " + msg)
    if not fNotify:
        return
    notify2.init("script")
    nt = notify2.Notification("openbox", msg,
                              icons[nIcon])
    nt.show()


def listup(icon, stat, msg):  # {{{1
    # type: (int, Type[status], Text) -> None
    for n, i in enumerate(stat.names):
        msg += i + (" (on)" if stat.actives[n] else "") + "\n"
    return notify(icon, msg)


def display_on1(stat, n, fPrim):
    # type: (Type[status], int, bool) -> List[Text]
    ret = []  # type: List[Text]
    for i in range(len(stat.names)):
        ret += ["--output", stat.names[i]]
        if i == n:
            cmd = "--auto"
        else:
            cmd = "--off"
        ret.append(cmd)
        if fPrim and i == stat.nPrim and cmd != "--off":
            ret.append("--primary")
    return ret


def display_dups(stat):
    # type: (Type[status]) -> List[Text]
    ret = []  # type: List[Text]
    name = stat.names[stat.nPrim]
    for i in range(len(stat.names)):
        ret += ["--output", stat.names[i], "--auto"]
        if i == stat.nPrim:
            ret.append("--primary")
        else:
            ret += ["--same-as", name]
    return ret


def display_exts(stat):
    # type: (Type[status]) -> List[Text]
    ret = []  # type: List[Text]
    name = stat.names[stat.nPrim]
    for i in range(len(stat.names)):
        ret += ["--output", stat.names[i], "--auto"]
        if i == stat.nPrim:
            ret.append("--primary")
        else:
            ret += ["--right-of", name]
    return ret


def main(args):
    # type: (List[Text]) -> None
    if "-d" in args:
        global fNotify
        fNotify = False

    icon = 0
    stat = fetch_status()
    if stat == status_none:
        return notify(0, "failed to get screen status")
    # if "-n" in args:
    #     return listup(stat)

    # primary -> double -> secondary -> primary...
    cmd = [cmd_xrandr]  # type: List[Text]
    if "-n" in args:
        cmd += ["--dryrun"]

    if sum(stat.conns) == 1:
        cmd += ["--auto"]  # set to active monitor
        icon = 0

    elif len(stat.conns) == 2:
        # swap or dup with option
        if sum(stat.actives) > 1:
            cmd += display_on1(stat, stat.nPrim, True)
            icon = 0
        elif "--dups" in args:
            cmd += display_dups(stat)  # to duplicated
            icon = 1
        elif "--extends" in args:
            cmd += display_exts(stat)
            icon = 1
        else:
            n = stat.actives.index(1)
            n = 0 if n == 1 else 1
            cmd += display_on1(stat, n, True)
            icon = 1
    else:
        # TODO: debug. did not have this environment.
        # give up, rotate monitors among in primary and specified
        if sum(stat.actives) > 1:
            # to primary
            cmd += display_on1(stat, stat.nPrim, True)
            icon = 0
        elif "--dups" in args:
            n = stat.actives.index(1) + 1
            n = n if n < len(stat.actives) else 0
            cmd += ["--output", stat.names[n], "--same-as",
                    stat.names[stat.nPrim]]
            icon = 1
        else:
            n = stat.actives.index(1) + 1
            n = n if n < len(stat.actives) else 0
            cmd += display_on1(stat, n, True)
            icon = 1

    # ret = if check_status()
    try:
        print(' '.join(cmd))
        st = sp.check_call(cmd)
    except sp.CalledProcessError as ex:
        st = ex.returncode
    if st != 0:
        return notify(False, "display changing was failed: " + str(st))
    stat = fetch_status()
    return listup(icon, stat, "Display switched to: ")


if __name__ == "__main__":
    main(sys.argv[1:])
# vi: ft=python:nowrap:et:ts=4:tw=80:fdm=marker
