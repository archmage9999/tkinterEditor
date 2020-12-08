#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from enum import IntEnum
import tkinter.font as tkFont
from tkinter import Entry, END, Label, Button
from tkinter.ttk import Combobox
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename

from ScrollRows import ScrollRows
from ScrollCols import ScrollCols
from WidgetRedirector import WidgetRedirector
from componentProperty import update_all_property, get_default_component_info, get_all_prop_name, get_pixel_width, get_pixel_height


def create_default_component(master, component_type, component_name, prop=None, use_name=True):
    """
    创建默认控件
    :param master: 父控件
    :param component_type: 控件类型
    :param component_name: 控件名字
    :param prop: 需要更新的属性
    :param use_name: 是否使用控件名字
    :return: 控件
    """
    class_name = getattr(sys.modules[__name__], component_type)
    if use_name:
        component = class_name(master, name=component_name)
    else:
        component = class_name(master)

    component_info = get_default_component_info(component_type, prop)
    update_all_property(component, component_info, component_type)

    return component, component_info


CURSOR_LIST = (
    "arrow;based_arrow_down;based_arrow_up;boat;bogosity;bottom_left_corner;bottom_right_corner;"
    "bottom_side;bottom_tee;box_spiral;center_ptr;circle;clock;coffee_mug;cross;cross_reverse;crosshair;"
    "diamond_cross;dot;dotbox;double_arrow;draft_large;draft_small;draped_box;exchange;fleur;gobbler;gumby;"
    "hand1;hand2;heart;icon;iron_cross;left_ptr;left_side;left_tee;leftbutton;ll_angle;lr_angle;man;"
    "middlebutton;mouse;none;pencil;pirate;plus;question_arrow;right_ptr;right_side;right_tee;rightbutton;"
    "rtl_logo;sailboat;sb_down_arrow;sb_h_double_arrow;sb_left_arrow;sb_right_arrow;sb_up_arrow;"
    "sb_v_double_arrow;shuttle;sizing;spider;spraycan;star;target;tcross;top_left_arrow;top_left_corner;"
    "top_right_corner;top_side;top_tee;trek;ul_angle;umbrella;ur_angle;watch;xterm;X_cursor"
)


PROP_TO_VALUES = {
    "anchor": ("n;s;w;e;nw;sw;ne;se;center"),
    "justify": ("left;right;center"),
    "font_anchor": ("n;s;w;e;nw;sw;ne;se;center"),
    "labelanchor": ("n;s;w;e;nw;sw;ne;se"),
    "relief": ("flat;groove;raised;ridge;solid;sunken"),
    "activerelief": ("flat;groove;raised;ridge;solid;sunken"),
    "sliderrelief": ("flat;groove;raised;ridge;solid;sunken"),
    "buttondownrelief": ("flat;groove;raised;ridge;solid;sunken"),
    "buttonuprelief": ("flat;groove;raised;ridge;solid;sunken"),
    "mode": ("determinate;indeterminate"),
    "state": ("active;disabled;normal;readonly"),
    "cursor": CURSOR_LIST,
    "buttoncursor": CURSOR_LIST,
    "compound": ("bottom;center;left;none;right;top"),
    "exportselection": ("0;1"),
    "selectmode": ("browse;multiple;single;extended;none"),
    "is_show_scroll": ("0;1"),
    "is_show_scroll_x": ("0;1"),
    "is_show_scroll_y": ("0;1"),
    "is_always_show_scroll": ("0;1"),
    "orient": ("horizontal;vertical"),
    "wrap": ("none;char;word"),
    "show": ("headings;tree;tree headings"),
}


PROP_COLOR_LIST = (
    "background", "activebackground", "activeforeground", "disabledforeground", "readonlybackground",
    "foreground", "highlightbackground", "highlightcolor", "insertbackground", "disabledbackground",
    "selectbackground", "selectforeground", "troughcolor", "selectcolor", "buttonbackground"
)


PROP_SELECT_LIST = (
    "bitmap", "image"
)


