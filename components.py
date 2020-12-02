#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from tkinter import *
from tkinter.ttk import Combobox, Treeview, Separator, Progressbar
from componentProperty import update_all_property, get_default_component_info

# 下面导入自己的控件
from EditorTree import EditorTree
from EditorTabControl import EditorTabControl
from ScrollCols import ScrollButtonCols
from ScrollCanvas import ScrollCanvas
from ScrollRows import ScrollRows
from EditorPropertyList import EditorPropertyList
from debugInterpreter import DebugInterpreterFrame


def create_component_from_dict(master, component_info):
    """
    根据字典里面给定的属性创建控件
    :param master: 父控件
    :param component_info: 控件信息
    :return: 创建的控件
    """
    gui_type = component_info["gui_type"]
    class_name = getattr(sys.modules[__name__], gui_type)

    component = class_name(master, name=component_info["component_name"])
    update_all_property(component, component_info, gui_type)

    return component


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