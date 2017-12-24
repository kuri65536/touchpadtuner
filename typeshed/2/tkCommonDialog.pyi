# base class for tk common dialogues
#
# this module provides a base class for accessing the common
# dialogues available in Tk 4.2 and newer.  use tkFileDialog,
# tkColorChooser, and tkMessageBox to access the individual
# dialogs.
#
# written by Fredrik Lundh, May 1997
#
from typing import Any, Optional
from Tkinter import *

class Dialog:

    command  = ...  # type: Optional[str]

    def __init__(self, master=None, **options) -> None: ...
    def _fixoptions(self) -> None:
        pass # hook

    def _fixresult(self, widget, result) -> Any:
        return result # hook

    def show(self, **options) -> str: ...
