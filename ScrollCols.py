#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from tkinter import Button
from ScrollCanvas import ScrollCanvas
from componentProperty import update_all_property, get_default_component_info, get_pixel_width


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


class ScrollCols(ScrollCanvas):

    def __init__(self, master=None, cnf={}, **kw):
        ScrollCanvas.__init__(self, master, cnf, **kw)
        self.created_col_num = 0                                    # 已创建的列数
        self.col_distance = 1                                       # 列间距
        self.pos_x_default = 0                                      # 列初始位置x
        self.cols = {}                                              # 存储所有的列

    def get_created_col_num(self):
        return self.created_col_num

    def set_created_col_num(self, created_col_num):
        if self.created_col_num == created_col_num:
            return
        self.created_col_num = created_col_num

    def get_col_distance(self):
        return self.col_distance

    def set_col_distance(self, col_distance):
        if self.col_distance == col_distance:
            return
        self.col_distance = col_distance

    def get_pos_x_default(self):
        return self.pos_x_default

    def set_pos_x_default(self, pos_x_default):
        if self.pos_x_default == pos_x_default:
            return
        self.pos_x_default = pos_x_default

    def on_update(self):
        ScrollCanvas.on_update(self)

    def get_col_by_index(self, index):
        return self.cols.get(index, None)

    def clear_cols(self):
        """
        清空所有列
        :return: None
        """
        for k, v in self.cols.items():
            v.destroy()
        self.set_created_col_num(0)
        self.cols.clear()

    def add_col_base(self, col_control, is_do_layout=True):
        """
        增加一列
        :param col_control: 列控件
        :param is_do_layout: 是否重新布局
        :return: None
        """
        created_num = self.get_created_col_num()
        self.cols[created_num] = col_control
        self.set_created_col_num(created_num + 1)

        if is_do_layout:
            self.do_layout_col()

    def add_cols_base(self, col_control_list):
        """
        增加多列
        :param col_control_list: 列控件列表
        :return: None
        """
        for col_control in col_control_list:
            self.add_col_base(col_control, False)

        self.do_layout_col()

    def get_sorted_cols(self):

        sorted_keys = sorted(self.cols.keys())
        sorted_cols = []
        for key in sorted_keys:
            sorted_cols.append(self.cols[key])

        return sorted_cols

    def do_layout_col(self):
        """
        重新布局界面
        :return: None
        """
        sorted_children = self.get_sorted_cols()
        pos_x = self.get_pos_x_default()
        for child in sorted_children:
            child.place(x=pos_x, y=child.place_info().get("y", 0))
            pos_x += get_pixel_width(child) + self.get_col_distance()
        self.update_scroll()


class ScrollButtonCols(ScrollCols):

    def __init__(self, master=None, cnf={}, **kw):
        ScrollCols.__init__(self, master, cnf, **kw)

    def on_update(self):
        ScrollCols.on_update(self)

    def add_col(self, prop, is_do_layout):
        btn, info = create_default_component(self.get_child_master(), "Button", "None", prop, False)
        self.add_col_base(btn, is_do_layout)
        return btn