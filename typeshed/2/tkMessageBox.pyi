# tk common message boxes
#
# this module provides an interface to the native message boxes
# available in Tk 4.2 and newer.
#
# written by Fredrik Lundh, May 1997
#

#
# options (all have default values):
#
# - default: which button to make default (one of the reply codes)
#
# - icon: which icon to display (see below)
#
# - message: the message to display
#
# - parent: which window to place the dialog on top of
#
# - title: dialog title
#
# - type: dialog type; that is, which buttons to display (see below)
#
from typing import Optional
from tkCommonDialog import Dialog

#
# constants

# icons
ERROR = "error"
INFO = "info"
QUESTION = "question"
WARNING = "warning"

# types
ABORTRETRYIGNORE = "abortretryignore"
OK = "ok"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"

# replies
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
OK = "ok"
CANCEL = "cancel"
YES = "yes"
NO = "no"


#
# message dialog class

class Message(Dialog):
    command  = ...  # type: Optional[str]


#
# convenience stuff

# Rename _icon and _type options to allow overriding them in options
def _show(title=None, message=None, _icon=None, _type=None, **options
          ) -> str: ...
def showinfo(title=None, message=None, **options) -> str: ...
def showwarning(title=None, message=None, **options) -> str: ...
def showerror(title=None, message=None, **options) -> str: ...
def askquestion(title=None, message=None, **options) -> str: ...
def askokcancel(title=None, message=None, **options) -> bool: ...
def askyesno(title=None, message=None, **options) -> bool: ...
def askyesnocancel(title=None, message=None, **options) -> Optional[bool]: ...
def askretrycancel(title=None, message=None, **options) -> bool: ...


# --------------------------------------------------------------------
# test stuff

