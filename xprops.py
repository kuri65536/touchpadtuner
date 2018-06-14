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
# from logging import info

from common import (parseBool, parseFloat, parseInt, parseIntOrPercent, )

try:
    from typing import (Any, Callable, Dict, IO, List, Optional, Sized,
                        Text, Tuple, Union, )
    Any, Callable, Dict, IO, List, Optional, Text, Tuple, Union
except:
    pass


def allok(seq):
    # type: (List[Text]) -> bool
    return True


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
    # name and numbers {{{1
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
    # hint text {{{1
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
    xconfs = {  # {{{1
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


# main {{{1
def main():  # {{{1
    # type: () -> int
    pass  # TODO: launch test


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
