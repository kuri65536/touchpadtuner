#! /usr/bin/python3
"""license::

 This Source Code Form is subject to the terms of the Mozilla Public License,
 v.2.0. If a copy of the MPL was not distributed with this file,
 You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import re
import subprocess as sp
import sys
from typing import List, Optional, Text

import notify2  # type: ignore

List, Optional, Text  # for mypy

cmd_xinput = "xinput"

icon1 = "notification-device-firewire"
icon2 = "notification-device-eject"
icon3 = "notification-network-wireless-disconnected"

fNotify = True  # use notify or only stdout
nXdev = "0"
nXprop = "0"


def check_status():
    # type: () -> Optional[bool]
    global nXdev, nXprop
    rex_touchpad = r"Touchpad\s+id=([0-9]+)"
    rex_xprop = r"Device Enabled\s*\(([0-9]+)\)\s*:\s+([0-9]+)"

    try:
        _src = sp.check_output([cmd_xinput, "list"])
        src = _src.decode("utf-8")
    except:
        return None
    for line in src.splitlines():
        mo = re.search(rex_touchpad, line)
        if mo is None:
            continue
        _id = nXdev = mo.group(1)
        break
    else:
        return None

    try:
        _src = sp.check_output([cmd_xinput, "list-props", _id])
        src = _src.decode("utf-8")
    except:
        return None
    for line in src.splitlines():
        mo = re.search(rex_xprop, line)
        if mo is None:
            continue
        nXprop = mo.group(1)
        val = mo.group(2)
        return val == "1"
    return None


def notify(fIcon, msg):
    # type: (Optional[bool], Text) -> None  # type: ignore
    if fIcon is None:
        icon = icon3
    elif fIcon:
        icon = icon1
    else:
        icon = icon2

    print("notify: " + msg)
    if not fNotify:
        return
    notify2.init("script")
    nt = notify2.Notification("openbox", msg,
                              icon)
    nt.show()


def main(args):
    # type: (List[Text]) -> None  # type: ignore
    if "-d" in args:
        global fNotify
        fNotify = False

    ret = check_status()
    if ret is None:
        return notify(ret, "failed to get touchpad status")
    if "-n" in args:
        s = "on" if ret else "off"
        return notify(ret, "touchpad status: " + s)
    # ret = if check_status()
    s = "0" if ret else "1"  # toggle
    try:
        stat = sp.check_call([cmd_xinput, "set-prop", nXdev,
                              "--type=int", nXprop, s])
    except sp.CalledProcessError as ex:
        stat = ex.returncode
    if stat != 0:
        return notify(ret, "touchpad changing was failed: " + str(stat))
    s = "off" if ret else "on"
    return notify(ret, "touchpad toggled to: " + s)


if __name__ == "__main__":
    main(sys.argv[1:])
# vi: ft=python:nowrap:et:ts=4:tw=80:fdm=marker
