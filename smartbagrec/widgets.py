""" The wrapper for the tkinter widgets.

This module contains the wrapper classes for the tkinter widgets.
This wrapper helps to write the object-oriented code.
"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable, Optional, Tuple, Union

Pos = Tuple[int, ...]
TkWidgets = Union[tk.Tk, tk.Toplevel, tk.Widget]


class Widget:
    """ Base class for all wrappers of tkinter widgets

    This class is not meant to be instantiated directly.

    Attributes:
        _parent (Widget): The parent widget of this widget
        _tk_widget (Union[tk.Tk, tk.Widget]): The tkinter widget this class wraps
    """

    _parent: Optional[Widget]
    _tk_widget: TkWidgets

    def __init__(self, parent: Optional[Widget]) -> None:
        self._parent = parent

    @property
    def parent(self) -> Widget:
        if self._parent is None:
            raise ValueError("Widget has no parent")
        return self._parent

    @property
    def tk_widget(self) -> TkWidgets:
        return self._tk_widget


class MainWindow(Widget):
    """ This class wraps the tkinter.Tk class.
    """

    def __init__(self, title: str) -> None:
        super().__init__(None)
        self._tk_widget = tk.Tk()
        self._tk_widget.title(title)
        self._tk_widget.columnconfigure(0, weight=1)
        self._tk_widget.rowconfigure(0, weight=1)

    def __call__(self) -> None:
        self._tk_widget.mainloop()


class ModalWindow(Widget):
    """ This class wraps the tkinter.Toplevel class.
    """

    def __init__(self, parent: Widget, master: tk.Tk, title: str) -> None:
        super().__init__(parent)
        self._tk_widget = tk.Toplevel()
        self._tk_widget.title(title)
        self._tk_widget.columnconfigure(0, weight=1)
        self._tk_widget.rowconfigure(0, weight=1)
        self._tk_widget.grab_set()
        self._tk_widget.focus_set()
        self._tk_widget.transient(master)  # type: ignore


class Frame(Widget):
    """ This class wraps the tkinter.ttk.Frame class.
    """

    def __init__(self, parent: Widget, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._tk_widget = ttk.Frame(parent.tk_widget)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore
        self._tk_widget.columnconfigure(0, weight=1)
        self._tk_widget.rowconfigure(0, weight=1)


class Labelframe(Widget):
    """ This class wraps the tkinter.ttk.Labelframe class.
    """

    def __init__(self, parent: Widget, text: str, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._tk_widget = ttk.Labelframe(parent.tk_widget, text=text)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore
        self._tk_widget.columnconfigure(0, weight=1)
        self._tk_widget.rowconfigure(0, weight=1)


class Label(Widget):
    """ This class wraps the tkinter.ttk.Label class.
    """

    def __init__(self, parent: Widget, text: str, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._tk_widget = ttk.Label(parent.tk_widget, text=text)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore


class Button(Widget):
    """ This class wraps the tkinter.ttk.Button class.
    """

    def __init__(self, parent: Widget, text: str, command: Callable, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._tk_widget = ttk.Button(parent.tk_widget, text=text, command=command)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore


class Checkbutton(Widget):
    """ This class wraps the tkinter.ttk.Checkbutton class.
    """

    _button_state: tk.BooleanVar

    def __init__(self, parent: Widget, text: str, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._button_state = tk.BooleanVar()
        self._tk_widget = ttk.Checkbutton(
            parent.tk_widget, text=text, variable=self._button_state, onvalue=True, offvalue=False)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore

    def get_state(self) -> bool:
        return self._button_state.get()


class Radiobutton(Widget):
    """ This class wraps the tkinter.ttk.Radiobutton class.
    """

    def __init__(self, parent: Widget, text: str, variable: tk.IntVar, value: Any, command: Callable, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._tk_widget = ttk.Radiobutton(
            parent.tk_widget, text=text, variable=variable, value=value, command=command)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore


class Entry(Widget):
    """ This class wraps the tkinter.ttk.Entry class.
    """

    _entry_state: tk.StringVar

    def __init__(self, parent: Widget, pos: Pos = (0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)
        self._entry_state = tk.StringVar()
        self._tk_widget = ttk.Entry(parent.tk_widget, textvariable=self._entry_state)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore

    def get_state(self) -> str:
        return self._entry_state.get()


class ScrollableListbox(Widget):
    """ This class wraps the tk.Listbox class and tk.Scrollbar class.
    """

    _tk_scrollbar: ttk.Scrollbar

    def __init__(self, parent: Widget, contents: Tuple[str], mode: str, pos: Pos = (0, 0, 0, 0), grid_opt: dict = {}) -> None:
        super().__init__(parent)

        string_var = tk.StringVar(value=contents)  # type: ignore
        self._tk_widget: tk.Listbox = tk.Listbox(parent.tk_widget, listvariable=string_var, selectmode=mode)
        self._tk_widget.grid(row=pos[0], column=pos[1], **grid_opt)  # type: ignore

        self._tk_scrollbar = ttk.Scrollbar(parent.tk_widget, orient=tk.VERTICAL, command=self._tk_widget.yview)
        self._tk_widget["yscrollcommand"] = self._tk_scrollbar.set
        self._tk_scrollbar.grid(row=pos[2], column=pos[3], **grid_opt)  # type: ignore

    @property
    def tk_scrollbar(self) -> ttk.Scrollbar:
        return self._tk_scrollbar

    def get_selected(self) -> Tuple[str]:
        return tuple([self._tk_widget.get(i) for i in self._tk_widget.curselection()])
