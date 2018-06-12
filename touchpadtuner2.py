#! env python
# -= encoding=utf-8 =-
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
from __future__ import print_function
import sys
import os
import subprocess
from logging import info

try:
    from typing import (Any, Callable, Dict, IO, List, Optional, Sized,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, List, Optional, Text, Tuple, Union
except:
    pass


if sys.version_info[0] == 3:
    import tkinter as tk
    import tkinter.messagebox as messagebox
    from tkinter import ttk
else:
    import codecs
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox


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


class PropFormat(Sized):  # {{{1
    def __init__(self, *args):  # {{{1
        # type: (Tuple[Text, Text]) -> None
        self.fmts = args
        if args[0][0] == "dummy":
            self.fmts = ()

    def __len__(self):  # {{{1
        # type: () -> int
        return len(self.fmts)

    def __getitem__(self, idx):  # {{{1
        # type: (Any) -> Tuple[Text, Text]
        assert isinstance(idx, int)
        return self.fmts[idx]


class NProp(object):  # {{{1
    # {{{1
    '''xinput list-props 11 {{{2
        Device 'ELAN1201:00 04F3:3054 Touchpad':
        Device Enabled (140):                     1
        Coordinate Transformation Matrix (142):   1.0, 0.0, 0.0,
                                                  0.0, 1.0, 0.0,
                                                  0.0, 0.0, 1.0
        Device Accel Profile (270):               1
        Device Accel Constant Deceleration (271): 2.500000
        Device Accel Adaptive Deceleration (272): 1.000000
   page Device Accel Velocity Scaling (273):      12.500000
      4 Synaptics Edges (274):                    127, 3065, 98, 1726
      1 Synaptics Finger (275):                   50, 100, 0
      1 Synaptics Tap Time (276):                 180
      1 Synaptics Tap Move (277):                 161
      1 Synaptics Tap Durations (278):            180, 180, 100
      x Synaptics ClickPad (279):                 1
      x Synaptics Middle Button Timeout (280):    0
      2 Synaptics Two-Finger Pressure (281):      282
      2 Synaptics Two-Finger Width (282):         7
      2 Synaptics Scrolling Distance (283):       73, 73
      4 Synaptics Edge Scrolling (284):           1, 0, 0
      2 Synaptics Two-Finger Scrolling (285):     1, 1
      5 Synaptics Move Speed (286):               1.0, 1.75, 0.054407, 0.000000
      x Synaptics Off (287):                      1
      5 Synaptics Locked Drags (288):             0
      5 Synaptics Locked Drags Timeout (289):     5000
      1 Synaptics Tap Action (290):               2, 3, 0, 0, 1, 3, 2
      1 Synaptics Click Action (291):             1, 3, 0
      5 Synaptics Circular Scrolling (292):       0
      5 Synaptics Circular Scrolling Distance (293): 0.100000
      5 Synaptics Circular Scrolling Trigger (294):  0
      5 Synaptics Circular Pad (295):             0
      4 Synaptics Palm Detection (296):           0
      4 Synaptics Palm Dimensions (297):          10, 200
      5 Synaptics Coasting Speed (298):           20.000000, 50.000000
      5 Synaptics Pressure Motion (299):          30, 160
      5 Synaptics Pressure Motion Factor (300):   1.000000, 1.000000
      x Synaptics Resolution Detect (301):        1
      x Synaptics Grab Event Device (302):        0
      5 Synaptics Gestures (303):                 1
      6 Synaptics Capabilities (304):             1, 0, 0, 1, 1, 0, 0
      6 Synaptics Pad Resolution (305):           31, 31
      x Synaptics Area (306):                     0, 0, 0, 0
      4 Synaptics Soft Button Areas (307):        1596, 0, 1495, 0, 0, 0, 0, 0
      5 Synaptics Noise Cancellation (308):       18, 18
      x Device Product ID (267):                  1267, 12372
      x Device Node (266):                        "/dev/input/event8"
    '''
    # name and numbers {{{2
    coordinate_transformation_matrix = 142
    device_accel_profile = 270
    device_accel_constant_deceleration = 271
    device_accel_adaptive_deceleration = 272
    device_accel_velocity_scaling = 273
    edges = 274
    finger = 275
    tap_time = 276
    tap_move = 277
    tap_durations = 278
    clickPad = 279
    middle_button_timeout = 280
    two_finger_pressure = 281
    two_finger_width = 282
    scrolling_distance = 283
    edge_scrolling = 284
    two_finger_scrolling = 285
    move_speed = 286
    off = 287
    locked_drags = 288
    locked_drags_timeout = 289
    tap_action = 290
    click_action = 291
    circular_scrolling = 292
    circular_scrolling_distance = 293
    circular_scrolling_trigger = 294
    circular_pad = 295
    palm_detection = 296
    palm_dimensions = 297
    coasting_speed = 298
    pressure_motion = 299
    pressure_motion_factor = 300
    resolution_detect = 301
    grab_event_device = 302
    gestures = 303
    capabilities = 304
    pad_resolution = 305
    area = 306
    soft_button_areas = 307
    noise_cancellation = 308
    device_product_id = 267
    device_node = 266

    # hint numbers {{{2
    hintnums = {}  # type: Dict[Text, int]
    # hint text {{{2
    hinttext = {
        edges: """ {{{2
            X/Y coordinates for left, right, top, bottom edge.""",
        click_action: """Property: "Synaptics Click Action" {{{2
            Which mouse button  is  reported  when left-clicking with one,
            two or three fingers. Set to 0 to disable.

            Option "ClickFinger1" "integer"
            Option "ClickFinger2" "integer"
            Option "ClickFinger3" "integer" """,
        tap_action: """Property: "Synaptics Tap Action" {{{2

            RT: Which mouse button is reported on a right top
            corner tap. Set 0 to disable.

            RB: Which mouse button is reported on a right bottom corner tap.
            Set to 0 to disable.

            LT: Which mouse button is reported on a left top corner tap. Set to
            0 to disable.

            LB: Which mouse button is reported on a left bottom corner tap. Set
            to 0 to disable.

            Finger-?: Which mouse button is reported on a non-corner
            one, two or three fingers tap.
            Set to 0 to disable.

            Option "RTCornerButton" "integer"
            Option "RBCornerButton" "integer"
            Option "LTCornerButton" "integer"
            Option "LBCornerButton" "integer"
            Option "TapButton1" "integer"
            Option "TapButton2" "integer"
            Option "TapButton3" "integer"
        """,
        finger: """Property: "Synaptics Finger" {{{2
            FingerLow: When finger pressure drops below this value,
            the driver counts it as a release.

            FingerHigh: When finger pressure goes above this value,
            the driver counts it as a touch.

            When finger pressure goes above this value, the driver counts it
            as a press.  Currently a press is equivalent to putting the
            touchpad in trackstick emulation mode.

            Option "FingerLow" "integer"
            Option "FingerHigh" "integer"
            Option "FingerPress" "integer"
        """,
        tap_time: """ {{{2
       Option "MaxTapMove" "integer"
              Maximum movement of the finger for detecting  a  tap.  Property:
              "Synaptics Tap Move"
        """,
        tap_durations: """ {{{2
       Option "MaxTapTime" "integer"
              Maximum  time  (in  milliseconds) for detecting a tap. Property:
              "Synaptics Tap Durations"

       Option "MaxDoubleTapTime" "integer"
              Maximum  time  (in  milliseconds)  for  detecting  a double tap.
              Property: "Synaptics Tap Durations"

       Option "ClickTime" "integer"
              The duration of the mouse click generated by tapping.  Property:
              "Synaptics Tap Durations"

       Option "SingleTapTimeout" "integer"
              Timeout  after  a tap to recognize it as a single tap. Property:
              "Synaptics Tap Durations"
        """,
        0: ''' {{{2
       Option "Device" "string"
              This  option  specifies the device file in your "/dev" directory
              which will be used to access the physical device.  Normally  you
              should  use  something like "/dev/input/eventX", where X is some
              integer.

       Option "ClickPad" "boolean"
              Whether  the  device  is  a  click  pad.  A click pad device has
              button(s) integrated into the touchpad surface.  The  user  must
              press  downward  on  the touchpad in order to generated a button
              press. This property may be set automatically  if  a  click  pad
              device  is detected at initialization time. Property: "Synaptics
              ClickPad"

       Option "Protocol" "string"
              Specifies which kernel driver will be used by this driver.  This
              is   the  list  of  supported  drivers  and  their  default  use
              scenarios.

              auto-dev   automatic, default (recommend)
              event      Linux 2.6 kernel events
              psaux      raw device access (Linux 2.4)
              psm        FreeBSD psm driver

       Option "SHMConfig" "boolean"
              Switch on/off shared memory for run-time debugging. This  option
              does not have an effect on run-time configuration anymore and is
              only useful for hardware event debugging.

       Option "FastTaps" "boolean"
              Makes the driver react faster to a single tap,  but  also  makes
              double   clicks  caused  by  double  tapping  slower.  Property:
              "Synaptics Tap FastTap"
        ''',
        edge_scrolling: ''' {{{2
       Option "VertEdgeScroll" "boolean"
              Enable vertical scrolling when dragging along  the  right  edge.
              Property: "Synaptics Edge Scrolling"

       Option "HorizEdgeScroll" "boolean"
              Enable horizontal scrolling when dragging along the bottom edge.
              Property: "Synaptics Edge Scrolling"

       Option "CornerCoasting" "boolean"
              Enable edge scrolling to continue while the finger stays  in  an
              edge corner.  Property: "Synaptics Edge Scrolling"
        ''',
        two_finger_scrolling: ''' {{{2
       Option "VertTwoFingerScroll" "boolean"
              Enable   vertical  scrolling  when  dragging  with  two  fingers
              anywhere  on  the  touchpad.  Property:  "Synaptics   Two-Finger
              Scrolling"

       Option "HorizTwoFingerScroll" "boolean"
              Enable  horizontal  scrolling  when  dragging  with  two fingers
              anywhere  on  the  touchpad.  Property:  "Synaptics   Two-Finger
              Scrolling"
        ''',
        scrolling_distance: ''' {{{2
       Option "VertScrollDelta" "integer"
              Move  distance  of  the  finger  for  a  scroll event. Property:
              "Synaptics Scrolling Distance"

       Option "HorizScrollDelta" "integer"
              Move distance of  the  finger  for  a  scroll  event.  Property:
              "Synaptics Scrolling Distance"
        ''',
        99: '''
       Option "EdgeMotionMinZ" "integer"
              Finger  pressure  at  which  minimum  edge  motion speed is set.
              Property: "Synaptics Edge Motion Pressure"

       Option "EdgeMotionMaxZ" "integer"
              Finger pressure at which  maximum  edge  motion  speed  is  set.
              Property: "Synaptics Edge Motion Pressure"

       Option "EdgeMotionMinSpeed" "integer"
              Slowest setting for edge motion speed. Property: "Synaptics Edge
              Motion Speed"

       Option "EdgeMotionMaxSpeed" "integer"
              Fastest setting for edge motion speed. Property: "Synaptics Edge
              Motion Speed"
        ''',
        98: '''
       Option "EdgeMotionUseAlways" "boolean"
              If  on,  edge motion is also used for normal movements.  If off,
              edge motion is used only  when  dragging.  Property:  "Synaptics
              Edge Motion Always"
        ''',
        move_speed: ''' {{{2
       Option "MinSpeed" "float"
              Minimum speed factor. Property: "Synaptics Move Speed"

       Option "MaxSpeed" "float"
              Maximum speed factor. Property: "Synaptics Move Speed"

       Option "AccelFactor" "float"
              Acceleration  factor  for  normal  pointer  movements. Property:
              "Synaptics Move Speed"

       Option "TrackstickSpeed" "float"
              Speed  scale  when  in  trackstick  emulation  mode.   Property:
              "Synaptics Move Speed"
        ''',
        pressure_motion: '''
       Option "PressureMotionMinZ" "integer"
              Finger  pressure  at  which  minimum  pressure  motion factor is
              applied. Property: "Synaptics Pressure Motion"

       Option "PressureMotionMaxZ" "integer"
              Finger pressure at  which  maximum  pressure  motion  factor  is
              applied.  Property: "Synaptics Pressure Motion"
        ''',
        pressure_motion_factor: ''' {{{2
       Option "PressureMotionMinFactor" "integer"
              Lowest  setting for pressure motion factor. Property: "Synaptics
              Pressure Motion Factor"

       Option "PressureMotionMaxFactor" "integer"
              Greatest  setting  for   pressure   motion   factor.   Property:
              "Synaptics Pressure Motion Factor"
        ''',
        3: '''
       Option "HorizHysteresis" "integer"
              The  minimum  horizontal HW distance required to generate motion
              events. Can be specified as  a  percentage.  Increase  if  noise
              motion  is  a  problem  for you. Zero is disabled.  Default: 0.5
              percent of the diagonal or (in case of  evdev)  the  appropriate
              "fuzz" as advertised by the device.

       Option "VertHysteresis" "integer"
              The  minimum  vertical  HW  distance required to generate motion
              events. See HorizHysteresis.

       Option "UpDownScrolling" "boolean"
              If on, the up/down buttons generate button 4/5 events.  If  off,
              the  up  button  generates  a  double  click and the down button
              generates a button 2 event. This option is  only  available  for
              touchpads  with  physical  scroll buttons.  Property: "Synaptics
              Button Scrolling"

       Option "LeftRightScrolling" "boolean"
              If on, the left/right buttons generate button  6/7  events.   If
              off, the left/right buttons both generate button 2 events.  This
              option is only available  for  touchpads  with  physical  scroll
              buttons.  Property: "Synaptics Button Scrolling"

       Option "UpDownScrollRepeat" "boolean"
              If   on,   and  the  up/down  buttons  are  used  for  scrolling
              (UpDownScrolling), these buttons will  send  auto-repeating  4/5
              events,   with   the   delay   between   repeats  determined  by
              ScrollButtonRepeat.  This option is only available for touchpads
              with  physical  scroll  buttons.   Property:  "Synaptics  Button
              Scrolling Repeat"

       Option "LeftRightScrollRepeat" "boolean"
              If on,  and  the  left/right  buttons  are  used  for  scrolling
              (LeftRightScrolling), these buttons will send auto-repeating 6/7
              events,  with  the   delay   between   repeats   determined   by
              ScrollButtonRepeat.  This option is only available for touchpads
              with  physical  scroll  buttons.   Property:  "Synaptics  Button
              Scrolling Repeat"

       Option "ScrollButtonRepeat" "integer"
              The  number of milliseconds between repeats of button events 4-7
              from the up/down/left/right scroll buttons.  This option is only
              available for touchpads with physical scroll buttons.  Property:
              "Synaptics Button Scrolling Time"

       Option "EmulateMidButtonTime" "integer"
              Maximum time (in  milliseconds)  for  middle  button  emulation.
              Property: "Synaptics Middle Button Timeout"
        ''',
        two_finger_pressure: '''
       Option "EmulateTwoFingerMinZ" "integer"
              For  touchpads not capable of detecting multiple fingers but are
              capable of detecting finger pressure and width, this sets the  Z
              pressure threshold.  When both Z pressure and W width thresholds
              are crossed, a two finger press will be emulated. This  defaults
              to  a  value that disables emulation on touchpads with real two-
              finger detection and defaults to a value that enables  emulation
              on  remaining touchpads that support pressure and width support.
              Property: "Synaptics Two-Finger Pressure"
        ''',
        two_finger_width: ''' {{{2
       Option "EmulateTwoFingerMinW" "integer"
              For touchpads not capable of detecting multiple fingers but  are
              capable  of detecting finger width and pressure, this sets the W
              width threshold.  When both W width and  Z  pressure  thresholds
              are  crossed,  a two finger press will be emulated. This feature
              works best with  (PalmDetect)  off.  Property:  "Synaptics  Two-
              Finger Width"
        ''',
        off: ''' {{{2
       Option "TouchpadOff" "integer"
              Switch off the touchpad.  Valid values are:

              0   Touchpad is enabled
              1   Touchpad is switched off
              2   Only tapping and scrolling is switched off
              Property: "Synaptics Off"
        ''',
        locked_drags: ''' {{{2
       Option "LockedDrags" "boolean"
              If off, a tap-and-drag gesture ends when you release the finger.
              If on, the gesture is active until you tap  a  second  time,  or
              until  LockedDragTimeout  expires.  Property:  "Synaptics Locked
              Drags"
        ''',
        locked_drags_timeout: ''' {{{2
       Option "LockedDragTimeout" "integer"
              This parameter specifies how long it takes (in milliseconds) for
              the  LockedDrags  mode  to be automatically turned off after the
              finger is  released  from  the  touchpad.  Property:  "Synaptics
              Locked Drags Timeout"
        ''',
        circular_scrolling: ''' {{{2
       Option "CircularScrolling" "boolean"
              If on, circular scrolling is used. Property: "Synaptics Circular
              Scrolling"
        ''',
        circular_scrolling_distance: ''' {{{2
       Option "CircScrollDelta" "float"
              Move angle (radians) of  finger  to  generate  a  scroll  event.
              Property: "Synaptics Circular Scrolling Distance"
        ''',
        circular_scrolling_trigger: ''' {{{2
       Option "CircScrollTrigger" "integer"
              Trigger region on the touchpad to start circular scrolling

              0   All Edges
              1   Top Edge
              2   Top Right Corner
              3   Right Edge
              4   Bottom Right Corner
              5   Bottom Edge
              6   Bottom Left Corner
              7   Left Edge
              8   Top Left Corner
              Property: "Synaptics Circular Scrolling Trigger"
        ''',
        circular_pad: ''' {{{2
       Option "CircularPad" "boolean"
              Instead  of  being a rectangle, the edge is the ellipse enclosed
              by  the  Left/Right/Top/BottomEdge  parameters.   For   circular
              touchpads. Property: "Synaptics Circular Pad"
        ''',
        palm_detection: ''' {{{2
       Option "PalmDetect" "boolean"
              If  palm  detection  should  be  enabled.   Note  that this also
              requires hardware/firmware support from the touchpad.  Property:
              "Synaptics Palm Detection"
        ''',
        palm_dimensions: ''' {{{2
       Option "PalmMinWidth" "integer"
              Minimum  finger  width  at  which  touch  is  considered a palm.
              Property: "Synaptics Palm Dimensions"

       Option "PalmMinZ" "integer"
              Minimum finger pressure at which touch  is  considered  a  palm.
              Property: "Synaptics Palm Dimensions"
        ''',
        coasting_speed: ''' {{{2
       Option "CoastingSpeed" "float"
              Your  finger  needs  to  produce this many scrolls per second in
              order to start coasting.  The default is 20 which should prevent
              you   from   starting   coasting  unintentionally.   0  disables
              coasting. Property: "Synaptics Coasting Speed"

       Option "CoastingFriction" "float"
              Number  of  scrolls/second²  to  decrease  the  coasting  speed.
              Default is 50.  Property: "Synaptics Coasting Speed"
        ''',
        grab_event_device: ''' {{{2
       Option "GrabEventDevice" "boolean"
              If GrabEventDevice is true,  the  driver  will  grab  the  event
              device  for  exclusive  use  when  using  the  linux  2.6  event
              protocol.  When  using  other  protocols,  this  option  has  no
              effect.   Grabbing  the  event  device  means that no other user
              space or kernel space program sees the touchpad events.  This is
              desirable  if  the  X config file includes /dev/input/mice as an
              input device, but is undesirable if  you  want  to  monitor  the
              device  from  user space.  When changing this parameter with the
              synclient program, the change will not  take  effect  until  the
              synaptics  driver  is  disabled  and  reenabled.   This  can  be
              achieved by switching to a text console and then switching  back
              to X.
        ''',
        gestures: ''' {{{2
       Option "TapAndDragGesture" "boolean"
              Switch  on/off  the  tap-and-drag  gesture.   This gesture is an
              alternative  way  of  dragging.   It  is  performed  by  tapping
              (touching  and  releasing  the  finger), then touching again and
              moving the finger on the touchpad.  The gesture  is  enabled  by
              default  and  can  be  disabled by setting the TapAndDragGesture
              option to false. Property: "Synaptics Gestures"
        ''',
        resolution_detect: ''' {{{2
       Option
              ®esolutionDetect" "" boolean " Allow or  prevent  the  synaptics
              driver  from reporting the size of the touchpad to the X server.
              The X server normally uses this information to  scale  movements
              so  that  touchpad movement corresponds visually to mouse cursor
              movements on the screen.  However, in some rare cases where  the
              touchpad  height/width ratio is significantly different from the
              laptop, it can cause the mouse cursor to skip pixels in the X or
              Y  axis.   This  option  allows disabling this scaling behavior,
              which  can  provide  smoother  mouse  movement  in  such  cases.
              Property: "Synaptics Resolution Detect"
        ''',
        97: '''
       Option "VertResolution" "integer"
              Resolution  of  X  coordinates in units/millimeter. The value is
              used  together  with  HorizResolution  to   compensate   unequal
              vertical  and horizontal sensitivity. Setting VertResolution and
              HorizResolution equal  values  means  no  compensation.  Default
              value  is  read from the touchpad or set to 1 if value could not
              be read.  Property: "Synaptics Pad Resolution"

       Option "HorizResolution" "integer"
              Resolution of Y coordinates in units/millimeter.  The  value  is
              used together with VertResolution to compensate unequal vertical
              and   horizontal   sensitivity.   Setting   VertResolution   and
              HorizResolution  equal  values  means  no  compensation. Default
              value is read from the touchpad or set to 1 if value  could  not
              be read.  Property: "Synaptics Pad Resolution"
        ''',
        96: '''
       Option "AreaLeftEdge" "integer"
              Ignore movements, scrolling and tapping which take place left of
              this edge.  The option is disabled by default and can be enabled
              by  setting  the  AreaLeftEdge option to any integer value other
              than zero. If supported by the server (version 1.9  and  later),
              the  edge  may be specified in percent of the total width of the
              touchpad. Property: "Synaptics Area"

       Option "AreaRightEdge" "integer"
              Ignore movements, scrolling and tapping which take  place  right
              of  this  edge.   The  option  is disabled by default and can be
              enabled by setting the AreaRightEdge option to any integer value
              other  than  zero.  If  supported by the server (version 1.9 and
              later), the edge may be specified in percent of the total  width
              of the touchpad. Property: "Synaptics Area"

       Option "AreaTopEdge" "integer"
              Ignore  movements,  scrolling and tapping which take place above
              this edge.  The option is disabled by default and can be enabled
              by  setting  the  AreaTopEdge  option to any integer value other
              than zero. If supported by the server (version 1.9  and  later),
              the  edge may be specified in percent of the total height of the
              touchpad. Property: "Synaptics Area"

       Option "AreaBottomEdge" "integer"
              Ignore movements, scrolling and tapping which take  place  below
              this edge.  The option is disabled by default and can be enabled
              by setting the AreaBottomEdge option to any integer value  other
              than  zero.  If supported by the server (version 1.9 and later),
              the edge may be specified in percent of the total height of  the
              touchpad. Property: "Synaptics Area"
        ''',
        soft_button_areas: ''' {{{2
       Option "SoftButtonAreas" "RBL RBR RBT RBB MBL MBR MBT MBB"
              This  option is only available on ClickPad devices.  Enable soft
              button click area support on ClickPad devices.  The  first  four
              parameters  define  the area of the right button, and the second
              four parameters define the area of the middle button. The  areas
              are  defined  by  the  left,  right,  top,  and  bottom edges as
              sequential values of the property. If any edge is set to 0,  the
              button  is assumed to extend to infinity in the given direction.
              Any of the values may be given as  percentage  of  the  touchpad
              width  or  height,  whichever applies.  When the user performs a
              click within the defined soft button areas, the right or  middle
              click  action  is  performed.   The  use of soft button areas is
              disabled by setting all the values for the area to 0.  Property:
              "Synaptics Soft Button Areas"
              """
        ''',
        noise_cancellation: '''{{{2
Noise cancellation
       The synaptics has a built-in noise cancellation  based  on  hysteresis.
       This means that incoming coordinates actually shift a box of predefined
       dimensions such that it covers the incoming coordinate,  and  only  the
       boxes  own  center is used as input. Obviously, the smaller the box the
       better,  but  the  likelyhood  of  noise  motion  coming  through  also
       increases.
        '''
    }
    xconfs = {  # {{{2
        edges: PropFormat(("Edges", "{:d} {:d} {:d} {:d}")),
        click_action: PropFormat(("ClickFinger1", "{:d}"),
                                 ("ClickFinger2", "{:d}"),
                                 ("ClickFinger3", "{:d}")),
        tap_action: PropFormat(("RTCornerButton", "{:d}"),
                               ("RBCornerButton", "{:d}"),
                               ("LTCornerButton", "{:d}"),
                               ("LBCornerButton", "{:d}"),
                               ("TapButton1", "{:d}"),
                               ("TapButton2", "{:d}"),
                               ("TapButton3", "{:d}")),
        finger: PropFormat(("FingerLow", "{:d}"),
                           ("FingerHigh", "{:d}"),
                           ("FingerPress", "{:d}")),
        tap_time: PropFormat(("MaxTapMove", "{:d}")),
        tap_durations: PropFormat(("MaxTapTime", "{:d}"),
                                  ("MaxDoubleTapTime", "{:d}"),
                                  ("ClickTime", "{:d}"),
                                  ("SingleTapTimeout", "{:d}")),
        0: PropFormat(("dummy", ''' {{{2
       Option "Device" "string"
              This  option  specifies the device file in your "/dev" directory
              which will be used to access the physical device.  Normally  you
              should  use  something like "/dev/input/eventX", where X is some
              integer.

       Option "ClickPad" "boolean"
              Whether  the  device  is  a  click  pad.  A click pad device has
              button(s) integrated into the touchpad surface.  The  user  must
              press  downward  on  the touchpad in order to generated a button
              press. This property may be set automatically  if  a  click  pad
              device  is detected at initialization time. Property: "Synaptics
              ClickPad"

       Option "Protocol" "string"
              Specifies which kernel driver will be used by this driver.  This
              is   the  list  of  supported  drivers  and  their  default  use
              scenarios.

              auto-dev   automatic, default (recommend)
              event      Linux 2.6 kernel events
              psaux      raw device access (Linux 2.4)
              psm        FreeBSD psm driver

       Option "SHMConfig" "boolean"
              Switch on/off shared memory for run-time debugging. This  option
              does not have an effect on run-time configuration anymore and is
              only useful for hardware event debugging.

       Option "FastTaps" "boolean"
              Makes the driver react faster to a single tap,  but  also  makes
              double   clicks  caused  by  double  tapping  slower.  Property:
              "Synaptics Tap FastTap"
        ''')),
        edge_scrolling: PropFormat(("VertEdgeScroll", "{:b}"),
                                   ("HorizEdgeScroll", "{:b}"),
                                   ("CornerCoasting", " {:b}")),
        two_finger_scrolling: PropFormat(("VertTwoFingerScroll", "{:b}"),
                                         ("HorizTwoFingerScroll", "{:b}")),
        scrolling_distance: PropFormat(("VertScrollDelta", "{:d}"),
                                       ("HorizScrollDelta", "{:d}")),
        99: PropFormat(("dummy", '''
       Option "EdgeMotionMinZ" "integer"
              Finger  pressure  at  which  minimum  edge  motion speed is set.
              Property: "Synaptics Edge Motion Pressure"

       Option "EdgeMotionMaxZ" "integer"
              Finger pressure at which  maximum  edge  motion  speed  is  set.
              Property: "Synaptics Edge Motion Pressure"

       Option "EdgeMotionMinSpeed" "integer"
              Slowest setting for edge motion speed. Property: "Synaptics Edge
              Motion Speed"

       Option "EdgeMotionMaxSpeed" "integer"
              Fastest setting for edge motion speed. Property: "Synaptics Edge
              Motion Speed"
        ''')),
        98: PropFormat(("dummy", ''' {{{2
       Option "EdgeMotionUseAlways" "boolean"
              If  on,  edge motion is also used for normal movements.  If off,
              edge motion is used only  when  dragging.  Property:  "Synaptics
              Edge Motion Always"
        ''')),
        move_speed: PropFormat(("MinSpeed", "{:f}"),
                               ("MaxSpeed", "{:f}"),
                               ("AccelFactor", "{:f}"),
                               ("TrackstickSpeed", "{:f}")),
        pressure_motion: PropFormat(("PressureMotionMinZ", "{:d}"),
                                    ("PressureMotionMaxZ", "{:d}")),
        pressure_motion_factor:
            PropFormat(("PressureMotionMinFactor", "{:d}"),
                       ("PressureMotionMaxFactor", "{:d}")),
        3: PropFormat(("dummy", ''' {{{2
       Option "HorizHysteresis" "integer"
              The  minimum  horizontal HW distance required to generate motion
              events. Can be specified as  a  percentage.  Increase  if  noise
              motion  is  a  problem  for you. Zero is disabled.  Default: 0.5
              percent of the diagonal or (in case of  evdev)  the  appropriate
              "fuzz" as advertised by the device.

       Option "VertHysteresis" "integer"
              The  minimum  vertical  HW  distance required to generate motion
              events. See HorizHysteresis.

       Option "UpDownScrolling" "boolean"
              If on, the up/down buttons generate button 4/5 events.  If  off,
              the  up  button  generates  a  double  click and the down button
              generates a button 2 event. This option is  only  available  for
              touchpads  with  physical  scroll buttons.  Property: "Synaptics
              Button Scrolling"

       Option "LeftRightScrolling" "boolean"
              If on, the left/right buttons generate button  6/7  events.   If
              off, the left/right buttons both generate button 2 events.  This
              option is only available  for  touchpads  with  physical  scroll
              buttons.  Property: "Synaptics Button Scrolling"

       Option "UpDownScrollRepeat" "boolean"
              If   on,   and  the  up/down  buttons  are  used  for  scrolling
              (UpDownScrolling), these buttons will  send  auto-repeating  4/5
              events,   with   the   delay   between   repeats  determined  by
              ScrollButtonRepeat.  This option is only available for touchpads
              with  physical  scroll  buttons.   Property:  "Synaptics  Button
              Scrolling Repeat"

       Option "LeftRightScrollRepeat" "boolean"
              If on,  and  the  left/right  buttons  are  used  for  scrolling
              (LeftRightScrolling), these buttons will send auto-repeating 6/7
              events,  with  the   delay   between   repeats   determined   by
              ScrollButtonRepeat.  This option is only available for touchpads
              with  physical  scroll  buttons.   Property:  "Synaptics  Button
              Scrolling Repeat"

       Option "ScrollButtonRepeat" "integer"
              The  number of milliseconds between repeats of button events 4-7
              from the up/down/left/right scroll buttons.  This option is only
              available for touchpads with physical scroll buttons.  Property:
              "Synaptics Button Scrolling Time"

       Option "EmulateMidButtonTime" "integer"
              Maximum time (in  milliseconds)  for  middle  button  emulation.
              Property: "Synaptics Middle Button Timeout"
        ''')),
        two_finger_pressure: PropFormat(("EmulateTwoFingerMinZ", "{:d}")),
        two_finger_width: PropFormat(("EmulateTwoFingerMinW", "{:d}"), ),
        off: PropFormat(("TouchpadOff", "{:d}"), ),
        locked_drags: PropFormat(("LockedDrags", "{:b}"), ),
        locked_drags_timeout: PropFormat(("LockedDragTimeout", "{:d}"), ),
        circular_scrolling: PropFormat(("CircularScrolling", "{:b}"), ),
        circular_scrolling_distance: PropFormat(("CircScrollDelta", "{:f}"), ),
        circular_scrolling_trigger:
            PropFormat(("CircScrollTrigger", "{:d}"), ),
        circular_pad: PropFormat(("CircularPad", "{:b}"), ),
        palm_detection: PropFormat(("PalmDetect", "{:b}"), ),
        palm_dimensions: PropFormat(("PalmMinWidth", "{:d}"),
                                    ("PalmMinZ", "{:d}")),
        coasting_speed: PropFormat(("CoastingSpeed", "{:f}"),
                                   ("CoastingFriction", "{:f}")),
        grab_event_device: PropFormat(("GrabEventDevice", "{:b}"), ),
        gestures: PropFormat(("TapAndDragGesture", "{:b}"), ),
        resolution_detect: PropFormat(("ResolutionDetect", "{:b}"), ),
        97: PropFormat(("VertResolution", "{:d}"),
                       ("HorizResolution", "{:d}")),
        96: PropFormat(("AreaLeftEdge", "{:d}"),
                       ("AreaRightEdge", "{:d}"),
                       ("AreaTopEdge", "{:d}"),
                       ("AreaBottomEdge", "{:d}")),
        soft_button_areas: PropFormat((
            "SoftButtonAreas", "{:P} {:P} {:P} {:P} {:P} {:P} {:P} {:P}")),
        noise_cancellation: PropFormat(("HorizonHysterisis", "{:d}"),
                                       ("VerticalHysterisis", "{:d}")),
    }

    def __init__(self, n, idx):  # {{{1
        # type: (int, int) -> None
        self.n = n
        self.idx = idx
        self.val = None  # type: Any
        self.vals = [None] * len(NProp.xconfs[n])   # type: List[Any]
        self.wrote = []  # type: List[int]
        self.n_section = -1

    @classmethod
    def compose_format(cls, fmt, v):  # cls {{{1
        # type: (Text, Any) -> Text
        # TODO: more complex conversion.
        fmt = fmt.replace("{:P}", "{:d}%")

        if not isinstance(v, (tuple, list)):
            return fmt.format(v)
        _v = []  # type: List[Any]
        for i in v:
            if "{:d}" in fmt:
                _v.append(int(i))
            elif "{:f}" in fmt:
                _v.append(float(i))
            else:
                _v.append(str(i))
        return fmt.format(*_v)

    def compose(self, idx):  # {{{1
        # type: (int) -> Text
        assert self.n in NProp.xconfs
        opts = NProp.xconfs[self.n]
        assert 0 <= idx < len(opts)
        opt, fmt = opts[idx]
        fmt = ((" " * 8) + 'Option "' + opt + '" "' +
               fmt + '"  # by touchpadtuner\n')
        val = self.vals[idx]
        return self.compose_format(fmt, val)

    @classmethod
    def parse(cls, src):  # cls {{{1
        # type: (Text) -> Optional[NProp]
        _src = src.strip()
        if _src.startswith("#"):
            return None  # comment line
        if not _src.lower().startswith("option "):
            return None  # not option line.
        _src = _src[8:].strip()  # remove 'Option' with starting '"'.
        for key, opts in cls.xconfs.items():
            for n, (opt, fmt) in enumerate(opts.fmts):
                o = opt + '" '
                if not _src.startswith(o):
                    continue
                _src = _src[len(o):]
                _src = cls.parse_quote(_src)
                ret = NProp(key, n)
                v = cls.parse_xconf(fmt, _src)
                if v is None:
                    break
                ret.val = v
                ret.vals[n] = v
                return ret
        return None

    @classmethod
    def parse_quote(cls, src):  # cls {{{1
        # type: (Text) -> Text
        ret = ""
        f_quote, f_escape = False, False
        for ch in src:
            if not f_quote:
                if ch == '"':
                    f_quote = True
                continue
            if f_escape:
                f_escape = False
            elif ch == '\\':
                f_escape = True
                continue
            elif ch == '"':
                return ret
            ret += ch
        # can't parse in quote
        return src

    @classmethod
    def parse_xconf(cls, fmt, _src):  # cls {{{1
        # type: (Text, Text) -> Any
        # TODO(Shimoda): remove the inline comment or ends '"'.
        if fmt == "{:d}":
            return parseInt(_src)
        elif fmt == "{:b}":
            return parseBool(_src)
        elif fmt == "{:f}":
            return parseFloat(_src)
        # else:
        #     assert False, "xconfs fmt {} not implemented".format(fmt)

        seq = fmt.split(" ")
        func = parseInt  # type: Callable[[Any], Any]
        if seq[0] == "{:d}":
            func = parseInt
        elif seq[0] == "{:b}":
            func = parseBool
        elif seq[0] == "{:f}":
            func = parseFloat
        elif seq[0] == "{:P}":
            func = parseIntOrPercent
        else:
            raise RuntimeError("format:{} can't be parsed".format(seq[0]))

        ret = []  # type: List[Any]
        for n, term in enumerate(_src.split(" ")):
            if n >= len(seq):
                return ret
            v = func(term)
            if v is None:
                # TODO(Shimoda): log error messsage.
                return None
            ret.append(v)
        return ret


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
    global opts
    assert opts is not None
    enc = opts.file_encoding
    if sys.version_info[0] == 2:
        return codecs.open(fname, mode, enc)
    else:
        return open(fname, mode + "t", encoding=enc)


# xinput {{{1
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
        self.cmdbuf = []  # type: List[List[Text]]
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
            if not self.fDryrun:
                info("prop_bool: {}".format(str(cmd + seq)))
                subprocess.call(cmd + seq)
            self.cmdbuf.append(cmd + seq)
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
                   Text(key), typ]
            if not self.fDryrun:
                info("prop_i{}: ".format(typ) + Text(cmd + seq))
                subprocess.call(cmd + seq)
            self.cmdbuf.append(cmd + seq)
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
            if not self.fDryrun:
                print("prop_flt: " + str(cmd + seq))
                subprocess.call(cmd + seq)
            self.cmdbuf.append(cmd + seq)
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

    def apply(self):  # {{{1
        # type: () -> bool
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

    def dump(self):  # {{{2
        # type: () -> List[List[Text]]
        # from GUI.
        self.fDryrun = True
        self.cmdbuf = []  # type: List[List[Text]]

        self.apply()
        # ret = self.cmdbuf.copy()  # type: List[List[str]]
        ret = list(self.cmdbuf)

        self.fDryrun = False
        self.cmdbuf = []
        return ret

    def dumpdb(self):  # {{{2
        # type: () -> Dict[NProp, Any]
        return {}

    def dumps(self):  # {{{2
        # type: () -> Text
        # from GUI.
        self.fDryrun = True
        self.cmdbuf = []
        self.apply()
        ret = u""
        for line in self.cmdbuf:
            ret += u'\n' + u' '.join(line)
        if len(ret) > 0:
            ret = ret[1:]

        self.fDryrun = False
        self.cmdbuf = []
        return ret

    @classmethod
    def read(cls, fname):  # cls {{{1
        # type: (str) -> Dict[int, NProp]
        ret = {}  # type: Dict[int, NProp]
        fp = open_file(fname, "r")
        cls.section_parser_clear()
        for i, line in enumerate(fp):
            sec, id_name = cls.section_parser(line)
            if sec < 0:
                continue
            prop = NProp.parse(line)
            if prop is None:
                continue  # just ignore that line could not be parsed.
            if prop.n in ret:
                dst = ret[prop.n]
            else:
                # merge prop.
                ret[prop.n] = prop
                dst = prop
            # TODO: split a prop to different section...
            dst.n_section = sec
            dst.vals[prop.idx] = prop.val
        return ret

    @classmethod
    def save(cls, fname, fnameIn, db):  # cls {{{1
        # type: (Text, Text, Dict[int, NProp]) -> bool
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
            EndSection  # }}}
        '''
        fp = open_file(fname, "w")
        fi = open_file(fnameIn, "r")
        p_sec = -1
        cls.section_parser_clear()
        fSynapticSection = False
        for i, line in enumerate(fi):
            n_sec, cur_sec = cls.section_parser(line)
            if n_sec < 0:
                if fSynapticSection:
                    cls.save_remains(fp, db, p_sec)
                fSynapticSection = False
                fp.write(line)
                continue
            p_sec = n_sec
            fSynapticSection = True

            prop = NProp.parse(line)
            if prop is None:
                fp.write(line)
                continue
            if prop.n not in db:
                fp.write(line)
                continue
            # TODO(Shimoda): append the comment after compose.
            import pdb; pdb.set_trace()
            db[prop.n].wrote.append(prop.idx)
            if prop.val == db[prop.n].vals[prop.idx]:
                fp.write(line)  # write original, just mark to db.
                continue
            line = db[prop.n].compose(prop.idx)
            fp.write(line)
        fi.close()
        fp.close()

        # ret += self.dump_line_int("FingerLow", db.fingerlow())
        # ret += self.dump_line_int("FingerHigh", db.fingerhig())
        # ret += self.dump_line_bool("VertTwoFingerScroll",
        #                            db.vert2fingerscroll())
        # ret += self.dump_line_bool("HorizTwoFingerScroll",
        #                            db.horz2fingerscroll())
        return False

    @classmethod
    def is_begin_of_section(cls, line):  # cls {{{2
        # type: (Text) -> Text
        line = line.strip().lower()
        if not line.startswith('section '):
            return ""
        seq = line.split('"')
        ret = seq[1]
        return ret

    @classmethod
    def is_end_section(cls, line):  # cls {{{2
        # type: (Text) -> bool
        line = line.strip().lower()
        return line.startswith("endsection")

    @classmethod
    def is_identifier(cls, line):  # cls {{{2
        # type: (Text) -> Text
        line = line.strip().lower()
        if not line.startswith("identifier"):
            return ""
        seq = line.split('"')
        ret = seq[1]
        return ret

    @classmethod
    def is_synaptic_section(cls, line):  # cls {{{2
        # type: (Text) -> bool
        line = line.strip().lower()
        if not line.startswith('driver '):
            return False
        line = line[7:].strip()
        if not line.startswith('"synaptics"'):
            return False
        return True

    @classmethod
    def section_parser(cls, line):  # cls {{{1
        # type: (Text) -> Tuple[int, Text]
        if cls.is_end_section(line):
            cls.f_section = False
            return -1, ""
        if not cls.f_section:
            # secname is lower-case
            secname = cls.is_begin_of_section(line)
            if secname == "":
                return -1, ""
            if secname != "inputclass":
                return -1, ""
            cls.f_section = True
            cls.n_section += 1
            cls.cur_section = ""
            return cls.n_section, ""
        if cls.cur_section == "":
            id_name = cls.is_identifier(line)
            if id_name != "":
                cls.cur_section = id_name
                cls.sections[cls.n_section] = id_name
                return cls.n_section, id_name
        return cls.n_section, cls.cur_section

    @classmethod
    def section_parser_clear(cls):  # cls {{{1
        # type: () -> None
        cls.f_section = False
        cls.n_section = 0
        cls.cur_section = ""
        cls.sections = {}

    @classmethod
    def save_remains(cls, fp, db, sec_prev):  # cls {{{2
        # type: (IO[Text], Dict[int, NProp], int) -> bool
        fWrote = False
        for n, prop in db.items():
            if not isinstance(prop, NProp):
                continue
            if prop.n_section != sec_prev:
                continue
            for idx, v in enumerate(prop.vals):
                if v is None:
                    continue  # not specified clearly
                if idx in prop.wrote:
                    continue  # already output
                if v == -1:
                    continue  # not specified output
                # TODO(Shimoda): check v is default
                # if is_default(v):
                #    continue
                if not fWrote:
                    fWrote = True
                    fp.write(" " * 8 + "# output by touchpadtuner\n")
                line = prop.compose(idx)
                fp.write(line)
        return False


# {{{2
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
        xi.apply()

    def cmdsave(self):  # {{{2
        # type: () -> None
        assert opts is not None
        db = XInputDB.read(opts.fnameIn)
        XInputDB.save(opts.fnameOut, opts.fnameIn, db)

    def cmdquit(self):  # {{{2
        # type: () -> None
        self.root.quit()

    def cmdreport(self):  # {{{2
        # type: () -> None
        import sys
        import platform
        from datetime import datetime
        global opts

        assert opts is not None
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
    gui.test.insert(tk.END, "Test field\n1\n2\n3\n4\n5\n6\nblah\nblah...")

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
    seq = ["Disabled", "Left-Click", "Middel-Click", "Right-Click"]
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
    tk.Label(page3, text="License: Modified BSD, 2017").pack()
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
opts = None
gui = None  # type: Optional[Gui]


# main {{{1
def main():  # {{{1
    # type: () -> int
    global gui, opts
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
