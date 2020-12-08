#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from tkinter import Canvas, Frame, Scrollbar
from componentProperty import update_all_property, get_default_component_info, get_pixel_width, get_pixel_height


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


class ScrollCanvas(Canvas):

    def __init__(self, master=None, cnf={}, **kw):

        Canvas.__init__(self, master, cnf, **kw)
        self.is_show_scroll_x = 1                                         # 是否显示水平滚动条
        self.is_show_scroll_y = 1                                         # 是否显示垂直滚动条
        self.is_always_show_scroll = 1                                    # 是否总是显示滚动条
        self.scroll_x_height = 17                                         # 水平滑动条默认高度
        self.scroll_x_width = 200                                         # 水平滑动条默认宽度
        self.scroll_y_height = 200                                        # 垂直滑动条默认高度
        self.scroll_y_width = 17                                          # 垂直滑动条默认宽度

    def set_is_show_scroll_x(self, is_show_scroll_x):
        """
        设置是否显示水平滑动条
        :param is_show_scroll_x:是否显示
        :return:None
        """
        if self.is_show_scroll_x == is_show_scroll_x:
            return
        self.is_show_scroll_x = is_show_scroll_x
        self.do_layout_need_control()

    def get_is_show_scroll_x(self):
        """
        获取是否显示水平滑动条
        :return:bool
        """
        return self.is_show_scroll_x

    def set_is_show_scroll_y(self, is_show_scroll_y):
        """
        设置是否显示垂直滑动条
        :param is_show_scroll_y:是否显示
        :return:None
        """
        if self.is_show_scroll_y == is_show_scroll_y:
            return
        self.is_show_scroll_y = is_show_scroll_y
        self.do_layout_need_control()

    def get_is_show_scroll_y(self):
        """
        获取是否显示垂直滑动条
        :return:bool
        """
        return self.is_show_scroll_y

    def set_is_always_show_scroll(self, is_always_show_scroll):
        """
        设置是否一直显示滑动条
        :param is_always_show_scroll:是否一直显示
        :return:None
        """
        if self.is_always_show_scroll == is_always_show_scroll:
            return
        self.is_always_show_scroll = is_always_show_scroll
        self.do_layout_need_control()

    def get_is_always_show_scroll(self):
        """
        获取是否一直显示滑动条
        :return:bool
        """
        return self.is_always_show_scroll

    @property
    def scroll_bar_x(self):
        return self.children.get("scroll_bar_x", None)

    @property
    def scroll_bar_y(self):
        return self.children.get("scroll_bar_y", None)

    @property
    def slide_window(self):
        return self.children.get("slide_window", None)

    def on_update(self):
        """
        初始化后会被调用，在这里创建滚动条和滑动窗口
        :return: None
        """
        self.create_need_control()
        self.update_scroll()

    def create_need_control(self):
        """
        创建所需控件
        :return:None
        """
        self.create_slide_window()
        self.create_scroll_bar()
        self.do_layout_need_control()

    def create_slide_window(self):
        """
        创建滑动窗口
        :return:None
        """
        prop = {
            "background": self["background"],
        }
        create_default_component(self, "Frame", "slide_window", prop)
        self.create_window((1, 1), window=self.slide_window, anchor="nw")

        self.slide_window.bind("<MouseWheel>", self.scroll_slide_window_y)
        self.slide_window.bind("<Control-MouseWheel>", self.scroll_slide_window_x)

    def create_scroll_bar(self):
        """
        创建滑动条
        :return:None
        """
        prop_scroll_y = {
            "command": self.yview,
            "pixel_width": self.scroll_y_width, "pixel_height": self.scroll_y_height
        }
        create_default_component(self, "Scrollbar", "scroll_bar_y", prop_scroll_y)

        prop_scroll_x = {
            "orient": "horizontal", "command": self.xview,
            "pixel_width":self.scroll_x_width, "pixel_height":self.scroll_x_height
        }
        create_default_component(self, "Scrollbar", "scroll_bar_x", prop_scroll_x)

        # 绑定滑动条事件
        self.configure(xscrollcommand=self.scroll_bar_x.set)
        self.configure(yscrollcommand=self.scroll_bar_y.set)

    def do_layout_need_control(self):
        """
        重新布局界面
        :return:None
        """
        self.do_layout_scroll_bar_x()
        self.do_layout_slide_window()
        self.do_layout_scroll_bar_y()

    def do_layout_scroll_bar_x(self):
        """
        重新布局水平滑动条
        :return: None
        """
        if self.scroll_bar_x is None:
            return

        self.scroll_bar_x.place_configure(x=1, y=get_pixel_height(self) - self.scroll_x_height)
        self.scroll_bar_x.place_configure(width=get_pixel_width(self) - get_pixel_width(self.scroll_bar_y) - 1)
        self.scroll_bar_x.place_configure(height=self.scroll_x_height)

        # 隐藏水平滑动条
        if not self.get_is_show_scroll_x():
            self.scroll_bar_x.place_forget()

    def do_layout_scroll_bar_y(self):
        """
        重新布局垂直滑动条
        :return: None
        """
        if self.scroll_bar_y is None:
            return

        self.scroll_bar_y.place_configure(x=get_pixel_width(self) - int(self.scroll_y_width), y=2)
        self.scroll_bar_y.place_configure(width=self.scroll_y_width)
        self.scroll_bar_y.place_configure(height=get_pixel_height(self) - 2)

        # 隐藏垂直滑动条
        if not self.get_is_show_scroll_y():
            self.scroll_bar_y.place_forget()

    def do_layout_slide_window(self):
        """
        重新布局slide window
        :return: None
        """
        if self.slide_window is None:
            return

        self.slide_window.configure(width=get_pixel_width(self))
        self.slide_window.configure(height=get_pixel_height(self))

    def update_scroll(self):
        """
        更新滑动条
        :return:None
        """
        self.update_scroll_vertical()
        self.update_scroll_horizontal()
        self.configure(scrollregion=self.bbox("all"))

    def update_scroll_vertical(self):
        """
        更新垂直滑动条
        :return:None
        """
        pos_y = self.calc_slide_window_height()
        is_always_show = self.get_is_always_show_scroll()

        visible = False
        if pos_y > get_pixel_height(self):
            self.slide_window.configure(height=pos_y + 20)
            visible = True
        else:
            if int(self.slide_window["height"]) > get_pixel_height(self):
                self.slide_window.configure(height=get_pixel_height(self) - self.scroll_x_height)

        # 一直显示垂直滑动条
        if is_always_show:
            visible = True

        if not self.get_is_show_scroll_y():
            visible = False

        if visible:
            self.do_layout_scroll_bar_y()
        else:
            self.scroll_bar_y.place_forget()

    def calc_slide_window_height(self):
        """
        计算滑动窗口的高度
        :return: int
        """
        pos_y = 0

        for (childName, child) in self.slide_window.children.items():
            if int(child.place_info()["y"]) + get_pixel_height(child) > pos_y:
                pos_y = int(child.place_info()["y"]) + get_pixel_height(child)

        return pos_y

    def update_scroll_horizontal(self):
        """
        更新水平滑动条
        :return:None
        """
        pos_x = self.calc_slide_window_width()
        is_always_show = self.get_is_always_show_scroll()

        visible = False
        if pos_x > get_pixel_width(self):
            self.slide_window.configure(width=pos_x + 20)
            visible = True
        else:
            if int(self.slide_window["width"]) > get_pixel_width(self):
                self.slide_window.configure(width=get_pixel_width(self) - self.scroll_y_width)

        # 一直显示垂直滑动条
        if is_always_show:
            visible = True

        if not self.get_is_show_scroll_x():
            visible = False

        if visible:
            self.do_layout_scroll_bar_x()
        else:
            self.scroll_bar_x.place_forget()

    def calc_slide_window_width(self):
        """
        计算滑动窗口的宽度
        :return: int
        """
        pos_x = 0

        for (childName, child) in self.slide_window.children.items():
            if int(child.place_info()["x"]) + get_pixel_width(child) > pos_x:
                pos_x = int(child.place_info()["x"]) + get_pixel_width(child)

        return pos_x

    def scroll_slide_window_y(self, event):
        """
        垂直滚动页面
        :param event:
        :return:None
        """
        if int(self.slide_window["height"]) <= get_pixel_height(self):
            return
        units = -5 if event.delta > 0 else 5
        self.yview_scroll(units, "units")

    def scroll_slide_window_x(self, event):
        """
        水平滚动页面
        :param event:
        :return:None
        """
        if int(self.slide_window["width"]) <= get_pixel_width(self):
            return
        units = -5 if event.delta > 0 else 5
        self.xview_scroll(units, "units")

    def get_child_master(self):
        return self.slide_window

    def on_end_drag_master(self):
        self.update_scroll()

    def on_size_change(self):
        """
        窗口尺寸变化时的处理
        :return: None
        """
        self.do_layout_need_control()

    def refresh_slide_window_bg(self):
        """
        刷新slide_window背景
        :return: None
        """
        prop = {
            "background": self["background"],
        }
        self.slide_window.configure(prop)

    @staticmethod
    def create_default(master, prop=None):
        return create_default_component(master, "ScrollCanvas", None, prop, False)
