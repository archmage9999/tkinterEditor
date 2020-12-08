#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from tkinter import Frame, Label
from ScrollCanvas import ScrollCanvas
from SimpleTabControl import SimpleTabControl
from componentProperty import update_all_property, get_default_component_info
from componentProperty import get_pixel_height, get_pixel_width


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


class EditorTabControlBtn(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)
        self.label_text = "default"                                 # 标签文字
        self.label_bg = "#1b2529"                                   # 标签背景
        self.label_fg = "white"                                     # 标签文字颜色
        self.close_bg = "#1b2529"                                   # 关闭按钮背景
        self.close_fg = "white"                                     # 关闭按钮文字颜色
        self.close_active_bg = "red"                                # 关闭按钮激活时的颜色
        self.under_line_bg = "red"                                  # 下划线背景
        self.handle_tab_select = None                               # tab_btn选中函数
        self.handle_tab_close = None                                # tab_close函数

    @property
    def tab_label(self):
        return self.children["label_text"]

    @property
    def tab_close(self):
        return self.children["label_close"]

    @property
    def tab_under_line(self):
        return self.children["under_line"]

    def set_label_text(self, label_text):
        if self.label_text == label_text:
            return
        self.label_text = label_text
        self.tab_label.place_configure(width='')
        self.tab_label.configure(text=self.label_text, width=len(self.label_text))
        self.tab_label.place_configure(width=self.tab_label.winfo_reqwidth())
        self.tab_under_line.place_configure(width=get_pixel_width(self.tab_label) + get_pixel_width(self.tab_close))
        self.do_layout()

    def get_label_text(self):
        return self.label_text

    def set_handle_tab_select(self, handle_tab_select):
        if self.handle_tab_select == handle_tab_select:
            return
        self.handle_tab_select = handle_tab_select

    def set_handle_tab_close(self, handle_tab_close):
        if self.handle_tab_close == handle_tab_close:
            return
        self.handle_tab_close = handle_tab_close

    def on_update(self):
        """
        初始化后会被调用，在这里创建所需控件
        :return: None
        """
        self.create_tab_label()
        self.create_tab_close()
        self.create_under_line()
        self.do_layout()

    def create_tab_label(self):
        """
        创建标签
        :return:None
        """
        prop = {
            "text": self.label_text, "width": len(self.label_text),
            "background": self.label_bg, "foreground": self.label_fg,
        }
        label, info = create_default_component(self, "Label", "label_text", prop)
        label.bind("<Button-1>", self.on_tab_label_click)

    def on_tab_label_click(self, event):
        if self.handle_tab_select is None:
            return
        self.handle_tab_select()

    def create_tab_close(self):
        """
        创建关闭按钮
        :return:None
        """
        prop = {
            "text": "x", "width": 2,
            "activebackground": self.close_bg,
            "activeforeground": self.close_active_bg,
            "background": self.close_bg, "foreground": self.close_fg,
        }
        label, info = create_default_component(self, "Label", "label_close", prop)
        label.bind("<Button-1>", self.on_tab_close_click)
        label.bind("<Enter>", self.on_tab_close_enter)
        label.bind("<Leave>", self.on_tab_close_leave)

    def on_tab_close_click(self, event):
        if self.handle_tab_close is None:
            return
        self.handle_tab_close()

    def on_tab_close_enter(self, event):
        self.tab_close.configure(state="active")

    def on_tab_close_leave(self, event):
        self.tab_close.configure(state="normal")

    def create_under_line(self):
        """
        创建under_line
        :return:None
        """
        prop = {
            "width": get_pixel_width(self.tab_label) + get_pixel_width(self.tab_close),
            "background": self.under_line_bg, "height": 2,
        }
        create_default_component(self, "Frame", "under_line", prop)

    def do_layout(self):
        """
        重新布局界面
        :return:None
        """
        self.tab_label.place(x=0, y=3)
        self.tab_close.place(x=get_pixel_width(self.tab_label), y=-5)
        self.tab_under_line.place(x=0, y=get_pixel_height(self.tab_label) + 5)
        self.place_configure(width=get_pixel_width(self.tab_label) + get_pixel_width(self.tab_close))
        self.place_configure(height=int(self.tab_under_line.place_info()["y"]) + get_pixel_height(self.tab_under_line))

    def on_tab_selected(self):
        """
        tab_btn被选中时的回调
        :return:None
        """
        self.set_under_line_visible(True)

    def on_tab_cancel_selected(self):
        """
        tab_btn被取消选中时的回调
        :return:None
        """
        self.set_under_line_visible(False)

    def set_under_line_visible(self, visible):
        """
        设置下划线显隐
        :param visible: 是否显示
        :return: None
        """
        if not visible:
            self.tab_under_line.place_forget()
            return

        self.tab_under_line.place_configure(
            x=0, y=get_pixel_height(self.tab_label) + 5, anchor="nw",
            width=get_pixel_width(self.tab_label) + get_pixel_width(self.tab_close)
        )

    @staticmethod
    def create_default(master, prop=None):

        property_dict = {
            "background": "#1b2529",
        }

        if prop is not None:
            property_dict.update(prop)

        return create_default_component(master, "EditorTabControlBtn", "None", property_dict, False)


class EditorTabControl(SimpleTabControl):

    def __init__(self, master=None, cnf={}, **kw):
        SimpleTabControl.__init__(self, master, cnf, **kw)

    def add_tab(self, btn_prop, frame_prop, data):
        """
        添加新tab
        :param btn_prop: tab_button属性
        :param frame_prop: tab_frame属性
        :param data: 额外数据
        :return: None
        """
        tab_btn = EditorTabControlBtn.create_default(self, btn_prop)[0]
        tab_frame = ScrollCanvas.create_default(self, frame_prop)[0]
        self.add_tab_base(tab_btn, tab_frame, data)