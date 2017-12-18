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
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import os
import subprocess

import tkinter as tk
from tkinter import Tk, ttk


def allok(seq: List[str]) -> bool:
    return True


class NProp(object):  # {{{1
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


# xinput {{{1
class XInputDB(object):  # {{{1
    # {{{2
    dev = 11
    propsdb = {}  # type: Dict[str, int]
    cmd_bin = "/usr/bin/xinput"
    cmd_shw = cmd_bin + " list-props {} | grep '({}):'"
    cmd_int = "set-int-prop"
    cmd_flt = "set-float-prop"
    cmd_atm = cmd_bin + " set-atomt-prop {} {} {} {}"

    cmd_wat = "query-state"

    def __init__(self):
        self._palmDims = []  # type: List[tk.IntVar]
        self._edges = []  # type: List[tk.IntVar]
        self._edgescrs = []  # type: List[tk.IntVar]
        self._movespd = []  # type: List[tk.DoubleVar]
        self._scrdist = []  # type: List[tk.IntVar]
        self._tapdurs = []  # type: List[tk.IntVar]
        self._cstspd = []  # type: List[tk.DoubleVar]
        self._prsmot = []  # type: List[tk.IntVar]
        self._prsfct = []  # type: List[tk.DoubleVar]
        self._noise = []  # type: List[tk.IntVar]
        self._softareas = []  # type: List[tk.IntVar]
        self._finger = []  # type: List[tk.IntVar]
        self._twofingerscroll = []  # type: List[tk.IntVar]
        self._clks = []  # type: List[tk.Combobox]
        self._taps = []  # type: List[tk.Combobox]

    @classmethod
    def determine_devid(cls) -> bool:  # cls {{{2
        cmd = cls.cmd_bin + " list | grep -i TouchPad"
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
    def createpropsdb(cls) -> bool:  # cls {{{2
        for name in dir(NProp):
            if name.startswith("_"):
                continue
            v = getattr(NProp, name)
            if not isinstance(v, int):
                continue
            cls.propsdb[name] = v

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
            name = line[:n]
            line = line[n:]
            if ")" not in line:
                continue
            n = line.index(")")
            line = line[:n].strip("( )")
            # print("createdb: {}".format(line))
            if not line.isdigit():
                # TODO: log
                continue
            name = name.strip("( ").lower().replace(" ", "_")
            if name.startswith("synaptics_"):
                name = name[10:]
            if name not in cls.propsdb:
                # TODO: log
                continue
            # print("{:20s}: {:3d}".format(name, int(line)))
            n += 1
            cls.propsdb[name] = int(line)
        return n < 1

    @classmethod
    def textprops(cls) -> str:  # cls {{{2
        ret = ""
        for name in cls.propsdb:
            ret += "\n{:20s} = {:3d}".format(name, cls.propsdb[name])
        if len(ret) > 0:
            ret = ret[1:]
        return ret

    def prop_get(self, key) -> List[str]:  # {{{2
        cmd = self.cmd_shw.format(self.dev, key)
        curb = subprocess.check_output(cmd, shell=True)
        curs = curb.decode("utf-8").strip()
        seq = curs.split(":")[1].split(",")
        return [i.strip() for i in seq]

    def prop_bool(self, key: int, idx: int,  # {{{2
                  v: List[bool]=[]) -> bool:
        if len(v) > 0:
            seq = ["1" if i else "0" for i in v]
            cmd = [self.cmd_bin, self.cmd_int, str(self.dev), str(key), "8"]
            if not self.fDryrun:
                print("prop_bool: " + str(cmd + seq))
                subprocess.call(cmd + seq)
            self.cmdbuf.append(cmd + seq)
        seq = self.prop_get(key)
        return True if seq[idx] == "1" else False

    def prop_int(self, typ: str, key: int, idx: int,  # {{{2
                 v: List[int]=[],
                 func: Callable[[List[str]], bool]=allok) -> bool:
        seq = ["{}".format(i) for i in v]
        if len(v) < 1:
            pass
        elif func(seq):
            cmd = [self.cmd_bin, self.cmd_int, str(self.dev),
                   str(key), typ]
            if not self.fDryrun:
                print("prop_i{}: ".format(typ) + str(cmd + seq))
                subprocess.call(cmd + seq)
            self.cmdbuf.append(cmd + seq)
        seq = self.prop_get(key)
        return int(seq[idx])

    def prop_i32(self, key: int, idx: int,  # {{{2
                 v: List[int]=[],
                 func: Callable[[List[str]], bool]=allok) -> bool:
        return self.prop_int("32", key, idx, v, func)

    def prop_i8(self, key: int, idx: int,  # {{{2
                v: List[int]=[],
                func: Callable[[List[str]], bool]=allok) -> bool:
        return self.prop_int("8", key, idx, v, func)

    def prop_flt(self, key: int, idx: int,  # {{{2
                 v: List[float]=[],
                 func: Callable[[List[str]], bool]=allok) -> bool:
        seq = ["{:f}".format(i) for i in v]
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

    def clks(self, i: int, v: List[int]=[]) -> int:  # {{{2
        assert len(v) == 0 or len(v) == 3
        return self.prop_i8(NProp.click_action, i, v)

    def taps(self, i: int, v: List[int]=[]) -> int:  # {{{2
        assert len(v) == 0 or len(v) == 7
        return self.prop_i8(NProp.tap_action, i, v)

    def tapdurs(self, i: int, v: List[int]=[]) -> int:  # {{{2
        assert len(v) == 0 or len(v) == 3
        return self.prop_i32(NProp.tap_durations, i, v)

    def taptime(self, v: Optional[int]=None) -> int:  # {{{2
        return self.prop_i32(NProp.tap_time, 0, [] if v is None else [v])

    def tapmove(self, v: Optional[int]=None) -> int:  # {{{2
        return self.prop_i32(NProp.tap_move, 0, [] if v is None else [v])

    def finger(self, i: int, v: List[int]=[]) -> int:  # {{{2
        def limit(seq: List[str]) -> bool:
            low = int(seq[0])
            hig = int(seq[1])
            return low < hig
        return self.prop_i32(NProp.finger, i, v, limit)

    def twofingerscroll(self, i: int, v: List[bool]=[]) -> bool:  # {{{2
        return self.prop_bool(NProp.two_finger_scrolling, i, v)

    def movespd(self, i: int, v: List[float]=[]) -> float:  # {{{2
        return self.prop_flt(NProp.move_speed, i, v)

    def lckdrags(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(NProp.locked_drags, 0, [] if v is None else [v])

    def lckdragstimeout(self, v: Optional[int]=None) -> int:  # {{{2
        return self.prop_i32(NProp.locked_drags_timeout, 0,
                             [] if v is None else [v])

    def cirscr(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(NProp.circular_scrolling, 0,
                              [] if v is None else [v])

    def cirtrg(self, v: Optional[int]=None) -> int:  # {{{2
        def limit(seq: List[str]) -> bool:
            cur = int(seq[0])
            return 0 <= cur <= 8
        return self.prop_i8(NProp.circular_scrolling_trigger, 0,
                            [] if v is None else [v], limit)

    def cirpad(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(NProp.circular_pad, 0, [] if v is None else [v])

    def cirdis(self, v: Optional[float]=None) -> float:  # {{{2
        return self.prop_flt(NProp.circular_scrolling_distance, 0,
                             [] if v is None else [v])

    def edges(self, i: int, v: List[int]=[]) -> bool:  # {{{2
        return self.prop_i32(NProp.edges, i, v)

    def edgescrs(self, i: int, v: List[bool]=[]) -> bool:  # {{{2
        return self.prop_bool(NProp.edge_scrolling, i, v)

    def cstspd(self, i: int, v: List[float]=[]) -> float:  # {{{2
        return self.prop_flt(NProp.coasting_speed, i, v)

    def prsmot(self, i: int, v: List[int]=[]) -> int:  # {{{2
        return self.prop_i32(NProp.pressure_motion, i, v)

    def prsfct(self, i: int, v: List[float]=[]) -> float:  # {{{2
        return self.prop_flt(NProp.pressure_motion_factor, i, v)

    def palmDetect(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(NProp.palm_detection, 0,
                              [] if v is None else [v])

    def palmDims(self, i: int, v: List[int]=[]) -> bool:  # {{{2
        return self.prop_i32(NProp.palm_dimensions, i, v)

    def softareas(self, i: int, v: List[int]=[]) -> bool:  # {{{2
        return self.prop_i32(NProp.soft_button_areas, i, v)

    def twoprs(self, v: Optional[int]=None) -> bool:  # {{{2
        return self.prop_i32(NProp.two_finger_pressure, 0,
                             [] if v is None else [v])

    def twowid(self, v: Optional[int]=None) -> bool:  # {{{2
        return self.prop_i32(NProp.two_finger_width, 0,
                             [] if v is None else [v])

    def scrdist(self, i: int, v: List[int]=[]) -> bool:  # {{{2
        return self.prop_i32(NProp.scrolling_distance, i, v)

    def gestures(self, v: Optional[bool]=None) -> bool:  # {{{2
        return self.prop_bool(NProp.gestures, 0, [] if v is None else [v])

    def noise(self, i: int, v: List[int]=[]) -> bool:  # {{{2
        return self.prop_i32(NProp.noise_cancellation, i, v)

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

    def apply(self) -> str:  # {{{2
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
        self.clks(0, [self._clks[i].current() for i in range(3)])  # 290
        self.taps(0, [self._taps[i].current() for i in range(7)])  # 291
        self.cirscr(self._cirscr.get())  # 292
        self.cirdis(self._cirdis.get())  # 293
        self.cirtrg(self._cirtrg.current())  # 294
        self.cirpad(self._cirpad.get())  # 295
        self.palmDetect(self._palmDetect.get())  # 296
        self.palmDims(0, [self._palmDims[i].get() for i in range(2)])  # 297
        self.cstspd(0, [self._cstspd[i].get() for i in range(2)])  # 298
        # xi.prsmot(i, xi._prsmot[i].get())  # 299 TODO: ??? not work ???
        self.prsfct(0, [self._prsfct[i].get() for i in range(2)])  # 300
        self.gestures(self._gestures.get())  # 303
        self.softareas(0, [self._softareas[i].get() for i in range(8)])  # 307
        self.noise(0, [self._noise[i].get() for i in range(2)])  # 308

    def dump(self) -> List[List[str]]:  # {{{2
        # from GUI.
        self.fDryrun = True
        self.cmdbuf = []

        self.apply()
        ret = [] + self.cmdbuf

        self.fDryrun = False
        self.cmdbuf = []
        return ret

    def dumps(self) -> str:  # {{{2
        # from GUI.
        self.fDryrun = True
        self.cmdbuf = []
        self.apply()
        ret = ""
        for line in self.cmdbuf:
            ret += '\n' + ' '.join(line)
        if len(ret) > 0:
            ret = ret[1:]

        self.fDryrun = False
        self.cmdbuf = []
        return ret

    def save(self, fname: str, fnameIn: str) -> str:  # {{{2
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
cmdorg = []  # type: List[List[str]]


# options {{{1
def options() -> Any:  # {{{1
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--device-id', '-d', type=int, default=0)
    p.add_argument('--file-encoding', '-e', type=str, default="utf-8")
    opts = p.parse_args()

    if opts.device_id == 0:
        XInputDB.determine_devid()
    return opts


# gui {{{1
class Gui(object):  # {{{1
    class BoolVar(object):
        def __init__(self):
            self._val = tk.IntVar()

        def get(self) -> bool:
            return self._val.get() == 1

        def set(self, v: bool) -> bool:
            self._val.set(1 if v else 0)
            return v

    def checkbox(self, parent: tk.Widget, title: str,  # {{{2
                 cur: bool) -> None:
        ret = Gui.BoolVar()
        ret._val.set(1 if cur else 0)
        tk.Checkbutton(parent, text=title,
                       variable=ret._val).pack(side=tk.LEFT)
        return ret

    def slider(self, parent: tk.Widget, from_: int, to: int,  # {{{2
               cur: int) -> None:
        ret = tk.IntVar()
        ret.set(cur)
        wid = tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL,
                       variable=ret)
        wid.pack(side=tk.LEFT)
        self.lastwid = wid
        return ret

    def slider_flt(self, parent: tk.Widget, from_: float, to: float,  # {{{2
                   cur: float) -> None:
        ret = tk.DoubleVar()
        ret.set(cur)
        tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL,
                 variable=ret, resolution=0.01).pack(side=tk.LEFT)
        return ret

    def combobox(self, parent: tk.Widget, seq: List[str],  # {{{2
                 cur: int) -> None:
        ret = ttk.Combobox(parent, values=seq)
        ret.current(cur)
        ret.pack(side=tk.LEFT)
        return ret

    def label2(self, parent: tk.Widget, txt: str, n: int,  # {{{2
               **kw: Dict[str, Any]) -> None:  # {{{2
        if len(kw) < 1:
            kw["anchor"] = tk.W
        if "width" in kw:
            ret = tk.Label(parent, text=txt, width=kw["width"])
            del kw["width"]
        else:
            ret = tk.Label(parent, text=txt)
        ret.pack(**kw)
        ret.bind("<Button-1>", gui.hint)
        ret.hint = NProp.hinttext[n]

    def label3(self, parent: tk.Widget, txt: str, n: int,  # {{{2
               **kw: Dict[str, Any]) -> None:  # {{{2
        if "side" not in kw:
            kw["side"] = tk.LEFT
        self.label2(parent, txt, n, **kw)

    def hint(self, ev: tk.Event) -> None:  # {{{2
        txt = getattr(ev.widget, "hint", "")
        if txt == "":
            return
        gui.test.delete(1.0, tk.END)
        gui.test.insert(tk.END, txt)

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
        _btns = ["black" if i else "white" for i in btns]
        gui_canvas(self.mouse, _btns, vals, [])
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
        for cmd in cmdorg:
            print("restore: " + str(cmd))
            subprocess.call(cmd)

    def cmdapply(self) -> None:  # {{{2
        xi.apply()

    def cmdsave(self) -> None:  # {{{2
        xi.dump(opts.fnameOut, opts.fnameIn)

    def cmdquit(self) -> None:  # {{{2
        self.root.quit()

    def cmdreport(self) -> None:  # {{{2
        import sys
        import platform
        from datetime import datetime
        global opts

        enc = opts.file_encoding
        fname = datetime.now().strftime("report-%Y%m%d-%H%M%S.txt")
        fp = open(fname, "at", encoding=enc)
        bs = subprocess.check_output("uname -a", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + "\n")
        bs = subprocess.check_output("python3 -m platform", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + "\n")
        fp.write("Python: {}\n".format(str(sys.version_info)))
        fp.write("Python: {} {}\n".format(
            platform.python_build(), platform.python_compiler()))
        bs = subprocess.check_output("xinput list", shell=True)
        msg = bs.decode(enc)
        fp.write(msg + "\n")
        fp.write("--- current settings (in app)---\n")
        fp.write(xi.dumps())
        # TODO: dump initial settings
        # xiorg.dump(fname)
        fp.close()

        from tkinter import messagebox
        msg = "Report: {} was made,\n" \
              "use this file to report a issue.".format(fname)
        messagebox.showinfo("Make a Report", msg)


def buildgui(opts: Any) -> Tk:  # {{{1
    global gui, cmdorg
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
    gui.mouse = tk.Canvas(frm1, width=_100, height=_100)
    frm13 = ttk.Frame(frm1)

    gui_canvas(gui.mouse, ["white"] * 7, ["0"] * 4,
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
    page1 = ttk.Frame(nb)
    nb.add(page1, text="Tap/Click")
    page4 = ttk.Frame(nb)
    nb.add(page4, text="Area")
    page2 = ttk.Frame(nb)
    nb.add(page2, text="Two-Fingers")
    page5 = ttk.Frame(nb)
    nb.add(page5, text="Misc.")
    page6 = ttk.Frame(nb)
    nb.add(page6, text="Information")
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
    v = tk.IntVar()
    v.set(0)
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
    xi._prsfct.append(gui.slider(frm, 1, 1000, xi.prsfct(0)))
    xi._prsfct.append(gui.slider(frm, 1, 1000, xi.prsfct(1)))
    frm.pack(anchor=tk.W)
    frm = tk.Frame(page5)
    gui.label3(frm, "Coasting speed", NProp.coasting_speed, width=w)
    xi._cstspd.append(gui.slider(frm, 1, 1000, xi.cstspd(0)))
    xi._cstspd.append(gui.slider(frm, 1, 1000, xi.cstspd(1)))
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
    return root


_100 = 150


def gui_scale(x: Union[str, float], y: Union[str, float]) -> Tuple[int, int]:
    rx = int(x) * _100 / 3192
    ry = int(y) * _100 / 1822
    return rx, ry


def gui_softarea(seq: List[int]) -> Tuple[int, int, int, int]:
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


def gui_canvas(inst: tk.Canvas, btns: List[str],  # {{{2
               vals: List[str], prms: List[List[int]]) -> None:
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


# main {{{1
def main() -> int:  # {{{1
    global opts
    opts = options()
    if XInputDB.createpropsdb():
        # TODO: there is not synaptic pad and exit. need the message to user.
        return 0
    root = buildgui(opts)
    root.after_idle(gui.callback_idle)
    root.mainloop()
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
