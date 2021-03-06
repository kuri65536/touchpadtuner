from typing import Any, Dict, Iterable, List, Tuple, Optional, Union
from Tkconstants import *  # noqa: F403

__version__ = "$Revision: 81008 $"
tkinter = ... # b/w compat for export
TclError = ...
wantobjects = 1
TkVersion = ...  # type: float
TclVersion = ...  # type: float
READABLE = ...  # _tkinter.READABLE
WRITABLE = ...  # _tkinter.WRITABLE
EXCEPTION = ...  # _tkinter.EXCEPTION
_magic_re = ...  # type: Any   ## re.compile(r'([\\{}])')
_space_re = ...  # type: Any   ## re.compile(r'([\s])')

def _join(value): ...
def _stringify(value) -> str: ...
def _flatten(tuple) -> Iterable[Any]: ...
def _cnfmerge(cnfs): ...
def _splitdict(tk, v, cut_minus=True, conv=None) -> Dict[str, Any]: ...

class Event: ...

_support_default_root = 1
_default_root = None

def NoDefaultRoot(): ...
def _tkerror(err): ...
def _exit(code=0): ...

_varnum = 0
class Variable:
    _default = ...  # type: Any
    _tclCommands = None
    def __init__(self, master=None, value=None, name=None) -> None: ...
    def __del__(self): ...
    def __str__(self): ...
    def set(self, value) -> Any: ...
    def get(self) -> Any: ...
    def trace_variable(self, mode, callback) -> str: ...
    trace = trace_variable
    def trace_vdelete(self, mode, cbname): ...
    def trace_vinfo(self): ...
    def __eq__(self, other): ...

class StringVar(Variable):
    def __init__(self, master=None, value=None, name=None) -> None: ...
    def get(self) -> str: ...

class IntVar(Variable):
    _default = 0
    def __init__(self, master=None, value=None, name=None) -> None: ...
    def set(self, value) -> Any: ...
    def get(self) -> int: ...

class DoubleVar(Variable):
    _default = 0.0
    def __init__(self, master=None, value=None, name=None) -> None: ...
    def get(self) -> float: ...

class BooleanVar(Variable):
    _default = False
    def __init__(self, master=None, value=None, name=None) -> None: ...
    def set(self, value):  # type: (bool) -> Any
        ...

    def get(self) -> bool: ...

def mainloop(n=0) -> None: ...

getint = int

getdouble = float

def getboolean(s) -> bool: ...

