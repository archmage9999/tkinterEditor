#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import END
from componentProperty import update_single_prop
from componentDragAble import ComponentDragAble

class editComponent(ComponentDragAble):

    def __init__(self, editor, component, component_info, component_master, parent):
        ComponentDragAble.__init__(self)
        self.editor = editor
        self.component = component
        self.component_info = component_info
        self.component_master = component_master
        self.parent = parent
        self.children = []
        self.can_not_move = ("Toplevel")
        self.can_not_sizing = (
            "Label", "Button", "Checkbutton", "Entry", "Text", "Listbox", "Scrollbar", "Toplevel",
            "Treeview", "Message", "Radiobutton", "Scale", "Spinbox", "Separator", "Progressbar"
        )

    def set_component_info(self, component_info):
        if self.component_info is component_info:
            return
        self.component_info = component_info

    def get_component_info(self):
        return self.component_info

    @property
    def name(self):
        return self.component_info["component_name"]

    @property
    def gui_type(self):
        return self.component_info["gui_type"]

    def find_edit_component(self, component):
        """
        查找
        :param component: 控件
        :return: editComponent
        """
        if component is self.component:
            return self

        for child in self.children:
            m = child.find_edit_component(component)
            if m is None:
                continue
            return m

        return None

    def add_child(self, edit_component, is_quick_create):
        """
        增加child
        :param edit_component: editComponent
        :param is_quick_create: 是否是从功能快捷键创建的
        :return: None
        """
        self.children.append(edit_component)
        if is_quick_create:
            self.component_info.setdefault("children", []).append(edit_component.get_component_info())
            self.editor.treeview.add_node(self.name, edit_component.name, edit_component, END, edit_component.name)
            self.editor.treeview.tree.item(self.name, open=True)

    def select_first_child(self):
        """
        选中第一个child
        :return: None
        """
        if len(self.children) <= 0:
            return
        child = self.children[0]
        self.editor.on_edit_component_selected(child, False, None)

    def on_edit_component_select(self, is_tree_select):
        """
        被选中时
        :return: None
        """
        self.editor.property_list.add_show_rows(self)
        if not is_tree_select:
            self.editor.treeview.tree.selection_set(self.name)
        self.component.master.configure(highlightthickness=2)

    def on_edit_component_cancel_select(self):
        """
        取消选中时
        :return: None
        """
        if not self.component or not self.component.master:
            return

        self.component.master.configure(highlightthickness=0)

    def update_property(self, prop_dict, not_update=None):
        """
        更新属性
        :param prop_dict: key:属性名,value:属性值
        :param not_update: 不更新的
        :return: None
        """
        try:
            # 更新属性信息
            self.component_info.update(prop_dict)

            # 更新属性列表
            if not_update != "prop_list":
                self.editor.property_list.update_property(self.component_info, prop_dict.keys())

            # 更新控件属性
            if not_update != "component":
                for prop_name, prop_value in prop_dict.items():
                    # 更改坐标的话修改控件的parent
                    if prop_name in ("x", "y", "anchor"):
                        update_single_prop(self.component.master, prop_name, prop_value, "Frame")
                        continue
                    update_single_prop(self.component, prop_name, prop_value, self.gui_type)
                    # 更改图片的话更新一下尺寸
                    if prop_name == "image" and prop_value not in ("", "None"):
                        self.update_property({"width":0, "height":0,}, "component")
                    # 更改尺寸相关的话修改控件的parent
                    if prop_name in ("image", "width", "height", "borderwidth", "highlightthickness", "padx", "pady",
                        "relief", "font"):
                        width = self.component.winfo_reqwidth() + 4
                        height = self.component.winfo_reqheight() + 4
                        if self.gui_type in ("Progressbar", "Scrollbar", "Separator"):
                            width = int(self.component_info["width"]) + 4
                            height = int(self.component_info["height"]) + 4
                        update_single_prop(self.component.master, "width", width, "Frame")
                        update_single_prop(self.component.master, "height", height, "Frame")
                    # 更改背景的话更新一下child的背景
                    if prop_name == "background":
                        for child in self.children:
                            update_single_prop(child.component.master, "background", prop_value, "Frame")
                pass

            # 更新树
            if "component_name" in prop_dict:
                self.editor.refresh_tree()
                self.editor.treeview.tree.selection_set(prop_dict["component_name"])
        except Exception as e:
            print(e)

    def delete_self(self):
        """
        删除自己
        :return: None
        """
        if int(self.get_component_info().get("is_main", 0)) == 1:
            return

        parent_info = self.parent.get_component_info()
        if parent_info != None:
            parent_info["children"].remove(self.component_info)

        master = self.component.master
        self.component.destroy()
        master.destroy()
        self.editor.treeview.tree.delete(self.name)

        self.component = None
        self.component_info = None
        self.component_master = None
        self.parent.children.remove(self)

        self.editor.on_edit_component_selected(self.parent, False, None)

    def get_real_component(self, component):
        return component.master

    def change_width(self, component, width):
        """
        修改宽度
        :param component: 控件
        :param width: 宽度
        :return: None
        """
        self.update_property({"width": width,})

    def change_height(self, component, height):
        """
        修改高度
        :param component: 控件
        :param height: 高度
        :return: None
        """
        self.update_property({"height": height,})

    def change_pos_x(self, component, pos_x):
        """
        修改x
        :param component: 控件
        :param pos_x: x
        :return: None
        """
        self.update_property({"x": pos_x, })

    def change_pos_y(self, component, pos_y):
        """
        修改y
        :param component: 控件
        :param pos_y: y
        :return: None
        """
        self.update_property({"y": pos_y, })