TouchPad(Synaptic) Tuning tool for Lxde
===============================================================================
Sometime, I face the problem of TouchPad configuration in Lubuntu.
My laptop have too sensitive TouchPad.

This tool configure the touchpad through xinput with GUI,
and no need to gnome or another heavy environment/dependencies.


Requirement
-----------------------------------------
- python and python-tk
- xinput command

### In lubuntu

for Python3

```
$ sudo apt intall python3
$ sudo apt intall python3-tk
$ sudo apt intall xf86-input-synaptics
```

for Python2

```
$ sudo apt intall python
$ sudo apt intall python-tk
$ sudo apt intall xf86-input-synaptics
```


How to use
-----------------------------------------
```
$ git clone https://github.com/kuri65536/touchpadtuner.git
$ cd touchpadtuner
$ python touchpadtuner2.py
```

### note-toggle-touchpad.py
append the script shortcut into your openbox configuration file.
in my case (Lubuntu): ~/.config/openbox/lubuntu-rc.xml.

```
    <keybind key="XF86TouchpadToggle">
        <action name="Execute">
            <command>bash -c 'eval $HOME/bin/note-toggle-touchpad.py'</command>
        </action>
    </keybind>
```

then reload the configuration file by command (or reboot your computer.)

```
$ openbox-lubuntu --reconfigure
```

### note-toggle-display.py
same as touchpad.

```
    <keybind key="W-p">
        <action name="Execute">
            <command>bash -c 'eval $HOME/bin/note-toggle-display.py'</command>
        </action>
    </keybind>
```

my laptop (E203NA) FN+f8 key generate the events

- `keydown: state 0x0, keycode 133`
- `keydown: state 0x40, keycode 33`
- `keyup: state 0x40, keycode 133`

keycode 133 is Super_L, so keybind is `W-p` .


TODO
-----------------------------------------
- Write down or modify file: `/usr/share/X11/xorg.conf.d/70-synaptic.conf`,
    to make the changes to permanent.
- Made GUI for some missing params. (
    I solved the sensitive touchpad with FingerLow and FingerHigh parameters.
    I don't use another params.
    )
- (my touchpad problem) Incorrect scroll up/down in typing.
- (my touchpad problem) Syndaemon stop with two finger scroll.


Development Environment
-----------------------------------------

| term | description   |
|:----:|:--------------|
| OS   | Lubuntu 18.04 |
| Xorg | 1.19.6        |
| lang | Python 3.6.5, Python 2.7.15rc1  |
| tool | xinput 1.6.2 (XI server 2.3) |
| tool | tkinter       |

I really don't know and don't have wayland environment.


Hardwares
-----------------------------------------

| term        | description   |
|:-----------:|:--------------|
| ASUS E203NA | as development machine |


Reference
-----------------------------------------
- https://wiki.archlinux.org/index.php/Touchpad_Synaptics
- https://help.ubuntu.com/community/SynapticsTouchpad


License
-----------------------------------------
see the top of source code, it is MPL2.0.


Screenshot
-----------------------------------------
![screen shot](https://github.com/kuri65536/touchpadtuner/blob/document-resources/screenshot-1.png)


xinput output
-----------------------------------------
### E203NA (Lubuntu 17.10, kernel 4.13.0.32)
<!-- {{{2 -->

```
Device 'ELAN1201:00 04F3:3054 Touchpad':
    Device Enabled (140):    1
    Coordinate Transformation Matrix (142):    1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000
    Device Accel Profile (270):    1
    Device Accel Constant Deceleration (271):    2.500000
    Device Accel Adaptive Deceleration (272):    1.000000
    Device Accel Velocity Scaling (273):    12.500000
    Synaptics Edges (274):    127, 3065, 98, 1726
    Synaptics Finger (275):    50, 100, 0
    Synaptics Tap Time (276):    180
    Synaptics Tap Move (277):    161
    Synaptics Tap Durations (278):    180, 180, 100
    Synaptics ClickPad (279):    1
    Synaptics Middle Button Timeout (280):    0
    Synaptics Two-Finger Pressure (281):    282
    Synaptics Two-Finger Width (282):    7
    Synaptics Scrolling Distance (283):    73, 73
    Synaptics Edge Scrolling (284):    1, 0, 0
    Synaptics Two-Finger Scrolling (285):    1, 1
    Synaptics Move Speed (286):    1.000000, 1.750000, 0.054407, 0.000000
    Synaptics Off (287):    0
    Synaptics Locked Drags (288):    0
    Synaptics Locked Drags Timeout (289):    5000
    Synaptics Tap Action (290):    2, 3, 0, 0, 1, 3, 2
    Synaptics Click Action (291):    1, 3, 0
    Synaptics Circular Scrolling (292):    0
    Synaptics Circular Scrolling Distance (293):    0.100000
    Synaptics Circular Scrolling Trigger (294):    0
    Synaptics Circular Pad (295):    0
    Synaptics Palm Detection (296):    0
    Synaptics Palm Dimensions (297):    10, 200
    Synaptics Coasting Speed (298):    20.000000, 50.000000
    Synaptics Pressure Motion (299):    30, 160
    Synaptics Pressure Motion Factor (300):    1.000000, 1.000000
    Synaptics Resolution Detect (301):    1
    Synaptics Grab Event Device (302):    0
    Synaptics Gestures (303):    1
    Synaptics Capabilities (304):    1, 0, 0, 1, 1, 0, 0
    Synaptics Pad Resolution (305):    31, 31
    Synaptics Area (306):    0, 0, 0, 0
    Synaptics Soft Button Areas (307):    1596, 0, 1495, 0, 0, 0, 0, 0
    Synaptics Noise Cancellation (308):    18, 18
    Device Product ID (267):    1267, 12372
    Device Node (266):    "/dev/input/event10"
```

<!-- }}} -->

### E203NA (17.10, under 4.13.0.21) <!-- {{{2 -->


Release
-----------------------------------------
| version | description |
|:-------:|:---|
| 1.0.0   | append the test, compat with python2, output to xconf |
| 0.3.0   | show hint text in sample label |
| 0.2.0   | append preview canvas |
| 0.1.0   | 1st version |

<!--
vi: ft=markdown:et:fdm=marker
-->