# Methods defined on both toplevel and interior widgets
class Misc:
    _tclCommands = None
    def destroy(self): ...
    def deletecommand(self, name): ...
    def tk_strictMotif(self, boolean=None): ...
    def tk_bisque(self): ...
    def tk_setPalette(self, *args, **kw) -> None: ...
    def tk_menuBar(self, *args) -> None: ...
    def wait_variable(self, name='PY_VAR') -> None: ...
    waitvar = wait_variable # XXX b/w compat
    def wait_window(self, window=None) -> None: ...
    def wait_visibility(self, window=None) -> None: ...
    def setvar(self, name='PY_VAR', value='1'): ...
    def getvar(self, name='PY_VAR'): ...
    getint = int
    getdouble = float
    def getboolean(self, s): ...
    def focus_set(self): ...
    focus = focus_set # XXX b/w compat?
    def focus_force(self): ...
    def focus_get(self): ...
    def focus_displayof(self): ...
    def focus_lastfor(self): ...
    def tk_focusFollowsMouse(self): ...
    def tk_focusNext(self): ...
    def tk_focusPrev(self): ...
    def after(self, ms, func=None, *args) -> int: ...
    def after_idle(self, func, *args) -> int: ...
    def after_cancel(self, id) -> None: ...
    def bell(self, displayof=0) -> None: ...

    # Clipboard handling:
    def clipboard_get(self, **kw) -> str: ...
    def clipboard_clear(self, **kw) -> None: ...
    def clipboard_append(self, string, **kw) -> None: ...
    def grab_current(self) -> Optional[Widget]: ...
    def grab_release(self) -> None: ...
    def grab_set(self) -> None: ...
    def grab_set_global(self) -> None: ...
    def grab_status(self) -> Optional[str]: ...
    def option_add(self, pattern, value, priority = None): ...
    def option_clear(self): ...
    def option_get(self, name, className): ...
    def option_readfile(self, fileName, priority = None): ...
    def selection_clear(self, **kw) -> None: ...
    def selection_get(self, **kw) -> str: ...
    def selection_handle(self, command, **kw) -> None: ...
    def selection_own(self, **kw) -> None: ...
    def selection_own_get(self, **kw) -> Optional[Widget]: ...
    def send(self, interp, cmd, *args) -> Any: ...
    def lower(self, belowThis=None) -> None: ...
    def tkraise(self, aboveThis=None) -> None: ...
    lift = tkraise
    def colormodel(self, value=None): ...
    def winfo_atom(self, name, displayof=0): ...
    def winfo_atomname(self, id, displayof=0): ...
    def winfo_cells(self): ...
    def winfo_children(self): ...

    def winfo_class(self): ...
    def winfo_colormapfull(self): ...
    def winfo_containing(self, rootX, rootY, displayof=0): ...
    def winfo_depth(self): ...
    def winfo_exists(self): ...
    def winfo_fpixels(self, number): ...
    def winfo_geometry(self): ...
    def winfo_height(self): ...
    def winfo_id(self): ...
    def winfo_interps(self, displayof=0): ...
    def winfo_ismapped(self): ...
    def winfo_manager(self): ...
    def winfo_name(self): ...
    def winfo_parent(self): ...
    def winfo_pathname(self, id, displayof=0): ...
    def winfo_pixels(self, number): ...
    def winfo_pointerx(self): ...
    def winfo_pointerxy(self): ...
    def winfo_pointery(self): ...
    def winfo_reqheight(self): ...
    def winfo_reqwidth(self): ...
    def winfo_rgb(self, color): ...
    def winfo_rootx(self): ...
    def winfo_rooty(self): ...
    def winfo_screen(self): ...
    def winfo_screencells(self): ...
    def winfo_screendepth(self): ...
    def winfo_screenheight(self): ...
    def winfo_screenmmheight(self): ...
    def winfo_screenmmwidth(self): ...
    def winfo_screenvisual(self): ...
    def winfo_screenwidth(self): ...
    def winfo_server(self): ...
    def winfo_toplevel(self): ...
    def winfo_viewable(self): ...
    def winfo_visual(self): ...
    def winfo_visualid(self): ...
    def winfo_visualsavailable(self, includeids=0): ...
    def __winfo_parseitem(self, t): ...
    def __winfo_getint(self, x): ...
    def winfo_vrootheight(self): ...
    def winfo_vrootwidth(self): ...
    def winfo_vrootx(self): ...
    def winfo_vrooty(self): ...
    def winfo_width(self): ...
    def winfo_x(self): ...
    def winfo_y(self): ...
    def update(self): ...
    def update_idletasks(self): ...
    def bindtags(self, tagList=None): ...
    def _bind(self, what, sequence, func, add, needcleanup=1
              ) -> Union[str, List[str]]: ...
    def bind(self, sequence=None, func=None, add=None
             ) -> Union[str, List[str]]: ...  # same as _bind
    def unbind(self, sequence, funcid=None): ...
    def bind_all(self, sequence=None, func=None, add=None): ...
    def unbind_all(self, sequence): ...
    def bind_class(self, className, sequence=None, func=None, add=None): ...
    def unbind_class(self, className, sequence): ...
    def mainloop(self, n=0) -> None: ...
    def quit(self) -> None: ...
    def _getints(self, string): ...
    def _getdoubles(self, string): ...
    def _getboolean(self, string): ...
    def _displayof(self, displayof): ...
    @property
    def _windowingsystem(self): ...
    def _options(self, cnf, kw = None) -> Iterable[str]: ...
    def nametowidget(self, name) -> Widget: ...
    _nametowidget = nametowidget
    def _register(self, func, subst=None, needcleanup=1): ...
    register = _register
    def _root(self): ...
    _subst_format = ('%#', '%b', '%f', '%h', '%k',
             '%s', '%t', '%w', '%x', '%y',
             '%A', '%E', '%K', '%N', '%W', '%T', '%X', '%Y', '%D')
    _subst_format_str = " ".join(_subst_format)
    def _substitute(self, *args) -> Tuple[Event]: ...
    def _report_exception(self): ...
    def _getconfigure(self, *args) -> Dict[str, Iterable[str]]: ...
    def _getconfigure1(self, *args) -> Iterable[str]: ...
    def _configure(self, cmd, cnf, kw
                   ) -> Union[Dict[str, Iterable[str]],
                              Iterable[str]]: ...
    def configure(self, cnf=None, **kw) -> None: ...
    config = configure
    def cget(self, key) -> Any: ...
    __getitem__ = cget
    def __setitem__(self, key, value) -> None: ...
    # def __contains__(self, key):
    #     raise TypeError("Tkinter objects don't support 'in' tests.")
    def keys(self): ...
    def __str__(self): ...
    # Pack methods that apply to the master
    _noarg_ = ['_noarg_']
    def pack_propagate(self, flag=_noarg_): ...
    propagate = pack_propagate
    def pack_slaves(self): ...
    # slaves = pack_slaves
    def place_slaves(self): ...
    def grid_bbox(self, column=None, row=None, col2=None, row2=None
                  ) -> Optional[int]: ...

    bbox = grid_bbox

    def _gridconvvalue(self, value) -> Any: ...
    def _grid_configure(self, command, index, cnf, kw) -> Any: ...
    def grid_columnconfigure(self, index, cnf={}, **kw) -> Any: ...
    columnconfigure = grid_columnconfigure
    def grid_location(self, x, y): ...
    def grid_propagate(self, flag=_noarg_): ...
    def grid_rowconfigure(self, index, cnf={}, **kw): ...
    rowconfigure = grid_rowconfigure
    def grid_size(self): ...
    size = grid_size
    def grid_slaves(self, row=None, column=None): ...

    # Support for the "event" command, new in Tk 4.2.
    # By Case Roole.

    def event_add(self, virtual, *sequences) -> None: ...
    def event_delete(self, virtual, *sequences) -> None: ...
    def event_generate(self, sequence, **kw) -> None: ...
    def event_info(self, virtual=None) -> Iterable[str]: ...

    # Image related commands

    def image_names(self): ...
    def image_types(self): ...