class EditPropType(IntEnum):

    TYPE_ENTRY = 1
    TYPE_COMBO_BOX = 2
    TYPE_COLOR = 3
    TYPE_SELECT = 4


class EntryBtnFunctionID(IntEnum):

    FUNCTION_COLOR = 1
    FUNCTION_SELECT = 2


def get_prop_type_by_name(name):
    """
    根据属性名字获取编辑框类型
    :param name: 属性名字
    :return: 编辑框类型
    """
    if name in PROP_TO_VALUES:
        return EditPropType.TYPE_COMBO_BOX

    if name in PROP_COLOR_LIST:
        return EditPropType.TYPE_COLOR

    if name in PROP_SELECT_LIST:
        return EditPropType.TYPE_SELECT

    return EditPropType.TYPE_ENTRY


class EntryWithBtn(Entry):

    def __init__(self, master=None, cnf={}, **kw):
        Entry.__init__(self, master, cnf, **kw)
        self.function_id = EntryBtnFunctionID.FUNCTION_COLOR
        self.function_dict = {
            EntryBtnFunctionID.FUNCTION_COLOR: self.btn_color_click,
            EntryBtnFunctionID.FUNCTION_SELECT: self.btn_select_click,
        }

    def set_function_id(self, function_id):
        if self.function_id == function_id:
            return
        self.function_id = function_id

    def get_function_id(self):
        return self.function_id

    def on_update(self):
        self.create_btn()

    def create_btn(self):

        prop = {
            "width": 0, "height": 1,
            "x": get_pixel_width(self) - 15,
            "text": "...", "background": "grey",
        }
        btn, info = create_default_component(self, "Button", "function_btn", prop, True)
        btn.bind("<Button-1>", self.on_btn_click)

    def on_btn_click(self, event):
        function = self.function_dict[self.get_function_id()]
        function()

    def btn_color_click(self):
        color = colorchooser.askcolor()
        if color[0] is None:
            return
        self.delete(0, END)
        self.insert(0, color[1])

    def btn_select_click(self):
        file_path = askopenfilename(title=u"选择文件", filetypes=[("all files", "*")])
        if not file_path:
            return
        self.delete(0, END)
        self.insert(0, file_path)


