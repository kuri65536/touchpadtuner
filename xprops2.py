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
from logging import info, warning as warn
import re
from typing import Dict, Iterator, Optional, Text, Tuple, Type
# from logging import info

import common
from xprops import NProp, PropFormat


Dict, Iterator, Optional, Text, Tuple, Type


class NProp1804(NProp):  # {{{1
    # {{{1
    # name and numbers {{{1
    device_enabled = NProp("Device Enabled", None, "")  # {{{1 (140):
    coordinate_transformation_matrix = NProp(  # {{{1
      "Coordinate Transformation Matrix", None, "")  # = 142
    device_accel_profile = NProp("Device Accel Profile", None, "")  # {{{1 =270
    device_accel_constant_deceleration = NProp(  # {{{1
      "Device Accel Constant Deceleration", None, "")  # = 271
    device_accel_adaptive_deceleration = NProp(  # {{{1
      "Device Accel Adaptive Deceleration", None, "")  # = 272
    device_accel_velocity_scalin = NProp(  # {{{1
      "Device Accel Velocity Scaling", None, "")  # = 273
    edges = NProp(  # {{{1
        "Synaptics Edges",
        PropFormat(("Edges", "{:d} {:d} {:d} {:d}")),
        "X/Y coordinates for left, right, top, bottom edge.")
    finger = NProp("Synaptics Finger",  # {{{1
                   PropFormat(("FingerLow", "{:d}"),
                              ("FingerHigh", "{:d}"),
                              ("FingerPress", "{:d}")),
                   """Property: "Synaptics Finger"
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
        """)
    tap_time = NProp("Synaptics Tap Time",  # {{{1 = 276
                     PropFormat(("MaxTapTime", "{:d}")),
                     """Option "MaxTapTime" "integer"
                        Maximum  time  (in  milliseconds) for detecting a tap.
                        Property: "Synaptics Tap Durations" <- wrong? """)
    tap_move = NProp("Synaptics Tap Move",  # {{{1 = 277
                     PropFormat(("MaxTapMove", "{:d}")),  # same as tap_dur
                     """Option "MaxTapMove" "integer"
                                Maximum movement of the finger for detecting
                                a tap. Property: "Synaptics Tap Move""")
    tap_durations = NProp("Synaptics Tap Durations",  # {{{1 = 278
                          PropFormat(("MaxDoubleTapTime", "{:d}"),
                                     ("ClickTime", "{:d}"),
                                     ("SingleTapTimeout", "{:d}")),
                          """Option "MaxDoubleTapTime" "integer"
              Maximum  time  (in  milliseconds)  for  detecting  a double tap.
              Property: "Synaptics Tap Durations"

       Option "ClickTime" "integer"
              The duration of the mouse click generated by tapping.  Property:
              "Synaptics Tap Durations"

       Option "SingleTapTimeout" "integer"
              Timeout  after  a tap to recognize it as a single tap. Property:
              "Synaptics Tap Durations"
        """)
    clickpad = NProp("Synaptics ClickPad",  # {{{1 = 279
                     PropFormat(("ClickPad", "{:d}")),
                     """Option "ClickPad" "boolean"
              Whether  the  device  is  a  click  pad.  A click pad device has
              button(s) integrated into the touchpad surface.  The  user  must
              press  downward  on  the touchpad in order to generated a button
              press. This property may be set automatically  if  a  click  pad
              device  is detected at initialization time. Property: "Synaptics
              ClickPad""")
    middle_button_timeout = NProp(  # {{{1 = 280
            "Synaptics Middle Button Timeout",
            PropFormat(("# MiddleButtonTimeout", "{:d}")),
            "")  # = 280
    two_finger_pressure = NProp(  # {{{1 = 281
            "Synaptics Two-Finger Pressure",  # = 281
            PropFormat(("EmulateTwoFingerMinZ", "{:d}")),
            '''Option "EmulateTwoFingerMinZ" "integer"
              For  touchpads not capable of detecting multiple fingers but are
              capable of detecting finger pressure and width, this sets the  Z
              pressure threshold.  When both Z pressure and W width thresholds
              are crossed, a two finger press will be emulated. This  defaults
              to  a  value that disables emulation on touchpads with real two-
              finger detection and defaults to a value that enables  emulation
              on  remaining touchpads that support pressure and width support.
              Property: "Synaptics Two-Finger Pressure"j
            ''')
    two_finger_width = NProp("Synaptics Two-Finger Width",  # = 282 {{{1
                             PropFormat(("EmulateTwoFingerMinW", "{:d}"),),
                             '''Option "EmulateTwoFingerMinW" "integer"
              For touchpads not capable of detecting multiple fingers but  are
              capable  of detecting finger width and pressure, this sets the W
              width threshold.  When both W width and  Z  pressure  thresholds
              are  crossed,  a two finger press will be emulated. This feature
              works best with  (PalmDetect)  off.  Property:  "Synaptics  Two-
              Finger Width"
        ''')
    scrdist = NProp("Synaptics Scrolling Distance",  # {{{1 = 283
                    PropFormat(("VertScrollDelta", "{:d}"),
                               ("HorizScrollDelta", "{:d}")),
                    '''Option "VertScrollDelta" "integer"
              Move  distance  of  the  finger  for  a  scroll event. Property:
              "Synaptics Scrolling Distance"

       Option "HorizScrollDelta" "integer"
              Move distance of  the  finger  for  a  scroll  event.  Property:
              "Synaptics Scrolling Distance"
        ''')
    edgescrs = NProp("Synaptics Edge Scrolling",  # {{{1 = 284
                     PropFormat(("VertEdgeScroll", "{:b}"),
                                ("HorizEdgeScroll", "{:b}"),
                                ("CornerCoasting", " {:b}")),
                     '''Option "VertEdgeScroll" "boolean"
              Enable vertical scrolling when dragging along  the  right  edge.
              Property: "Synaptics Edge Scrolling"

       Option "HorizEdgeScroll" "boolean"
              Enable horizontal scrolling when dragging along the bottom edge.
              Property: "Synaptics Edge Scrolling"

       Option "CornerCoasting" "boolean"
              Enable edge scrolling to continue while the finger stays  in  an
              edge corner.  Property: "Synaptics Edge Scrolling"
        ''')
    two_finger_scrolling = NProp("Synaptics Two-Finger Scrolling",  # {{{1 =285
                                 PropFormat(
                                    ("VertTwoFingerScroll", "{:b}"),
                                    ("HorizTwoFingerScroll", "{:b}")),
                                 '''
       Option "VertTwoFingerScroll" "boolean"
              Enable   vertical  scrolling  when  dragging  with  two  fingers
              anywhere  on  the  touchpad.  Property:  "Synaptics   Two-Finger
              Scrolling"

       Option "HorizTwoFingerScroll" "boolean"
              Enable  horizontal  scrolling  when  dragging  with  two fingers
              anywhere  on  the  touchpad.  Property:  "Synaptics   Two-Finger
              Scrolling"
        ''')
    move_speed = NProp("Synaptics Move Speed",  # {{{1 = 286
                       PropFormat(("MinSpeed", "{:f}", "3"),
                                  ("MaxSpeed", "{:f}", "3"),
                                  ("AccelFactor", "{:f}", "3"),
                                  ("TrackstickSpeed", "{:f}", "3")),
                       '''Option "MinSpeed" "float"
              Minimum speed factor. Property: "Synaptics Move Speed"

       Option "MaxSpeed" "float"
              Maximum speed factor. Property: "Synaptics Move Speed"

       Option "AccelFactor" "float"
              Acceleration  factor  for  normal  pointer  movements. Property:
              "Synaptics Move Speed"

       Option "TrackstickSpeed" "float"
              Speed  scale  when  in  trackstick  emulation  mode.   Property:
              "Synaptics Move Speed"
        ''')
    off = NProp("Synaptics Off",  # {{{1 = 287
                PropFormat(("TouchpadOff", "{:d}"), ),
                '''Option "TouchpadOff" "integer"
              Switch off the touchpad.  Valid values are:

              0   Touchpad is enabled
              1   Touchpad is switched off
              2   Only tapping and scrolling is switched off
              Property: "Synaptics Off"
        ''')
    locked_drags = NProp("Synaptics Locked Drags (",  # {{{1 = 288 {{{1
                         PropFormat(("LockedDrags", "{:b}"), ),
                         '''Option "LockedDrags" "boolean"
              If off, a tap-and-drag gesture ends when you release the finger.
              If on, the gesture is active until you tap  a  second  time,  or
              until  LockedDragTimeout  expires.  Property:  "Synaptics Locked
              Drags"
        ''')
    locked_drags_timeout = NProp("Synaptics Locked Drags Timeout",  # {{{1 =289
                                 PropFormat(
                                    ("LockedDragTimeout", "{:d}"),),
                                 '''
        Option "LockedDragTimeout" "integer"
              This parameter specifies how long it takes (in milliseconds) for
              the  LockedDrags  mode  to be automatically turned off after the
              finger is  released  from  the  touchpad.  Property:  "Synaptics
              Locked Drags Timeout"
        ''')
    tap_action = NProp("Synaptics Tap Action",  # {{{1 = 290
                       PropFormat(("RTCornerButton", "{:d}"),
                                  ("RBCornerButton", "{:d}"),
                                  ("LTCornerButton", "{:d}"),
                                  ("LBCornerButton", "{:d}"),
                                  ("TapButton1", "{:d}"),
                                  ("TapButton2", "{:d}"),
                                  ("TapButton3", "{:d}")),
                       """Property: "Synaptics Tap Action"

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
        """)
    click_action = NProp("Synaptics Click Action",  # {{{1 = 291
                         PropFormat(("ClickFinger1", "{:d}"),
                                    ("ClickFinger2", "{:d}"),
                                    ("ClickFinger3", "{:d}")),
                         """Property: "Synaptics Click Action"
        Which mouse button  is  reported  when left-clicking with one,
        two or three fingers. Set to 0 to disable.

        Option "ClickFinger1" "integer"
        Option "ClickFinger2" "integer"
        Option "ClickFinger3" "integer" """)
    cirscr = NProp("Synaptics Circular Scrolling (",  # {{{1 = 292 {{{1
                   PropFormat(("CircularScrolling", "{:b}"), ),
                   '''Option "CircularScrolling" "boolean"
              If on, circular scrolling is used. Property: "Synaptics Circular
              Scrolling"
        ''')
    cirdis = NProp("Synaptics Circular Scrolling Distance",  # {{{1 = 293
                   PropFormat(("CircScrollDelta", "{:f}", "3"), ),
                   '''Option "CircScrollDelta" "float"
              Move angle (radians) of  finger  to  generate  a  scroll  event.
              Property: "Synaptics Circular Scrolling Distance"
        ''')
    cirtrg = NProp("Synaptics Circular Scrolling Trigger",  # {{{1 = 294
                   PropFormat(("CircScrollTrigger", "{:d}"), ),
                   '''Option "CircScrollTrigger" "integer"
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
        ''')
    cirpad = NProp("Synaptics Circular Pad",  # {{{1 = 295
                   PropFormat(("CircularPad", "{:b}"), ),
                   '''Option "CircularPad" "boolean"
              Instead  of  being a rectangle, the edge is the ellipse enclosed
              by  the  Left/Right/Top/BottomEdge  parameters.   For   circular
              touchpads. Property: "Synaptics Circular Pad"
        ''')
    palm_detection = NProp("Synaptics Palm Detection",  # {{{1 = 296
                           PropFormat(("PalmDetect", "{:b}"), ),
                           '''
        Option "PalmDetect" "boolean"
              If  palm  detection  should  be  enabled.   Note  that this also
              requires hardware/firmware support from the touchpad.  Property:
              "Synaptics Palm Detection"
        ''')
    palm_dimensions = NProp("Synaptics Palm Dimensions",  # {{{1 = 297
                            PropFormat(("PalmMinWidth", "{:d}"),
                                       ("PalmMinZ", "{:d}")),
                            '''Option "PalmMinWidth" "integer"
              Minimum  finger  width  at  which  touch  is  considered a palm.
              Property: "Synaptics Palm Dimensions"

       Option "PalmMinZ" "integer"
              Minimum finger pressure at which touch  is  considered  a  palm.
              Property: "Synaptics Palm Dimensions"
        ''')
    coasting_speed = NProp("Synaptics Coasting Speed",  # {{{1 = 298
                           PropFormat(("CoastingSpeed", "{:f}", "3"),
                                      ("CoastingFriction", "{:f}", "3")),
                           '''Option "CoastingSpeed" "float"
              Your  finger  needs  to  produce this many scrolls per second in
              order to start coasting.  The default is 20 which should prevent
              you   from   starting   coasting  unintentionally.   0  disables
              coasting. Property: "Synaptics Coasting Speed"

       Option "CoastingFriction" "float"
              Number  of  scrolls/second²  to  decrease  the  coasting  speed.
              Default is 50.  Property: "Synaptics Coasting Speed"
        ''')
    pressure_motion = NProp("Synaptics Pressure Motion (",  # = 299 {{{1
                            PropFormat(("PressureMotionMinZ", "{:d}"),
                                       ("PressureMotionMaxZ", "{:d}")),
                            '''Option "PressureMotionMinZ" "integer"
              Finger  pressure  at  which  minimum  pressure  motion factor is
              applied. Property: "Synaptics Pressure Motion"

       Option "PressureMotionMaxZ" "integer"
              Finger pressure at  which  maximum  pressure  motion  factor  is
              applied.  Property: "Synaptics Pressure Motion"
        ''')
    pressure_motion_factor = NProp(  # {{{1
        "Synaptics Pressure Motion Factor",  # = 300(int) -> 304(float)
        PropFormat(("PressureMotionMinFactor", "{:f}"),
                   ("PressureMotionMaxFactor", "{:f}")),
        # PropFormat(("PressureMotionMinFactor", "{:d}"),
        #            ("PressureMotionMaxFactor", "{:d}")),
        '''Option "PressureMotionMinFactor" "integer"
              Lowest  setting for pressure motion factor. Property: "Synaptics
              Pressure Motion Factor"

       Option "PressureMotionMaxFactor" "integer"
              Greatest  setting  for   pressure   motion   factor.   Property:
              "Synaptics Pressure Motion Factor"
        ''')
    resolution_detect = NProp("Synaptics Resolution Detect",  # {{{1 = 301
                              PropFormat(("ResolutionDetect", "{:b}"), ),
                              '''
        Option "ResolutionDetect" "boolean" {{{
              Allow or  prevent  the  synaptics
              driver  from reporting the size of the touchpad to the X server.
              The X server normally uses this information to  scale  movements
              so  that  touchpad movement corresponds visually to mouse cursor
              movements on the screen.  However, in some rare cases where  the
              touchpad  height/width ratio is significantly different from the
              laptop, it can cause the mouse cursor to skip pixels in the X or
              Y  axis.   This  option  allows disabling this scaling behavior,
              which  can  provide  smoother  mouse  movement  in  such  cases.
              Property: "Synaptics Resolution Detect"
        ''')
    grab_event_device = NProp("Synaptics Grab Event Device",  # {{{1 = 302
                              PropFormat(("GrabEventDevice", "{:b}"), ),
                              '''Option "GrabEventDevice" "boolean"
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
        ''')
    gestures = NProp("Synaptics Gestures",  # {{{1 = 303
                     PropFormat(("TapAndDragGesture", "{:b}"), ),
                     '''Option "TapAndDragGesture" "boolean"
              Switch  on/off  the  tap-and-drag  gesture.   This gesture is an
              alternative  way  of  dragging.   It  is  performed  by  tapping
              (touching  and  releasing  the  finger), then touching again and
              moving the finger on the touchpad.  The gesture  is  enabled  by
              default  and  can  be  disabled by setting the TapAndDragGesture
              option to false. Property: "Synaptics Gestures"
        ''')
    capabilities = NProp("Synaptics Capabilities",  # {{{1 = 304
                         PropFormat((
                                 "Capabilities",
                                 "{:d} {:d} {:d} {:d} {:d} {:d} {:d}"), ),
                         "")
    pad_resolution = NProp("Synaptics Pad Resolution",  # {{{1
                           # PropFormat(("ResolutionDetect", "{:d} {:d"}), ),
                           None,  # read-only
                           """Synaptics Pad Resolution
                              32 bit unsigned, 2 values (read-only),
                              vertical, horizontal in units/millimeter.
                           """)  # = 305
    area = NProp("Synaptics Area",  # {{{1
                 PropFormat(("AreaLeftEdge", "{:d}"),
                            ("AreaRightEdge", "{:d}"),
                            ("AreaTopEdge", "{:d}"),
                            ("AreaBottomEdge", "{:d}")),
                 "")  # = 306
    softareas = NProp("Synaptics Soft Button Areas",  # {{{1 = 307
                      PropFormat((
                          "SoftButtonAreas",
                          "{:P} {:P} {:P} {:P} {:P} {:P} {:P} {:P}")),
                      '''
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
        ''')
    noise_cancellation = NProp("Synaptics Noise Cancellation",  # {{{1 = 308
                               PropFormat(("HorizonHysterisis", "{:d}"),
                                          ("VerticalHysterisis", "{:d}")),
                               '''Noise cancellation
       The synaptics has a built-in noise cancellation  based  on  hysteresis.
       This means that incoming coordinates actually shift a box of predefined
       dimensions such that it covers the incoming coordinate,  and  only  the
       boxes  own  center is used as input. Obviously, the smaller the box the
       better,  but  the  likelyhood  of  noise  motion  coming  through  also
       increases.
        ''')
    device_product_id = NProp("Device Product ID", None, "")  # {{{1 = 267
    device_node = NProp("Device Node", None,  # {{{1 = 266
                        '''Option "Device" "string"
              This  option  specifies the device file in your "/dev" directory
              which will be used to access the physical device.  Normally  you
              should  use  something like "/dev/input/eventX", where X is some
              integer.
        ''')

    __not_implemented_options__ = {  # {{{1
        1: ''' {{{2
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
        97: '''
        97: PropFormat(("VertResolution", "{:d}"),
                       ("HorizResolution", "{:d}")),
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
        96: PropFormat(("AreaLeftEdge", "{:d}"),
                       ("AreaRightEdge", "{:d}"),
                       ("AreaTopEdge", "{:d}"),
                       ("AreaBottomEdge", "{:d}")),
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
    }

    @classmethod  # get_touchpad_id {{{1
    def get_touchpad_id(cls):
        # type: () -> Text
        _id = ""
        for line in common.check_output(["xinput"]).splitlines():
            if "Touchpad" not in line:
                continue
            seq = line.split("\t")
            for src in seq:
                if not src.startswith("id="):
                    continue
                _id = src.replace("id=", "")
                return _id
        return ""

    @classmethod  # auto_id {{{1
    def auto_id(cls, verbose=False):
        # type: (bool) -> int
        _id = cls.get_touchpad_id()
        cmd = ["xinput", "list-props", _id]
        for p, v in cls.props():
            v.prop_id = -1  # clear id
        ret = 0
        for line in common.check_output(cmd).splitlines():
            for p, v in cls.props():
                if v.key not in line:
                    continue
                mo = re.search(r"([0-9]+)", line)
                if not mo:
                    continue
                _id = mo.group(1)
                v.prop_id = int(_id)
                info("id:{:3} as {} - {}".format(_id, p, v.key))
                num = NProp1804.parse_props(v, line, verbose)
                if num != len(v.vals):
                    warn("id:{:3}, {} - {}".format(_id, num, len(v.vals)))
                ret += 1
                break
            else:
                if verbose:
                    print("???????:" + line)
        if verbose:
            for p, key in cls.props():
                if key.prop_id > 0:
                    print("{:3} was loaded as {}".format(getattr(cls, p), p))
                else:
                    print("{} was not found...".format(p))
        return ret

    @classmethod
    def parse_props(cls, self, src, verbose=False):  # {{{1
        # type: (NProp, Text, bool) -> int
        if len(self.fmts) < 1:
            return 0
        r = ":".join(src.split(":")[1:])
        r = r.replace("\t", " ")
        seq = r.split(",")
        # print(seq)
        n1, n2 = len(seq), len(self.vals)
        if n1 != n2:
            warn("{} != {}".format(n1, n2))
        for n, i in enumerate(seq):
            self.vals[n] = i.strip()
        return len(seq)

    @classmethod
    def textprops(cls):  # cls {{{2
        # type: () -> Text
        ret = ""
        for k, v in cls.__dict__.items():
            if not isinstance(v, NProp):
                continue
            name = v.key.replace(" (", "")
            ret += "\n{:20s} = {:3d}".format(name, v.prop_id)
        if len(ret) > 0:
            ret = ret[1:]
        return ret

    @classmethod  # props_copy {{{1
    def props_copy(cls, nprop):
        # type: (Type[NProp]) -> None
        for k, v in cls.__dict__.items():
            if not isinstance(v, NProp):
                continue
            setattr(nprop, k, v)


# main {{{1
def main():  # {{{1
    # type: () -> int
    _id = NProp1804.get_touchpad_id()
    if _id != "":
        print("detected touchpad as id=" + _id)
        # os.system("xinput list-props " + _id)
        NProp1804.auto_id(True)
    else:
        print("does not detected touchpad")
    return 0


if __name__ == "__main__":  # end of file {{{1
    main()
# vi: ft=python:et:fdm=marker:nowrap:tw=80