class CallWrapper:
    """Internal class. Stores function to call when some user
    defined Tcl function is called e.g. after an event occurred."""
    def __init__(self, func, subst, widget) -> None: ...
    def __call__(self, *args): ...


class XView:
    def xview(self, *args): ...
    def xview_moveto(self, fraction): ...
    def xview_scroll(self, number, what): ...


class YView:
    def yview(self, *args): ...
    def yview_moveto(self, fraction): ...
    def yview_scroll(self, number, what): ...


class Wm:
    def wm_aspect(self,
              minNumer=None, minDenom=None,
              maxNumer=None, maxDenom=None): ...
    aspect = wm_aspect

    def wm_attributes(self, *args): ...
    attributes=wm_attributes

    def wm_client(self, name=None): ...
    client = wm_client
    def wm_colormapwindows(self, *wlist): ...
    colormapwindows = wm_colormapwindows
    def wm_command(self, value=None): ...
    command = wm_command
    def wm_deiconify(self): ...
    deiconify = wm_deiconify
    def wm_focusmodel(self, model=None): ...
    focusmodel = wm_focusmodel
    def wm_frame(self): ...
    frame = wm_frame
    def wm_geometry(self, newGeometry=None): ...
    geometry = wm_geometry
    def wm_grid(self, w): ...
    grid = wm_grid
    def wm_group(self, pathName=None): ...
    group = wm_group
    def wm_iconbitmap(self, bitmap=None, default=None): ...
    iconbitmap = wm_iconbitmap
    def wm_iconify(self): ...
    iconify = wm_iconify
    def wm_iconmask(self, bitmap=None): ...
    iconmask = wm_iconmask
    def wm_iconname(self, newName=None): ...
    iconname = wm_iconname
    def wm_iconposition(self, x=None, y=None): ...
    iconposition = wm_iconposition
    def wm_iconwindow(self, pathName=None): ...
    iconwindow = wm_iconwindow
    def wm_maxsize(self, width=None, height=None): ...
    maxsize = wm_maxsize
    def wm_minsize(self, width=None, height=None): ...
    minsize = wm_minsize
    def wm_overrideredirect(self, boolean=None): ...
    overrideredirect = wm_overrideredirect
    def wm_positionfrom(self, who=None): ...
    positionfrom = wm_positionfrom
    def wm_protocol(self, name=None, func=None): ...
    protocol = wm_protocol
    def wm_resizable(self, width=None, height=None): ...
    resizable = wm_resizable
    def wm_sizefrom(self, who=None): ...
    sizefrom = wm_sizefrom
    def wm_state(self, newstate=None): ...
    state = wm_state
    def wm_title(self, string=None) -> str: ...
    title = wm_title
    def wm_transient(self, master=None): ...
    transient = wm_transient
    def wm_withdraw(self): ...
    withdraw = wm_withdraw


