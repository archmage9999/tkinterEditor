#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from tkinter.ttk import Treeview
from ScrollCanvas import ScrollCanvas
from componentProperty import update_all_property, get_default_component_info


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


class EditorTree(ScrollCanvas):

    def __init__(self, master=None, cnf={}, **kw):
        ScrollCanvas.__init__(self, master, cnf, **kw)
        self.root_index = 0                                 # 根节点索引
        self.node_num = 0                                   # 所有节点个数
        self.data = {}                                      # 额外存储的数据
        self.editor = None                                  # 编辑器
        self.on_select_tree = None                          # 选中树的回调
        self.on_select_tree_3 = None                        # 右键树

    def set_editor(self, editor):
        self.editor = editor

    @property
    def tree(self):
        return self.slide_window.children.get("tree", None)

    def get_data_by_index(self, index):
        if index not in self.data:
            return None
        return self.data[index]

    def set_on_select_tree(self, on_select_tree):
        self.on_select_tree = on_select_tree

    def set_on_select_tree_3(self, on_select_tree_3):
        self.on_select_tree_3 = on_select_tree_3

    def on_update(self):
        ScrollCanvas.on_update(self)
        self.create_tree()
        self.update_scroll()

    def create_tree(self):
        """
        创建树
        :return: None
        """
        property_dict = {
            "height": 14,
            "show": "tree",
            "selectmode": "browse",
        }

        tree_view, info = create_default_component(self.slide_window, "Treeview", "tree", property_dict)

        tree_view.bind('<ButtonRelease-1>', self.select_tree)
        tree_view.bind('<ButtonRelease-3>', self.select_tree_3)
        tree_view.bind('<Key>', self.key_press)

    def key_press(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right"):
            return "break"

    def select_tree(self, event):
        if self.on_select_tree != None:
            self.on_select_tree(event)

    def select_tree_3(self, event):
        if self.on_select_tree_3 != None:
            self.on_select_tree_3(event)

    def add_root_node(self, text, values=(), root_name=""):
        """
        增加跟节点
        :param text: 节点标题
        :param values: 节点存的数据
        :return: 节点索引
        """
        if root_name:
            index = self.tree.insert("", self.root_index, root_name, text=text, values=values)
        else:
            index = self.tree.insert("", self.root_index, text=text, values=values)

        self.data[index] = values
        self.add_node_num()

        return index

    def add_node(self, parent_index, text, values=(), add_index='end', index_name=""):
        """
        增加节点
        :param parent_index: 父节点索引
        :param text: 节点标题
        :param values: 节点存的数据
        :param add_index: 添加的节点索引，默认是在最后添加
        :return: 节点索引
        """
        if index_name:
            index = self.tree.insert(parent_index, add_index, index_name, text=text, values=values)
        else:
            index = self.tree.insert(parent_index, add_index, text=text, values=values)

        self.data[index] = values
        self.add_node_num()

        return index

    def add_node_num(self):
        self.node_num += 1
        if self.node_num >= int(self.tree["height"]):
            self.tree.configure(height=int(self.tree["height"])+1)
        self.update_scroll()

    def open_all_node(self, item):
        """
        打开某节点的所有子节点
        :param item: 父节点
        :return: None
        """
        self.tree.item(item, open=True)
        def open_child(parent):
            for child in self.tree.get_children(parent):
                self.tree.item(child, open=True)
                open_child(child)
        open_child(item)

    def clear_all_node(self):
        """
        清除所有节点
        :return: None
        """
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        self.data.clear()
        self.root_index = 0
        self.node_num = 0
        self.update_scroll()