class EditorProperty(ScrollCols):

    TYPE_TO_CLASS = {
        EditPropType.TYPE_ENTRY: Entry,
        EditPropType.TYPE_COMBO_BOX: Combobox,
        EditPropType.TYPE_COLOR: EntryWithBtn,
        EditPropType.TYPE_SELECT: EntryWithBtn,
    }

    def __init__(self, master=None, cnf={}, **kw):
        ScrollCols.__init__(self, master, cnf, **kw)
        self.col_distance = 2
        self.is_updating_property = False                       # 是否正在更新属性

    def create_label(self, label_text, is_do_layout=False):
        """
        创建属性名字标签
        :param label_text: 标签内容
        :param is_do_layout: 是否重新布局
        :return: None
        """
        label_prop = {
            "width": 23, "borderwidth": 2,
            "x": 0, "y": 1,
            "text": label_text,
            "relief": "sunken",
            "highlightthickness": 1,
        }
        label, info = create_default_component(self.slide_window, "Label", "label_text", label_prop)
        self.add_col_base(label, is_do_layout)

    def create_edit(self, edit_type, edit_value, default_values="None", is_do_layout=False):
        """
        创建属性编辑框
        :param edit_type: 编辑框类型
        :param edit_value: 默认值
        :param default_values: comboBox下拉列表默认值
        :param is_do_layout: 是否重新布局
        :return: None
        """
        edit_class = self.TYPE_TO_CLASS[edit_type]
        edit_prop = {
            "borderwidth": 2, "width": 29,
            "x": 0, "y": 1,
        }

        if edit_type == EditPropType.TYPE_COMBO_BOX:
            values = default_values.split(";")
            value_list = []
            for value in values:
                value_list.append(value)
            edit_prop.update({"values": value_list, "width": 27, "position_y": 1, "borderwidth": 1, "height": 5,})
        elif edit_type == EditPropType.TYPE_SELECT:
            edit_prop.update({"function_id": EntryBtnFunctionID.FUNCTION_SELECT})
        elif edit_type == EditPropType.TYPE_COLOR:
            edit_prop.update({"function_id": EntryBtnFunctionID.FUNCTION_COLOR})

        edit, info = create_default_component(self.slide_window, edit_class.__name__, "edit", edit_prop)
        edit.bind("<Key>", self.key_click)
        if edit_type == EditPropType.TYPE_COMBO_BOX:
            edit.bind("<<ComboboxSelected>>", self.on_prop_change)

        self.add_col_base(edit, is_do_layout)

        if edit_value is not None:
            edit.insert(0, edit_value)

        redir = WidgetRedirector(edit)

        def my_insert(*args):
            original_insert(*args)
            self.on_prop_change(None)

        def my_delete(*args):
            original_delete(*args)
            self.on_prop_change(None)

        original_insert = redir.register("insert", my_insert)
        original_delete = redir.register("delete", my_delete)

    def create_one_property(self, label_text, edit_value, edit_type, default_value):
        """
        创建编辑属性所需的控件
        :param label_text: 属性名字
        :param edit_value: 属性值
        :param edit_type: 编辑框类型
        :param default_value: comboBox下拉列表默认值
        :return: None
        """
        self.create_label(label_text)
        self.create_edit(edit_type, edit_value, default_value)
        self.do_layout_col()

    def update_prop_value(self, prop_value):
        """
        更新属性值
        :param prop_value: 属性值
        :return: None
        """
        edit = self.slide_window.children.get("edit", None)
        if edit is None:
            return
        self.is_updating_property = True
        edit.delete(0, END)
        edit.insert(0, prop_value)
        self.is_updating_property = False

    def clear_edit_value(self):
        """
        清除编辑框内容
        :return: None
        """
        edit = self.slide_window.children.get("edit", None)
        if edit is None:
            return
        self.is_updating_property = True
        edit.delete(0, END)
        self.is_updating_property = False

    def on_prop_change(self, event):
        """
        属性更新之后回调
        :param event:
        :return:
        """
        if self.is_updating_property:
            return

        label = self.slide_window.children.get("label_text", None)
        if label is None:
            return

        edit = self.slide_window.children.get("edit", None)
        if edit is None:
            return

        value = edit.get()
        if not value:
            return

        self.master.master.edit_component.update_property({label['text']: value,}, "prop_list")

    def key_click(self, event):
        if event.keysym in ("Up", "Down"):
            return "break"

    @staticmethod
    def create_default_property(master, component_name, prop=None):

        property_dict = {
            "x": 0, "y": 0,
            "width": 500, "height": 500,
            "borderwidth": 0, "pos_x_default": 3,
        }

        if prop is not None:
            property_dict.update(prop)

        property, info = create_default_component(master, "EditorProperty", component_name, property_dict)

        return property


def collect_font_names():
    """
    获取字体名字
    :return: string
    """
    fonts = ""
    families = tkFont.families()

    for family in families:
        fonts += family + ";"

    PROP_TO_VALUES["font"] = fonts


