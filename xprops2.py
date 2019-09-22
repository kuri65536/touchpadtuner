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
import re
import subprocess as sp
from typing import Dict, Text
# from logging import info

from xprops import NProp, PropFormat


Dict, Text


class NProp1804(NProp):  # {{{1
    # {{{1
    # name and numbers {{{1
    device_enabled = 140
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
    clickpad = 279
    middle_button_timeout = 280
    two_finger_pressure = 281
    two_finger_width = 282
    scrdist = scrolling_distance = 283
    edgescrs = edge_scrolling = 284
    two_finger_scrolling = 285
    move_speed = 286
    off = 287
    locked_drags = 288
    locked_drags_timeout = 289
    tap_action = 290
    click_action = 291
    cirscr = circular_scrolling = 292
    cirdis = circular_scrolling_distance = 293
    cirtrg = circular_scrolling_trigger = 294
    cirpad = circular_pad = 295
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
    softareas = soft_button_areas = 307
    noise_cancellation = 308
    device_product_id = 267
    device_node = 266

    pairs = [
        ("device_enabled", "Device Enabled"),  # (140):                     1
        ("coordinate_transformation_matrix",
            "Coordinate Transformation Matrix"),  # = 142
        ("device_accel_profile", "Device Accel Profile"),  # = 270
        ("device_accel_constant_deceleration",
            "Device Accel Constant Deceleration"),  # = 271
        ("device_accel_adaptive_deceleration",
            "Device Accel Adaptive Deceleration"),  # = 272
        ("device_accel_velocity_scaling",
            "Device Accel Velocity Scaling"),  # = 273
        ("edges", "Synaptics Edges"),  # = 274
        ("finger", "Synaptics Finger"),  # = 275
        ("tap_time", "Synaptics Tap Time"),  # = 276
        ("tap_move", "Synaptics Tap Move"),  # = 277
        ("tap_durations", "Synaptics Tap Durations"),  # = 278
        ("clickpad", "Synaptics ClickPad"),  # = 279
        ("middle_button_timeout", "Synaptics Middle Button Timeout"),  # = 280
        ("two_finger_pressure", "Synaptics Two-Finger Pressure"),  # = 281
        ("two_finger_width", "Synaptics Two-Finger Width"),  # = 282
        ("scrdist", "Synaptics Scrolling Distance"),  # = 283
        ("edgescrs", "Synaptics Edge Scrolling"),  # = 284
        ("two_finger_scrolling", "Synaptics Two-Finger Scrolling"),  # = 285
        ("move_speed", "Synaptics Move Speed"),  # = 286
        ("off", "Synaptics Off"),  # = 287
        ("locked_drags", "Synaptics Locked Drags"),  # = 288
        ("locked_drags_timeout", "Synaptics Locked Drags Timeout"),  # = 289
        ("tap_action", "Synaptics Tap Action"),  # = 290
        ("click_action", "Synaptics Click Action"),  # = 291
        ("cirscr", "Synaptics Circular Scrolling"),  # = 292
        ("cirdis", "Synaptics Circular Scrolling Distance"),  # = 293
        ("cirtrg", "Synaptics Circular Scrolling Trigger"),  # = 294
        ("cirpad", "Synaptics Circular Pad"),  # = 295
        ("palm_detection", "Synaptics Palm Detection"),  # = 296
        ("palm_dimensions", "Synaptics Palm Dimensions"),  # = 297
        ("coasting_speed", "Synaptics Coasting Speed"),  # = 298
        ("pressure_motion", "Synaptics Pressure Motion"),  # = 299
        ("pressure_motion_factor",
            "Synaptics Pressure Motion Factor"),  # = 300
        ("resolution_detect", "Synaptics Resolution Detect"),  # = 301
        ("grab_event_device", "Synaptics Grab Event Device"),  # = 302
        ("gestures", "Synaptics Gestures"),  # = 303
        ("capabilities", "Synaptics Capabilities"),  # = 304
        ("pad_resolution", "Synaptics Pad Resolution"),  # = 305
        ("area", "Synaptics Area"),  # = 306
        ("softareas", "Synaptics Soft Button Areas"),  # = 307
        ("noise_cancellation", "Synaptics Noise Cancellation"),  # = 308
        ("device_product_id", "Device Product ID"),  # = 267
        ("device_node", "Device Node"),  # = 266
    ]

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
        ''',
        279: ''' {{{2
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
        move_speed: PropFormat(("MinSpeed", "{:f}", "3"),
                               ("MaxSpeed", "{:f}", "3"),
                               ("AccelFactor", "{:f}", "3"),
                               ("TrackstickSpeed", "{:f}", "3")),
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
        circular_scrolling_distance:
            PropFormat(("CircScrollDelta", "{:f}", "3"), ),
        circular_scrolling_trigger:
            PropFormat(("CircScrollTrigger", "{:d}"), ),
        circular_pad: PropFormat(("CircularPad", "{:b}"), ),
        palm_detection: PropFormat(("PalmDetect", "{:b}"), ),
        palm_dimensions: PropFormat(("PalmMinWidth", "{:d}"),
                                    ("PalmMinZ", "{:d}")),
        coasting_speed: PropFormat(("CoastingSpeed", "{:f}", "3"),
                                   ("CoastingFriction", "{:f}", "3")),
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
    xconfs[tap_move] = xconfs[tap_durations]

    xinputs = {  # {{{1
        edges: 4,  # 274
        finger: 3,  # 275
        tap_time: 1,  # 276
        tap_move: 1,  # 277
        tap_durations: 3,  # 278
        two_finger_pressure: 1,  # 281
        two_finger_width: 1,  # 282
        scrdist: 2,  # 283
        edgescrs: 3,  # 284
        two_finger_scrolling: 2,
        move_speed: 4,  # 286
        locked_drags: 1,  # 288
        locked_drags_timeout: 1,
        tap_action: 7,  # 290
        click_action: 3,  # 291
        cirscr: 1,  # 292
        cirdis: 1,  # 293
        cirtrg: 1,  # 294
        cirpad: 1,  # 295
        palm_detection: 1,  # 296
        palm_dimensions: 2,  # 297
        coasting_speed: 2,  # 298
        pressure_motion: 1,  # 299 ???
        pressure_motion_factor: 2,  # 300
        gestures: 1,  # 303
        softareas: 8,  # 307
        noise_cancellation: 2,  # 308
    }

    @classmethod  # get_touchpad_id {{{1
    def get_touchpad_id(cls):
        # type: () -> Text
        _id = ""
        for line in sp.check_output("xinput").splitlines():
            if "Touchpad" not in line:
                continue
            seq = line.split("\t")
            for src in seq:
                if not src.startswith("id="):
                    continue
                _id = src.replace("id=", "")
                return _id
        return ""

    @classmethod  # auto {{{1
    def auto_id(cls):
        # type: () -> int
        _id = cls.get_touchpad_id()
        cmd = ["xinput", "list-props", _id]
        seq = cls.pairs + []
        for line in sp.check_output(cmd).splitlines():
            i = -1
            for n, (p, key) in enumerate(seq):
                if key not in line:
                    continue
                mo = re.search(r"([0-9]+)", line)
                if not mo:
                    continue
                _id = mo.group(1)
                i = n
                setattr(cls, p, int(_id))
                # print("id:{:3} as {}".format(_id, p))
                break
            else:
                print("???????:" + line)
            if i != -1:
                del seq[i]
        for p, key in cls.pairs:
            print("{:3} was loaded as {}".format(getattr(cls, p), p))
        for p, key in seq:
            print("{} was not found...".format(p))
        return 0


# main {{{1
def main():  # {{{1
    # type: () -> int
    _id = NProp1804.get_touchpad_id()
    if _id != "":
        print("detected touchpad as id=" + _id)
        # os.system("xinput list-props " + _id)
        NProp1804.auto_id()
    else:
        print("does not detected touchpad")
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