class Tk(Misc, Wm):
    _w = '.'
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None) -> None: ...
    def loadtk(self): ...
    def _loadtk(self) -> None: ...
    def destroy(self) -> None: ...
    def readprofile(self, baseName, className) -> None: ...
    def report_callback_exception(self, exc, val, tb) -> None: ...
    def __getattr__(self, attr) -> Any: ...


def Tcl(screenName=None, baseName=None, className='Tk', useTk=0):
    return Tk(screenName, baseName, className, useTk)

class Pack:
    def pack_configure(self, cnf={}, **kw) -> None: ...
    pack = ...  # type: Any
    configure = ...  # type: Any  ## config = pack_configure
    def pack_forget(self) -> None: ...
    forget = pack_forget
    def pack_info(self): ...
    info = pack_info
    propagate = pack_propagate = Misc.pack_propagate
    slaves = ...  # type: Any  ## pack_slaves = Misc.pack_slaves

class Place:
    def place_configure(self, cnf={}, **kw) -> None: ...
    place = ...  # type: Any
    configure = ...  # type: Any  ## config = place_configure
    def place_forget(self) -> None: ...
    forget = place_forget
    def place_info(self) -> Dict[str, Any]: ...
    info = place_info
    slaves = ...  # type: Any  ## place_slaves = Misc.place_slaves

class Grid:
    def grid_configure(self, cnf={}, **kw) -> None: ...
    grid = ...  # type: Any
    configure = ...  # type: Any  ## config = grid_configure
    bbox = grid_bbox = Misc.grid_bbox
    columnconfigure = grid_columnconfigure = Misc.grid_columnconfigure
    def grid_forget(self) -> None: ...
    forget = grid_forget
    def grid_remove(self) -> None: ...
    def grid_info(self) -> Dict[str, Any]: ...
    info = grid_info
    location = grid_location = Misc.grid_location
    propagate = grid_propagate = Misc.grid_propagate
    rowconfigure = grid_rowconfigure = Misc.grid_rowconfigure
    size = grid_size = Misc.grid_size
    slaves = ...  # type: Any  ## grid_slaves = Misc.grid_slaves

class BaseWidget(Misc):
    def _setup(self, master, cnf) -> None: ...
    def __init__(self, master, widgetName, cnf={}, kw={}, extra=()
                 ) -> None: ...
    def destroy(self) -> None: ...
    def _do(self, name, args=()):
        # XXX Obsolete -- better use self.tk.call directly!
        return self.tk.call((self._w, name) + args)

class Widget(BaseWidget, Pack, Place, Grid):
    pass

