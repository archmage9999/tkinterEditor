#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
geometry_pattern = re.compile("(\d+)x(\d+)\+(-?\d+)\+(-?\d+)")

from tkinter import PhotoImage
import tkinter.font as tkFont

# 默认值, 属性类型
PROP_CONFIGURE = {
    "activebackground": {
        "Button": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Label": ("None", "string",),
        "Radiobutton": ("None", "string",),
        "Scale": ("SystemScrollbar", "string",),
        "Scrollbar": ("SystemScrollbar", "string",),
        "Spinbox": ("SystemScrollbar", "string",),
    },
    "activeforeground": {
        "Button": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Label": ("None", "string",),
        "Radiobutton": ("None", "string",),
    },
    "activerelief": {
        "Scrollbar": ("raised", "string",),
    },
    "autoseparators": {
        "Text": (True, "bool",),
    },
    "aspect": {
        "Message": (150, "int",),
    },
    "background": {
        "Button": ("white", "string",),
        "Checkbutton": ("white", "string",),
        "Canvas": ("white", "string",),
        "Combobox": ("white", "string",),
        "Entry": ("white", "string",),
        "Frame": ("white", "string",),
        "Label": ("white", "string",),
        "LabelFrame": ("white", "string",),
        "Listbox": ("white", "string",),
        "Message": ("white", "string",),
        "PanedWindow": ("white", "string",),
        "Radiobutton": ("white", "string",),
        "Scale": ("white", "string",),
        "Scrollbar": ("#263238", "string",),
        "Spinbox": ("white", "string",),
        "Text": ("white", "string",),
        "Toplevel": ("white", "string",),
        "EditorProperty": ("white", "string",),
        "EditorPropertyList": ("white", "string",),
        "EditorTabControl": ("white", "string",),
        "EditorTabControlBtn": ("white", "string",),
        "EntryWithBtn": ("white", "string",),
        "EditorTree": ("white", "string",),
        "ScrollButtonCols": ("white", "string",),
        "ScrollCols": ("white", "string",),
        "ScrollCanvas": ("white", "string",),
        "ScrollRows": ("white", "string",),
    },
    "bigincrement": {
        "Scale": (0, "int",),
    },
    "borderwidth": {
        "Button": (0, "int",),
        "Canvas": (0, "int",),
        "Checkbutton": (2, "int",),
        "Entry": (1, "int",),
        "Frame": (0, "int",),
        "Label": (0, "int",),
        "LabelFrame": (2, "int",),
        "Listbox": (0, "int",),
        "Message": (0, "int",),
        "PanedWindow": (1, "int",),
        "Radiobutton": (2, "int",),
        "Scale": (1, "int",),
        "Scrollbar": (0, "int",),
        "Spinbox": (1, "int",),
        "Text": (0, "int",),
        "Toplevel": (0, "int",),
        "EditorProperty": (0, "int",),
        "EditorPropertyList": (0, "int",),
        "EditorTabControl": (0, "int",),
        "EditorTabControlBtn": (0, "int",),
        "EntryWithBtn": (1, "int",),
        "EditorTree": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
        "ScrollCanvas": (0, "int",),
        "ScrollRows": (0, "int",),
    },
    "buttonbackground": {
        "Spinbox": ("None", "string",),
    },
    "buttoncursor": {
        "Spinbox": ("arrow", "string",),
    },
    "buttondownrelief": {
        "Spinbox": ("raised", "string",),
    },
    "buttonuprelief": {
        "Spinbox": ("raised", "string",),
    },
    "cursor": {
        "Button": ("arrow", "string",),
        "Canvas": ("arrow", "string",),
        "Checkbutton": ("arrow", "string",),
        "Combobox": ("xterm", "string",),
        "Entry": ("xterm", "string",),
        "Frame": ("arrow", "string",),
        "Label": ("arrow", "string",),
        "LabelFrame": ("arrow", "string",),
        "Listbox": ("arrow", "string",),
        "Message": ("arrow", "string",),
        "PanedWindow": ("arrow", "string",),
        "Progressbar": ("arrow", "string",),
        "Radiobutton": ("arrow", "string",),
        "Scale": ("arrow", "string",),
        "Scrollbar": ("arrow", "string",),
        "Spinbox": ("arrow", "string",),
        "Text": ("xterm", "string",),
        "Toplevel": ("arrow", "string",),
        "Treeview": ("arrow", "string",),
        "EditorProperty": ("arrow", "string",),
        "EditorPropertyList": ("arrow", "string",),
        "EditorTabControl": ("arrow", "string",),
        "EditorTabControlBtn": ("arrow", "string",),
        "EntryWithBtn": ("xterm", "string",),
        "EditorTree": ("arrow", "string",),
        "ScrollButtonCols": ("arrow", "string",),
        "ScrollCols": ("arrow", "string",),
        "ScrollCanvas": ("arrow", "string",),
        "ScrollRows": ("arrow", "string",),
    },
    "compound": {
        "Label": ("center", "string",),
        "Button": ("center", "string",),
        "Checkbutton": ("center", "string",),
        "Radiobutton": ("center", "string",),
    },
    "command": {
        "Scrollbar": ("None", "string",),
    },
    "confine": {
        "Canvas": (True, "bool",),
        "ScrollCanvas": (True, "bool",),
    },
    "closeenough": {
        "Canvas": (1.0, "float",),
        "EditorProperty": (1.0, "float",),
        "EditorTree": (1.0, "float",),
        "ScrollButtonCols": (1.0, "float",),
        "ScrollCols": (1.0, "float",),
        "ScrollCanvas": (1.0, "float",),
        "ScrollRows": (1.0, "float",),
    },
    "digits": {
        "Scale": (0, "int",),
    },
    "disabledforeground": {
        "Button": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Label": ("None", "string",),
        "Radiobutton": ("None", "string",),
        "Spinbox": ("None", "string",),
    },
    "disabledbackground": {
        "Spinbox": ("None", "string",),
    },
    "exportselection": {
        "Combobox": (1, "int",),
        "Entry": (1, "int",),
        "EntryWithBtn": (1, "int",),
        "Listbox": (1, "int",),
        "Spinbox": (1, "int",),
        "Text": (1, "int",),
    },
    "elementborderwidth": {
        "Scrollbar": (-1, "int",),
    },
    "font": {
        "Button": ("None", "font",),
        "Checkbutton": ("None", "font",),
        "Entry": ("None", "font",),
        "EntryWithBtn": ("None", "font",),
        "Label": ("None", "font",),
        "LabelFrame": ("None", "font",),
        "Listbox": ("None", "font",),
        "Message": ("None", "font",),
        "Radiobutton": ("None", "font",),
        "Scale": ("None", "font",),
        "Spinbox": ("None", "font",),
        "Text": ("None", "font",),
    },
    "font_anchor": {
        "Button": ("center", "string",),
        "Checkbutton": ("center", "string",),
        "Label": ("center", "string",),
        "Radiobutton": ("center", "string",),
    },
    "foreground": {
        "Button": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Combobox": ("None", "string",),
        "Entry": ("None", "string",),
        "Label": ("None", "string",),
        "LabelFrame": ("None", "string",),
        "Listbox": ("None", "string",),
        "Message": ("None", "string",),
        "Radiobutton": ("None", "string",),
        "Scale": ("None", "string",),
        "Spinbox": ("None", "string",),
        "Text": ("None", "string",),
        "EntryWithBtn": ("None", "string",),
    },
    "from": {
    },
    "handlepad": {
        "PanedWindow": (8, "int",),
    },
    "handlesize": {
        "PanedWindow": (8, "int",),
    },
    "height": {
        "Button": (1, "int",),
        "Canvas": (300, "int",),
        "Checkbutton": (0, "int",),
        "Combobox": (1, "int",),
        "Frame": (400, "int",),
        "Label": (1, "int",),
        "LabelFrame": (400, "int",),
        "Listbox": (10, "int",),
        "PanedWindow": (400, "int",),
        "Radiobutton": (0, "int",),
        "Text": (2, "int",),
        "Treeview": (5, "int",),
        "EditorProperty": (300, "int",),
        "EditorPropertyList": (300, "int",),
        "EditorTabControl": (300, "int",),
        "EditorTabControlBtn": (20, "int",),
        "EditorTree": (300, "int",),
        "ScrollButtonCols": (300, "int",),
        "ScrollCols": (300, "int",),
        "ScrollCanvas": (300, "int",),
        "ScrollRows": (300, "int",),
    },
    "highlightbackground": {
        "Button": ("red", "string",),
        "Canvas": ("red", "string",),
        "Checkbutton": ("red", "string",),
        "Entry": ("red", "string",),
        "Frame": ("red", "string",),
        "Label": ("red", "string",),
        "LabelFrame": ("red", "string",),
        "Listbox": ("red", "string",),
        "Message": ("red", "string",),
        "Radiobutton": ("red", "string",),
        "Scale": ("red", "string",),
        "Scrollbar": ("red", "string",),
        "Spinbox": ("red", "string",),
        "Text": ("red", "string",),
        "Toplevel": ("red", "string",),
        "EditorProperty": ("red", "string",),
        "EditorPropertyList": ("red", "string",),
        "EditorTabControl": ("red", "string",),
        "EditorTabControlBtn": ("red", "string",),
        "EntryWithBtn": ("red", "string",),
        "EditorTree": ("red", "string",),
        "ScrollButtonCols": ("red", "string",),
        "ScrollCols": ("red", "string",),
        "ScrollCanvas": ("red", "string",),
        "ScrollRows": ("red", "string",),
    },
    "highlightcolor": {
        "Button": ("None", "string",),
        "Canvas": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Entry": ("None", "string",),
        "Frame": ("None", "string",),
        "Label": ("None", "string",),
        "LabelFrame": ("None", "string",),
        "Listbox": ("None", "string",),
        "Message": ("None", "string",),
        "Radiobutton": ("None", "string",),
        "Scale": ("None", "string",),
        "Scrollbar": ("None", "string",),
        "Spinbox": ("None", "string",),
        "Text": ("None", "string",),
        "Toplevel": ("None", "string",),
        "EditorProperty": ("None", "string",),
        "EditorPropertyList": ("None", "string",),
        "EditorTabControl": ("None", "string",),
        "EditorTabControlBtn": ("None", "string",),
        "EntryWithBtn": ("None", "string",),
        "EditorTree": ("None", "string",),
        "ScrollButtonCols": ("None", "string",),
        "ScrollCols": ("None", "string",),
        "ScrollCanvas": ("None", "string",),
        "ScrollRows": ("None", "string",),
    },
    "highlightthickness": {
        "Button": (0, "int",),
        "Canvas": (0, "int",),
        "Checkbutton": (0, "int",),
        "Entry": (0, "int",),
        "Frame": (0, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Listbox": (0, "int",),
        "Message": (0, "int",),
        "Radiobutton": (0, "int",),
        "Scale": (0, "int",),
        "Scrollbar": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "Toplevel": (0, "int",),
        "EditorProperty": (0, "int",),
        "EditorPropertyList": (0, "int",),
        "EditorTabControl": (0, "int",),
        "EditorTabControlBtn": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "EditorTree": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
        "ScrollCanvas": (0, "int",),
        "ScrollRows": (0, "int",),
    },
    "increment": {
        "Spinbox": (1, "float",),
    },
    "indicatoron": {
        "Checkbutton": (True, "bool",),
        "Radiobutton": (True, "bool",),
    },
    "insertbackground": {
        "Canvas": ("SystemWindowText", "string",),
        "Entry": ("SystemWindowText", "string",),
        "Spinbox": ("SystemWindowText", "string",),
        "Text": ("SystemWindowText", "string",),
        "EntryWithBtn": ("SystemWindowText", "string",),
        "ScrollCanvas": ("SystemWindowText", "string",),
    },
    "insertborderwidth": {
        "Canvas": (0, "int",),
        "Entry": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "ScrollCanvas": (0, "int",),
    },
    "insertofftime": {
        "Canvas": (300, "int",),
        "Entry": (300, "int",),
        "Spinbox": (300, "int",),
        "Text": (300, "int",),
        "EntryWithBtn": (300, "int",),
        "ScrollCanvas": (300, "int",),
    },
    "insertontime": {
        "Canvas": (600, "int",),
        "Entry": (600, "int",),
        "Spinbox": (600, "int",),
        "Text": (600, "int",),
        "EntryWithBtn": (600, "int",),
        "ScrollCanvas": (600, "int",),
    },
    "insertwidth": {
        "Canvas": (2, "int",),
        "Entry": (2, "int",),
        "Text": (2, "int",),
        "Spinbox": (2, "int",),
        "EntryWithBtn": (2, "int",),
        "ScrollCanvas": (2, "int",),
    },
    "image": {
        "Button": ("None", "string",),
        "Checkbutton": ("None", "string",),
        "Label": ("None", "string",),
        "Radiobutton": ("None", "string",),
    },
    "justify": {
        "Button": ("center", "string",),
        "Checkbutton": ("center", "string",),
        "Combobox": ("center", "string",),
        "Entry": ("center", "string",),
        "Label": ("center", "string",),
        "Message": ("center", "string",),
        "Radiobutton": ("center", "string",),
        "Spinbox": ("center", "string",),
        "EntryWithBtn": ("center", "string",),
    },
    "jump": {
        "Scrollbar": (False, "bool",),
    },
    "label": {
        "Scale": ("", "string",),
    },
    "labelanchor": {
        "LabelFrame": ("nw", "string",),
    },
    "length": {
        "Progressbar": (100, "int",),
        "Scale": (100, "int",),
    },
    "maxundo": {
        "Text": (0, "int",),
    },
    "maximum": {
        "Progressbar": (100, "int"),
    },
    "mode": {
        "Progressbar": ("determinate", "string"),
    },
    "offvalue": {
        "Checkbutton": (0, "int",),
    },
    "onvalue": {
        "Checkbutton": (1, "int",),
    },
    "opaqueresize": {
        "PanedWindow": (True, "bool",),
    },
    "orient": {
        "PanedWindow": ("vertical", "string",),
        "Progressbar": ("horizontal", "string",),
        "Scale": ("vertical", "string",),
        "Scrollbar": ("vertical", "string",),
        "Separator": ("vertical", "string",),
    },
    "padx": {
        "Button": (0, "int",),
        "Checkbutton": (1, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Message": (0, "int",),
        "Radiobutton": (0, "int",),
        "Text": (0, "int",),
    },
    "pady": {
        "Button": (0, "int",),
        "Checkbutton": (1, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Message": (0, "int",),
        "Radiobutton": (0, "int",),
        "Text": (0, "int",),
    },
    "readonlybackground": {
        "Spinbox": ("None", "string",),
    },
    "relief": {
        "Button": ("raised", "string",),
        "Canvas": ("flat", "string",),
        "Checkbutton": ("flat", "string",),
        "Entry": ("sunken", "string",),
        "Frame": ("flat", "string",),
        "Label": ("flat", "string",),
        "LabelFrame": ("groove", "string",),
        "Listbox": ("None", "string",),
        "Message": ("flat", "string",),
        "PanedWindow": ("flat", "string",),
        "Radiobutton": ("flat", "string",),
        "Scale": ("sunken", "string",),
        "Scrollbar": ("sunken", "string",),
        "Spinbox": ("sunken", "string",),
        "Text": ("sunken", "string",),
        "Toplevel": ("flat", "string",),
        "EditorProperty": ("flat", "string",),
        "EditorPropertyList": ("flat", "string",),
        "EditorTabControl": ("flat", "string",),
        "EditorTabControlBtn": ("flat", "string",),
        "EntryWithBtn": ("sunken", "string",),
        "EditorTree": ("flat", "string",),
        "ScrollButtonCols": ("flat", "string",),
        "ScrollCols": ("flat", "string",),
        "ScrollCanvas": ("flat", "string",),
        "ScrollRows": ("flat", "string",),
    },
    "repeatdelay": {
        "Button": (0, "int",),
        "Scale": (300, "int",),
        "Scrollbar": (300, "int",),
        "Spinbox": (300, "int",),
    },
    "repeatinterval": {
        "Button": (0, "int",),
        "Scale": (100, "int",),
        "Scrollbar": (100, "int",),
        "Spinbox": (100, "int",),
    },
    "resolution": {
        "Scale": (1, "float",),
    },
    "sashcursor": {
        "PanedWindow": ("arrow", "string",),
    },
    "sashpad": {
        "PanedWindow": (0, "int",),
    },
    "sashrelief": {
        "PanedWindow": ("flat", "string",),
    },
    "sashwidth": {
        "PanedWindow": (3, "int",),
    },
    "showhandle": {
        "PanedWindow": (False, "bool",),
    },
    "showvalue": {
        "Scale": (True, "bool",),
    },
    "sliderlength": {
        "Scale": (30, "int",),
    },
    "sliderrelief": {
        "Scale": ("raised", "string",),
    },
    "state": {
        "Button": ("normal", "string",),
        "Canvas": ("normal", "string",),
        "Checkbutton": ("normal", "string",),
        "Combobox": ("normal", "string",),
        "Entry": ("normal", "string",),
        "Label": ("normal", "string",),
        "Radiobutton": ("normal", "string",),
        "Scale": ("normal", "string",),
        "Spinbox": ("normal", "string",),
        "EntryWithBtn": ("normal", "string",),
        "ScrollCanvas": ("normal", "string",),
    },
    "selectbackground": {
        "Canvas": ("SystemHighlight", "string",),
        "Entry": ("SystemHighlight", "string",),
        "Listbox": ("SystemHighlight", "string",),
        "Spinbox": ("SystemHighlight", "string",),
        "Text": ("SystemHighlight", "string",),
        "EntryWithBtn": ("SystemHighlight", "string",),
        "ScrollCanvas": ("SystemHighlight", "string",),
    },
    "selectborderwidth": {
        "Canvas": (0, "int",),
        "Entry": (0, "int",),
        "Listbox": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "ScrollCanvas": (0, "int",),
    },
    "selectcolor": {
        "Checkbutton": ("SystemWindow", "string",),
        "Radiobutton": ("SystemWindow", "string",),
    },
    "selectforeground": {
        "Canvas": ("SystemHighlightText", "string",),
        "Entry": ("SystemHighlightText", "string",),
        "Listbox": ("SystemHighlightText", "string",),
        "Spinbox": ("SystemHighlightText", "string",),
        "Text": ("SystemHighlightText", "string",),
        "EntryWithBtn": ("SystemHighlightText", "string",),
        "ScrollCanvas": ("SystemHighlightText", "string",),
    },
    "selectmode": {
        "Listbox": ("single", "string",),
        "Treeview": ("extended", "string",),
    },
    "show": {
        "Treeview": ("tree headings", "string",),
    },
    "spacing1": {
        "Text": (0, "int",),
    },
    "spacing2": {
        "Text": (0, "int",),
    },
    "spacing3": {
        "Text": (0, "int",),
    },
    "text": {
        "Button": ("button", "string",),
        "Checkbutton": ("checkbox", "string",),
        "Label": ("label", "string",),
        "LabelFrame": ("None", "string"),
        "Message": ("message", "string",),
        "Radiobutton": ("radiobutton", "string",),
    },
    "takefocus": {
        "Button": (0, "int",),
        "Canvas": (0, "int",),
        "Checkbutton": (0, "int",),
        "Combobox": (0, "int",),
        "Entry": (0, "int",),
        "Frame": (0, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Listbox": (0, "int",),
        "Message": (0, "int",),
        "Progressbar": (0, "int",),
        "Radiobutton": (0, "int",),
        "Scale": (0, "int",),
        "Scrollbar": (0, "int",),
        "Separator": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "Toplevel": (0, "int",),
        "Treeview": (0, "int",),
        "EditorProperty": (0, "int",),
        "EditorPropertyList": (0, "int",),
        "EditorTabControl": (0, "int",),
        "EditorTabControlBtn": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "EditorTree": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
        "ScrollCanvas": (0, "int",),
        "ScrollRows": (0, "int",),
    },
    "tickinterval": {
        "Scale": (0, "int",),
    },
    "to": {
    },
    "troughcolor": {
        "Scale": ("SystemScrollbar", "string",),
        "Scrollbar": ("SystemScrollbar", "string",),
    },
    "underline": {
        "Button": (-1, "int",),
        "Checkbutton": (-1, "int",),
        "Label": (-1, "int",),
        "Radiobutton": (-1, "int",),
    },
    "undo": {
        "Text": (False, "bool",),
    },
    "value": {
        "Progressbar": (0, "int"),
        "Radiobutton": ("None", "string",),
    },
    "values": {
        "Combobox": ("None", "string",),
    },
    "width": {
        "Button": (15, "int",),
        "Checkbutton": (0, "int",),
        "Canvas": (300, "int",),
        "Combobox": (30, "int",),
        "Entry": (30, "int",),
        "Frame": (400, "int",),
        "Label": (30, "int",),
        "LabelFrame": (400, "int",),
        "Listbox": (30, "int",),
        "Message": (0, "int",),
        "PanedWindow": (400, "int",),
        "Radiobutton": (0, "int",),
        "Scale": (15, "int",),
        "Spinbox": (20, "int",),
        "Text": (30, "int",),
        "EditorProperty": (300, "int",),
        "EditorPropertyList": (300, "int",),
        "EditorTabControl": (300, "int",),
        "EditorTabControlBtn": (300, "int",),
        "EntryWithBtn": (30, "int",),
        "EditorTree": (300, "int",),
        "ScrollButtonCols": (300, "int",),
        "ScrollCols": (300, "int",),
        "ScrollCanvas": (300, "int",),
        "ScrollRows": (300, "int",),
    },
    "wrap": {
        "Text": ("char", "string",),
    },
    "wrapspinbox": {
        "Spinbox": (False, "bool",),
    },
    "wraplength": {
        "Button": (0, "int",),
        "Checkbutton": (0, "int",),
        "Label": (0, "int",),
        "Radiobutton": (0, "int",),
    },
}


PROP_PLACE_CONFIGURE = {
    "x": {
        "Button": (0, "int",),
        "Canvas": (0, "int",),
        "Checkbutton": (0, "int",),
        "Combobox": (0, "int",),
        "Entry": (0, "int",),
        "Frame": (0, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Listbox": (0, "int",),
        "Message": (0, "int",),
        "PanedWindow": (0, "int",),
        "Progressbar": (0, "int",),
        "Radiobutton": (0, "int",),
        "Scale": (0, "int",),
        "Scrollbar": (0, "int",),
        "Separator": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "Treeview": (0, "int",),
        "EditorProperty": (0, "int",),
        "EditorPropertyList": (0, "int",),
        "EditorTabControl": (0, "int",),
        "EditorTabControlBtn": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "EditorTree": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
        "ScrollCanvas": (0, "int",),
        "ScrollRows": (0, "int",),
    },
    "y": {
        "Button": (0, "int",),
        "Canvas": (0, "int",),
        "Checkbutton": (0, "int",),
        "Combobox": (0, "int",),
        "Entry": (0, "int",),
        "Frame": (0, "int",),
        "Label": (0, "int",),
        "LabelFrame": (0, "int",),
        "Listbox": (0, "int",),
        "Message": (0, "int",),
        "PanedWindow": (0, "int",),
        "Progressbar": (0, "int",),
        "Radiobutton": (0, "int",),
        "Scale": (0, "int",),
        "Scrollbar": (0, "int",),
        "Separator": (0, "int",),
        "Spinbox": (0, "int",),
        "Text": (0, "int",),
        "Treeview": (0, "int",),
        "EditorProperty": (0, "int",),
        "EditorPropertyList": (0, "int",),
        "EditorTabControl": (0, "int",),
        "EditorTabControlBtn": (0, "int",),
        "EntryWithBtn": (0, "int",),
        "EditorTree": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
        "ScrollCanvas": (0, "int",),
        "ScrollRows": (0, "int",),
    },
    "anchor": {
        "Button": ("nw", "string",),
        "Canvas": ("nw", "string",),
        "Checkbutton": ("nw", "string",),
        "Combobox": ("nw", "string",),
        "Entry": ("nw", "string",),
        "Frame": ("nw", "string",),
        "Label": ("nw", "string",),
        "LabelFrame": ("nw", "string",),
        "Listbox": ("nw", "string",),
        "Message": ("nw", "string",),
        "PanedWindow": ("nw", "string",),
        "Progressbar": ("nw", "string",),
        "Radiobutton": ("nw", "string",),
        "Scale": ("nw", "string",),
        "Scrollbar": ("nw", "string",),
        "Separator": ("nw", "string",),
        "Spinbox": ("nw", "string",),
        "Text": ("nw", "string",),
        "Treeview": ("nw", "string",),
        "EditorProperty": ("nw", "string",),
        "EditorPropertyList": ("nw", "string",),
        "EditorTabControl": ("nw", "string",),
        "EditorTabControlBtn": ("nw", "string",),
        "EntryWithBtn": ("nw", "string",),
        "EditorTree": ("nw", "string",),
        "ScrollButtonCols": ("nw", "string",),
        "ScrollCols": ("nw", "string",),
        "ScrollCanvas": ("nw", "string",),
        "ScrollRows": ("nw", "string",),
    },
    "width": {
        "Progressbar": (100, "int",),
        "Scrollbar": (16, "int",),
        "Separator": (1, "int",),
    },
    "height": {
        "Progressbar": (30, "int",),
        "Scrollbar": (200, "int",),
        "Separator": (20, "int",),
    },
}


PROP_EXT = {
    "btn_frame_distance": {
        "EditorTabControl": (2, "int",),
    },
    "col_distance": {
        "EditorProperty": (2, "int",),
        "EditorTabControl": (2, "int",),
        "ScrollButtonCols": (1, "int",),
    },
    "function_id": {
        "EntryWithBtn": (1, "int",),
    },
    "is_always_show_scroll": {
        "EditorProperty": (1, "int",),
        "EditorPropertyList": (1, "int",),
        "EditorTree": (1, "int",),
        "ScrollButtonCols": (1, "int",),
        "ScrollCols": (1, "int",),
        "ScrollCanvas": (1, "int",),
        "ScrollRows": (1, "int",),
    },
    "is_show_scroll_x": {
        "EditorProperty": (1, "int",),
        "EditorPropertyList": (1, "int",),
        "EditorTree": (1, "int",),
        "ScrollButtonCols": (1, "int",),
        "ScrollCols": (1, "int",),
        "ScrollCanvas": (1, "int",),
        "ScrollRows": (1, "int",),
    },
    "is_show_scroll_y": {
        "EditorTree": (1, "int",),
        "EditorProperty": (1, "int",),
        "EditorPropertyList": (1, "int",),
        "ScrollButtonCols": (1, "int",),
        "ScrollCols": (1, "int",),
        "ScrollCanvas": (1, "int",),
        "ScrollRows": (1, "int",),
    },
    "label_text": {
        "EditorTabControlBtn": ("default", "string",),
    },
    "pos_x_default": {
        "EditorProperty": (0, "int",),
        "ScrollButtonCols": (0, "int",),
        "ScrollCols": (0, "int",),
    },
    "pos_y_default": {
        "EditorPropertyList": (0, "int",),
        "ScrollRows": (0, "int",),
    },
}


PROP_LIKE_TOP_LEVEL = {
    "x": {
        "Toplevel": (0, "int",),
    },
    "y": {
        "Toplevel": (0, "int",),
    },
    "width": {
        "Toplevel": (400, "int",),
    },
    "height": {
        "Toplevel": (400, "int",),
    },
    "title": {
        "Toplevel": ("toplevel", "string",),
    },
    "topmost": {
        "Toplevel": (1, "int",),
    },
}


PROP_NAME_CHANGE = {
    "font_anchor": "anchor",
    "wrapspinbox": "wrap",
}


def change_prop(prop_type, prop):
    """
    根据属性名字转换属性
    :param prop_type: 属性类型
    :param prop: 属性值
    :return: 转换后的属性值
    """
    if prop_type == "int":
        return int(prop)

    if prop_type == "float":
        return float(prop)

    if prop_type == "bool":
        return bool(prop)

    if prop_type == "font":
        return tkFont.Font(family=prop)

    return prop


def update_place_property(component, component_info, gui_type):
    """
    更新位置相关属性
    :param component: 控件
    :param component_info: 控件信息
    :param gui_type: 控件类型
    :return: None
    """
    for prop_name, prop in component_info.items():
        if prop == "None":
            continue
        if prop_name not in PROP_PLACE_CONFIGURE:
            continue
        if gui_type not in PROP_PLACE_CONFIGURE[prop_name]:
            continue
        prop = change_prop(PROP_PLACE_CONFIGURE[prop_name][gui_type][1], prop)
        component.place_configure({prop_name: prop})

    return


def update_normal_property(component, component_info, gui_type):
    """
    更新普通属性
    :param component: 控件
    :param component_info: 控件信息
    :param gui_type: 控件类型
    :return: None
    """
    for prop_name, prop in component_info.items():
        if prop == "None":
            continue
        if prop_name not in PROP_CONFIGURE:
            continue
        if gui_type not in PROP_CONFIGURE[prop_name]:
            continue
        prop = change_prop(PROP_CONFIGURE[prop_name][gui_type][1], prop)
        if prop_name in PROP_NAME_CHANGE:
            prop_name = PROP_NAME_CHANGE[prop_name]
        # image属性在下面处理
        if prop_name == "image":
            continue
        component.configure({prop_name:prop})

    # 给image赋值后修改一下宽和高
    if gui_type in PROP_CONFIGURE["image"]:
        image = component_info.get("image", "None")
        if image != "None":
            component.photo = PhotoImage(file=image)
            component.configure(image=component.photo)
            component.configure(width=0, height=0)
            component_info["width"] = 0
            component_info["height"] = 0
        return

    return


def update_ext_property(component, component_info, gui_type):
    """
    更新自定义属性
    :param component: 控件
    :param component_info: 控件信息
    :param gui_type: 控件类型
    :return: None
    """
    for prop_name, prop in component_info.items():
        if prop == "None":
            continue
        if prop_name not in PROP_EXT:
            continue
        if gui_type not in PROP_EXT[prop_name]:
            continue
        prop = change_prop(PROP_EXT[prop_name][gui_type][1], prop)
        func = getattr(component, "set_" + prop_name, None)
        if not func:
            continue
        func(prop)

    return


def update_like_toplevel_property(component, component_info, gui_type):
    """
    更新类toplevel属性
    :param component: 控件
    :param component_info: 控件信息
    :param gui_type: 控件类型
    :return: None
    """
    for prop_name, prop in component_info.items():
        if prop == "None":
            continue
        if prop_name not in PROP_LIKE_TOP_LEVEL:
            continue
        if gui_type not in PROP_LIKE_TOP_LEVEL[prop_name]:
            continue
        prop = change_prop(PROP_LIKE_TOP_LEVEL[prop_name][gui_type][1], prop)
        if prop_name in ("x", "y", "width", "height"):
            component.geometry("%sx%s+%s+%s" % (component_info["width"], component_info["height"], component_info["x"], component_info["y"],))
            continue
        if prop_name == "title":
            component.title(prop)
            continue
        if prop_name in ("topmost"):
            component.wm_attributes('-{0}'.format(prop_name), prop)


def update_all_property(component, component_info, gui_type):
    """
    更新所有属性
    :param component: 控件
    :param component_info: 控件信息
    :param gui_type: 控件类型
    :return: None
    """
    update_place_property(component, component_info, gui_type)
    update_normal_property(component, component_info, gui_type)
    update_like_toplevel_property(component, component_info, gui_type)
    if hasattr(component, "on_update"):
        component.on_update()
    update_ext_property(component, component_info, gui_type)


def get_default_component_info(component_type, prop=None):
    """
    根据控件类型获取控件默认属性
    :param component_type: 控件类型
    :param prop: 需要更新的属性
    :return: dict
    """
    property_dict = {}

    for prop_name, value in PROP_CONFIGURE.items():
        if component_type not in value:
            continue
        property_dict[prop_name] = value[component_type][0]

    for prop_name, value in PROP_PLACE_CONFIGURE.items():
        if component_type not in value:
            continue
        property_dict[prop_name] = value[component_type][0]

    for prop_name, value in PROP_EXT.items():
        if component_type not in value:
            continue
        property_dict[prop_name] = value[component_type][0]

    for prop_name, value in PROP_LIKE_TOP_LEVEL.items():
        if component_type not in value:
            continue
        property_dict[prop_name] = value[component_type][0]

    if prop is not None:
        property_dict.update(prop)

    return property_dict


def get_all_prop_name():
    """
    获取所有属性名字
    :return: set
    """
    all_name = set(PROP_CONFIGURE.keys())
    all_name.update(PROP_PLACE_CONFIGURE.keys())
    all_name.update(PROP_EXT.keys())
    all_name.update(PROP_LIKE_TOP_LEVEL.keys())
    all_name.add("component_name")

    return all_name


def update_single_prop(component, prop_name, prop_value, gui_type):

    if prop_name == "image":
        if gui_type in PROP_CONFIGURE["image"] and prop_value != "None":
            component.photo = PhotoImage(file=prop_value)
            component.configure(image=component.photo)
            component.configure(width=0, height=0)
        return

    if prop_name in PROP_PLACE_CONFIGURE and gui_type in PROP_PLACE_CONFIGURE[prop_name]:
        prop = change_prop(PROP_PLACE_CONFIGURE[prop_name][gui_type][1], prop_value)
        if prop != "None":
            component.place_configure({prop_name: prop})
        return

    if prop_name in PROP_CONFIGURE and gui_type in PROP_CONFIGURE[prop_name]:
        prop = change_prop(PROP_CONFIGURE[prop_name][gui_type][1], prop_value)
        if prop != "None":
            if prop_name in PROP_NAME_CHANGE:
                prop_name = PROP_NAME_CHANGE[prop_name]
            component.configure({prop_name: prop})
        return

    if prop_name in PROP_EXT and gui_type in PROP_EXT[prop_name]:
        prop = change_prop(PROP_EXT[prop_name][gui_type][1], prop_value)
        if prop != "None":
            func = getattr(component, "set_" + prop_name, None)
            if func:
                func(prop)
        return

    if prop_name in PROP_LIKE_TOP_LEVEL and gui_type in PROP_LIKE_TOP_LEVEL[prop_name]:
        prop = change_prop(PROP_LIKE_TOP_LEVEL[prop_name][gui_type][1], prop_value)
        if prop != "None":
            if prop_name == "x":
                geometry = component.winfo_geometry()
                matched = geometry_pattern.match(geometry)
                component.geometry("%sx%s+%d+%s" % (matched.groups()[0], matched.groups()[1], prop, matched.groups()[3],))
            elif prop_name == "y":
                geometry = component.winfo_geometry()
                matched = geometry_pattern.match(geometry)
                component.geometry("%sx%s+%s+%d" % (matched.groups()[0], matched.groups()[1], matched.groups()[2], prop,))
            elif prop_name == "width":
                geometry = component.winfo_geometry()
                matched = geometry_pattern.match(geometry)
                component.geometry("%dx%s+%s+%s" % (prop, matched.groups()[1], matched.groups()[2], matched.groups()[3],))
            elif prop_name == "height":
                geometry = component.winfo_geometry()
                matched = geometry_pattern.match(geometry)
                component.geometry("%sx%d+%s+%s" % (matched.groups()[0], prop, matched.groups()[2], matched.groups()[3],))
            elif prop_name == "title":
                component.title(prop)
            elif prop_name in ("topmost"):
                component.wm_attributes('-{0}'.format(prop_name), prop)
        return