class EditorPropertyList(ScrollRows):

    def __init__(self, master=None, cnf={}, **kw):
        ScrollRows.__init__(self, master, cnf, **kw)
        self.all_rows = []                              # 存储所有的行
        self.show_rows = []                             # 存储显示的行
        self.row_height = 24                            # 每行的默认高度
        self.editor = None                              # 编辑器
        self.edit_component = None                      # 当前正在编辑的控件对象
        collect_font_names()

    def set_editor(self, editor):
        self.editor = editor

    def set_edit_component(self, edit_component):
        if self.edit_component is edit_component:
            return
        self.edit_component = edit_component

    def on_update(self):
        ScrollRows.on_update(self)
        self.add_prop_rows()

    def get_sorted_rows(self):

        sorted_rows = []
        show_rows_sort = sorted(self.show_rows)
        for row_name in show_rows_sort:
            row = self.get_row_by_name(row_name)
            if row is None:
                continue
            sorted_rows.append(row)

        return sorted_rows

    def calc_slide_window_width(self):

        pos_x = 0

        for child in self.get_sorted_rows():
            if int(child.place_info()["x"]) + get_pixel_width(child) > pos_x:
                pos_x = int(child.place_info()["x"]) + get_pixel_width(child)

        return pos_x

    def calc_slide_window_height(self):

        pos_y = 0

        for child in self.get_sorted_rows():
            if int(child.place_info()["y"]) + get_pixel_height(child) > pos_y:
                pos_y = int(child.place_info()["y"]) + get_pixel_height(child)

        return pos_y

    def get_layout_children(self):
        sorted_children = sorted(self.show_rows, key=lambda x: int(x.split("_")[1]))
        return sorted_children

    def get_row_by_name(self, name):
        """
        根据名字获取row
        :param name: 名字
        :return: row
        """
        return self.get_child_master().children.get("row_" + name, None)

    def add_row(self, label_text, edit_value, edit_type, default_value="None", is_do_layout=True):
        """
        增加一行
        :param label_text:属性名字
        :param edit_value:属性值
        :param edit_type:edit_type
        :param row_values:comboBox的values
        :param is_do_layout:是否do_layout
        :return:None
        """
        prop = {
            "is_show_scroll_x": 0,
            "is_show_scroll_y": 0,
            "is_always_show_scroll": 0,
            "width": get_pixel_width(self) - 18,
            "height": self.row_height,
        }

        row = EditorProperty.create_default_property(self.get_child_master(), "row_" + label_text, prop)
        self.add_row_base(row, False)
        row.create_one_property(label_text, edit_value, edit_type, default_value)

        if is_do_layout:
            self.do_layout_row()

        return row

    def add_prop_rows(self):
        """
        创建所有属性的row,如果每次重新创建所有的row会卡,所以在初始化后直接创建
        :return: None
        """
        all_name = sorted(get_all_prop_name())
        for prop_name in all_name:
            edit_type = get_prop_type_by_name(prop_name)
            default_values = PROP_TO_VALUES.get(prop_name, "None")
            self.add_row(prop_name, None, edit_type, default_values, False)
            self.all_rows.append(prop_name)
        self.hide_rows()

    def add_show_rows(self, edit_component, is_update_property=True):
        """
        增加要显示的row
        :param edit_component: 编辑控件
        :param is_update_property: 是否更新属性
        :return: None
        """
        self.set_edit_component(edit_component)
        self.hide_rows()

        prop = {"component_name": ""}
        if int(edit_component.component_info.get("is_main", 0)) == 1:
            prop["is_main"] = 1
            prop["title"] = edit_component.component_info.get("title", "demo")

        gui_type = edit_component.component_info.get("gui_type", "None")
        for prop_name in get_default_component_info(gui_type, prop).keys():
            self.show_rows.append(prop_name)

        self.do_layout_row()
        if is_update_property:
            self.update_property(edit_component.component_info)

    def hide_rows(self):
        """
        隐藏所有row
        :return: None
        """
        del self.show_rows[:]
        for row_name in self.all_rows:
            row = self.get_row_by_name(row_name)
            if row is None:
                print("hide_rows error row:" + row_name)
                continue
            row.clear_edit_value()
            row.place_forget()
        self.do_layout_row()

    def update_property(self, component_info, prop_list=None):
        """
        更新属性
        :param component_info: 控件信息
        :param prop_list: 要更新的属性列表
        :return: None
        """
        if prop_list is None:
            prop_list = self.show_rows

        for prop_name in prop_list:
            if prop_name not in self.show_rows:
                continue
            if prop_name not in component_info:
                continue
            row = self.get_row_by_name(prop_name)
            if not row:
                continue
            row.update_prop_value(component_info[prop_name])