class Toplevel(BaseWidget, Wm):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Button(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def tkButtonEnter(self, *dummy) -> None: ...
    def tkButtonLeave(self, *dummy) -> None: ...
    def tkButtonDown(self, *dummy) -> None: ...
    def tkButtonUp(self, *dummy) -> None: ...
    def tkButtonInvoke(self, *dummy) -> None: ...
    def flash(self) -> None: ...
    def invoke(self) -> str: ...

# Indices:
def AtEnd(): ...
def AtInsert(*args): ...
def AtSelFirst(): ...
def AtSelLast(): ...
def At(x, y=None): ...

class Canvas(Widget, XView, YView):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def addtag(self, *args): ...
    def addtag_above(self, newtag, tagOrId): ...
    def addtag_all(self, newtag): ...
    def addtag_below(self, newtag, tagOrId): ...
    def addtag_closest(self, newtag, x, y, halo=None, start=None): ...
    def addtag_enclosed(self, newtag, x1, y1, x2, y2): ...
    def addtag_overlapping(self, newtag, x1, y1, x2, y2): ...
    def addtag_withtag(self, newtag, tagOrId): ...
    def bbox(self, *args): ...
    def tag_unbind(self, tagOrId, sequence, funcid=None): ...
    def tag_bind(self, tagOrId, sequence=None, func=None, add=None): ...
    def canvasx(self, screenx, gridspacing=None): ...
    def canvasy(self, screeny, gridspacing=None): ...
    def coords(self, *args): ...
    def _create(self, itemType, args, kw): ...  # Args: (val, val, ..., cnf={})
    def create_arc(self, *args, **kw) -> int: ...
    def create_bitmap(self, *args, **kw) -> int: ...
    def create_image(self, *args, **kw) -> int: ...
    def create_line(self, *args, **kw) -> int: ...
    def create_oval(self, *args, **kw) -> int: ...
    def create_polygon(self, *args, **kw) -> int: ...
    def create_rectangle(self, *args, **kw) -> int: ...
    def create_text(self, *args, **kw) -> int: ...
    def create_window(self, *args, **kw) -> int: ...
    def dchars(self, *args): ...
    def delete(self, *args): ...
    def dtag(self, *args): ...
    def find(self, *args): ...
    def find_above(self, tagOrId): ...
    def find_all(self): ...
    def find_below(self, tagOrId): ...
    def find_closest(self, x, y, halo=None, start=None): ...
    def find_enclosed(self, x1, y1, x2, y2): ...
    def find_overlapping(self, x1, y1, x2, y2): ...
    def find_withtag(self, tagOrId): ...
    def focus(self, *args): ...
    def gettags(self, *args): ...
    def icursor(self, *args): ...
    def index(self, *args): ...
    def insert(self, *args): ...
    def itemcget(self, tagOrId, option): ...
    def itemconfigure(self, tagOrId, cnf=None, **kw): ...
    itemconfig = itemconfigure
    def tag_lower(self, *args): ...
    lower = tag_lower
    def move(self, *args): ...
    def postscript(self, cnf={}, **kw): ...
    def tag_raise(self, *args): ...
    lift = tkraise = tag_raise
    def scale(self, *args): ...
    def scan_mark(self, x, y): ...
    def scan_dragto(self, x, y, gain=10): ...
    def select_adjust(self, tagOrId, index): ...
    def select_clear(self): ...
    def select_from(self, tagOrId, index): ...
    def select_item(self): ...
    def select_to(self, tagOrId, index): ...
    def type(self, tagOrId): ...

class Checkbutton(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def deselect(self) -> None: ...
    def flash(self) -> None: ...
    def invoke(self) -> str: ...
    def select(self) -> None: ...
    def toggle(self) -> None: ...

class Entry(Widget, XView):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def delete(self, first, last=None) -> None: ...
    def get(self) -> str: ...
    def icursor(self, index) -> None: ...
    def index(self, index) -> int: ...
    def insert(self, index, string) -> None: ...
    def scan_mark(self, x) -> None: ...
    def scan_dragto(self, x) -> None: ...
    def selection_adjust(self, index) -> None: ...
    select_adjust = selection_adjust
    def selection_clear(self): ...
    select_clear = selection_clear
    def selection_from(self, index) -> None: ...
    select_from = selection_from
    def selection_present(self) -> bool: ...
    select_present = selection_present
    def selection_range(self, start, end) -> None: ...
    select_range = selection_range
    def selection_to(self, index) -> None: ...
    select_to = selection_to

class Frame(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Label(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Listbox(Widget, XView, YView):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def activate(self, index) -> None: ...
    def bbox(self, index): ...
    def curselection(self): ...
    def delete(self, first, last=None): ...
    def get(self, first, last=None): ...
    def index(self, index): ...
    def insert(self, index, *elements): ...
    def nearest(self, y): ...
    def scan_mark(self, x, y): ...
    def scan_dragto(self, x, y): ...
    def see(self, index): ...
    def selection_anchor(self, index): ...
    select_anchor = selection_anchor
    def selection_clear(self, first, last=None): ...
    select_clear = selection_clear
    def selection_includes(self, index): ...
    select_includes = selection_includes
    def selection_set(self, first, last=None): ...
    select_set = selection_set
    def size(self): ...
    def itemcget(self, index, option): ...
    def itemconfigure(self, index, cnf=None, **kw): ...
    itemconfig = itemconfigure

class Menu(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def tk_bindForTraversal(self): ...
    def tk_mbPost(self): ...
    def tk_mbUnpost(self): ...
    def tk_traverseToMenu(self, char): ...
    def tk_traverseWithinMenu(self, char): ...
    def tk_getMenuButtons(self): ...
    def tk_nextMenu(self, count): ...
    def tk_nextMenuEntry(self, count): ...
    def tk_invokeMenu(self): ...
    def tk_firstMenu(self): ...
    def tk_mbButtonDown(self): ...
    def tk_popup(self, x, y, entry=""): ...
    def activate(self, index): ...
    def add(self, itemType, cnf={}, **kw): ...
    def add_cascade(self, cnf={}, **kw): ...
    def add_checkbutton(self, cnf={}, **kw): ...
    def add_command(self, cnf={}, **kw): ...
    def add_radiobutton(self, cnf={}, **kw): ...
    def add_separator(self, cnf={}, **kw): ...
    def insert(self, index, itemType, cnf={}, **kw): ...
    def insert_cascade(self, index, cnf={}, **kw): ...
    def insert_checkbutton(self, index, cnf={}, **kw): ...
    def insert_command(self, index, cnf={}, **kw): ...
    def insert_radiobutton(self, index, cnf={}, **kw): ...
    def insert_separator(self, index, cnf={}, **kw): ...
    def delete(self, index1, index2=None): ...
    def entrycget(self, index, option): ...
    def entryconfigure(self, index, cnf=None, **kw): ...
    entryconfig = entryconfigure
    def index(self, index): ...
    def invoke(self, index): ...
    def post(self, x, y): ...
    def type(self, index): ...
    def unpost(self): ...
    def yposition(self, index): ...

class Menubutton(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Message(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Radiobutton(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def deselect(self): ...
    def flash(self): ...
    def invoke(self): ...
    def select(self): ...

class Scale(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def get(self) -> float: ...
    def set(self, value) -> None: ...
    def coords(self, value=None): ...
    def identify(self, x, y): ...

class Scrollbar(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def activate(self, index): ...
    def delta(self, deltax, deltay): ...
    def fraction(self, x, y): ...
    def identify(self, x, y): ...
    def get(self): ...
    def set(self, *args): ...

class Text(Widget, XView, YView):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def bbox(self, *args): ...
    def tk_textSelectTo(self, index): ...
    def tk_textBackspace(self): ...
    def tk_textIndexCloser(self, a, b, c): ...
    def tk_textResetAnchor(self, index): ...
    def compare(self, index1, op, index2): ...
    def debug(self, boolean=None): ...
    def delete(self, index1, index2=None) -> None: ...
    def dlineinfo(self, index): ...
    def dump(self, index1, index2=None, command=None, **kw
             ) -> List[Tuple[str, Any, int]]: ...
    def edit(self, *args): ...
    def edit_modified(self, arg=None): ...
    def edit_redo(self): ...
    def edit_reset(self): ...
    def edit_separator(self): ...
    def edit_undo(self): ...
    def get(self, index1, index2=None): ...
    def image_cget(self, index, option): ...
    def image_configure(self, index, cnf=None, **kw): ...
    def image_create(self, index, cnf={}, **kw): ...
    def image_names(self): ...
    def index(self, index): ...
    def insert(self, index, chars, *args) -> None: ...
    def mark_gravity(self, markName, direction=None): ...
    def mark_names(self): ...
    def mark_set(self, markName, index): ...
    def mark_unset(self, *markNames): ...
    def mark_next(self, index): ...
    def mark_previous(self, index): ...
    def scan_mark(self, x, y): ...
    def scan_dragto(self, x, y): ...
    def search(self, pattern, index, stopindex=None,
           forwards=None, backwards=None, exact=None,
           regexp=None, nocase=None, count=None, elide=None): ...
    def see(self, index): ...
    def tag_add(self, tagName, index1, *args): ...
    def tag_unbind(self, tagName, sequence, funcid=None): ...
    def tag_bind(self, tagName, sequence, func, add=None): ...
    def tag_cget(self, tagName, option): ...
    def tag_configure(self, tagName, cnf=None, **kw): ...
    tag_config = tag_configure
    def tag_delete(self, *tagNames): ...
    def tag_lower(self, tagName, belowThis=None): ...
    def tag_names(self, index=None): ...
    def tag_nextrange(self, tagName, index1, index2=None): ...
    def tag_prevrange(self, tagName, index1, index2=None): ...
    def tag_raise(self, tagName, aboveThis=None): ...
    def tag_ranges(self, tagName): ...
    def tag_remove(self, tagName, index1, index2=None): ...
    def window_cget(self, index, option): ...
    def window_configure(self, index, cnf=None, **kw): ...
    window_config = window_configure
    def window_create(self, index, cnf={}, **kw): ...
    def window_names(self): ...
    def yview_pickplace(self, *what): ...


class _setit:
    """Internal class. It wraps the command in the widget OptionMenu."""
    def __init__(self, var, value, callback=None) -> None: ...
    def __call__(self, *args):
        self.__var.set(self.__value)
        if self.__callback:
            self.__callback(self.__value, *args)

class OptionMenu(Menubutton):
    def __init__(self, master, variable, value, *values, **kwargs) -> None: ...
    def __getitem__(self, name): ...
    def destroy(self) -> None: ...

class Image:
    _last_id = 0
    def __init__(self, imgtype, name=None, cnf={}, master=None, **kw) -> None: ...
    def __str__(self) -> str: ...
    def __del__(self) -> None: ...
    def __setitem__(self, key, value): ...
    def __getitem__(self, key): ...
    def configure(self, **kw) -> None: ...
    config = configure
    def height(self) -> int: ...
    def type(self) -> str: ...
    def width(self) -> int: ...

class PhotoImage(Image):
    def __init__(self, name=None, cnf={}, master=None, **kw) -> None: ...
    def blank(self) -> None: ...
    def cget(self, option): ...
    def __getitem__(self, key): ...
    def copy(self): ...
    def zoom(self, x, y=''): ...
    def subsample(self, x, y=''): ...
    def get(self, x, y): ...
    def put(self, data, to=None) -> None: ...
    def write(self, filename, format=None, from_coords=None) -> None: ...

class BitmapImage(Image):
    def __init__(self, name=None, cnf={}, master=None, **kw) -> None: ...

def image_names() -> Iterable[str]: ...
def image_types() -> Iterable[str]: ...


class Spinbox(Widget, XView):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def bbox(self, index): ...
    def delete(self, first, last=None): ...
    def get(self): ...
    def icursor(self, index): ...
    def identify(self, x, y): ...
    def index(self, index): ...
    def insert(self, index, s): ...
    def invoke(self, element): ...
    def scan(self, *args): ...
    def scan_mark(self, x): ...
    def scan_dragto(self, x): ...
    def selection(self, *args) -> Iterable[int]: ...
    def selection_adjust(self, index) -> Iterable[int]: ...
    def selection_clear(self): ...
    def selection_element(self, element=None) -> Iterable[int]: ...

###########################################################################

class LabelFrame(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

########################################################################

class PanedWindow(Widget):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
    def add(self, child, **kw) -> None: ...
    def remove(self, child): ...
    forget = ...  # type: Any  ## remove

    def identify(self, x, y) -> str: ...
    def proxy(self, *args) -> Iterable[int]: ...
    def proxy_coord(self) -> Iterable[int]: ...
    def proxy_forget(self) -> Iterable[int]: ...
    def proxy_place(self, x, y) -> Iterable[int]: ...
    def sash(self, *args) -> Iterable[int]: ...
    def sash_coord(self, index) -> Iterable[int]: ...
    def sash_mark(self, index) -> Iterable[int]: ...
    def sash_place(self, index, x, y) -> Iterable[int]: ...
    def panecget(self, child, option) -> str: ...
    def paneconfigure(self, tagOrId, cnf=None, **kw) -> None: ...
    paneconfig = paneconfigure

    def panes(self) -> Iterable[Widget]: ...

######################################################################
# Extensions:

class Studbutton(Button):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...

class Tributton(Button):
    def __init__(self, master=None, cnf={}, **kw) -> None: ...
