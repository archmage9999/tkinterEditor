#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from ScrollCanvas import ScrollCanvas
from componentProperty import update_all_property, get_default_component_info, get_pixel_height


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


class ScrollRows(ScrollCanvas):

    def __init__(self, master=None, cnf={}, **kw):
        ScrollCanvas.__init__(self, master, cnf, **kw)
        self.created_row_num = 0                                        # 已创建的行数
        self.row_distance = 1                                           # 行间距
        self.pos_y_default = 0                                          # 列初始位置y
        self.rows = {}                                                  # 存储所有的行

    def get_created_row_num(self):
        return self.created_row_num

    def set_created_row_num(self, created_row_num):
        if self.created_row_num == created_row_num:
            return
        self.created_row_num = created_row_num

    def get_row_distance(self):
        return self.row_distance

    def set_row_distance(self, row_distance):
        if self.row_distance == row_distance:
            return
        self.row_distance = row_distance

    def get_pos_y_default(self):
        return self.pos_y_default

    def set_pos_y_default(self, pos_y_default):
        if self.pos_y_default == pos_y_default:
            return
        self.pos_y_default = pos_y_default

    def on_update(self):
        ScrollCanvas.on_update(self)

    def get_row_by_index(self, index):
        return self.rows.get(index, None)

    def clear_rows(self):
        """
        清空所有row
        :return:None
        """
        for k, v in self.rows.items():
            v.destroy()
        self.set_created_row_num(0)
        self.rows.clear()

    def add_row_base(self, row_control, is_do_layout=True):
        """
        增加一行
        :param row_control:行控件
        :param is_do_layout:是否do_layout
        :return: None
        """
        created_num = self.get_created_row_num()
        self.rows[created_num] = row_control
        self.set_created_row_num(created_num + 1)

        if is_do_layout:
            self.do_layout_row()

    def add_rows_base(self, row_control_list):
        """
        增加多行
        :param row_control_list:行控件
        :return: None
        """
        for col_control in row_control_list:
            self.add_row_base(col_control, False)

        self.do_layout_row()

    def get_sorted_rows(self):

        sorted_keys = sorted(self.rows.keys())
        sorted_rows = []
        for key in sorted_keys:
            sorted_rows.append(self.rows[key])

        return sorted_rows

    def do_layout_row(self):
        """
        重新布局界面
        :return:None
        """
        sorted_children = self.get_sorted_rows()
        pos_y = self.get_pos_y_default()
        for child in sorted_children:
            child.place(x=child.place_info().get("x", 0), y=pos_y)
            pos_y += get_pixel_height(child) + self.get_row_distance()
        self.update_scroll()