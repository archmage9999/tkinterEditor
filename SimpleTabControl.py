#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Frame
from functools import partial


class SimpleTabControl(Frame):

    def __init__(self, master=None, cnf={}, **kw):

        Frame.__init__(self, master, cnf, **kw)
        self.tabs = {}                                  # 所有tab{"btn": tab_button, "frame": tab_frame, "data": data}
        self.tab_index = 0                              # tab索引
        self.cur_tab = None                             # 当前选中的tab
        self.col_distance = 1                           # 列间距
        self.btn_frame_distance = 0                     # btn与frame间距
        self.on_add_tab = None                          # 增加tab回调
        self.on_del_tab = None                          # 删除tab回调
        self.on_select_tab = None                       # 选择tab回调

    def get_tab_index(self):
        return self.tab_index

    def set_tab_index(self, tab_index):
        if self.tab_index == tab_index:
            return
        self.tab_index = tab_index

    def add_tab_index(self, add_num=1):
        self.tab_index += add_num

    def get_cur_tab(self):
        return self.cur_tab

    def set_cur_tab(self, cur_tab):
        if self.cur_tab == cur_tab:
            return
        self.cur_tab = cur_tab

    def get_col_distance(self):
        return self.col_distance

    def set_col_distance(self, col_distance):
        if self.col_distance == col_distance:
            return
        self.col_distance = col_distance
        self.do_layout()

    def get_btn_frame_distance(self):
        return self.btn_frame_distance

    def set_btn_frame_distance(self, btn_frame_distance):
        if self.btn_frame_distance == btn_frame_distance:
            return
        self.btn_frame_distance = btn_frame_distance

    def set_on_add_tab(self, on_add_tab):
        self.on_add_tab = on_add_tab

    def set_on_del_tab(self, on_del_tab):
        self.on_del_tab = on_del_tab

    def set_on_select_tab(self, on_select_tab):
        self.on_select_tab = on_select_tab

    def get_data(self, tab_index=None):
        if tab_index is None:
            tab_index = self.get_cur_tab()
        if tab_index not in self.tabs:
            return None
        return self.tabs[tab_index]["data"]

    def get_tab_frame(self, tab_index=None):
        if tab_index is None:
            tab_index = self.get_cur_tab()
        if tab_index not in self.tabs:
            return None
        return self.tabs[tab_index]["frame"]

    def get_tab_button(self, tab_index=None):
        if tab_index is None:
            tab_index = self.get_cur_tab()
        if tab_index not in self.tabs:
            return None
        return self.tabs[tab_index]["btn"]

    def add_tab_base(self, tab_button, tab_frame, data, is_select_tab=True):
        """
        添加一个新tab
        :param tab_button: tab_button
        :param tab_frame: tab_frame
        :param data: 存储的额外数据
        :param is_select_tab: 增加tab后是否选中这个tab
        :return: None
        """
        tab_index = self.get_tab_index()
        self.tabs[tab_index] = {"btn": tab_button, "frame": tab_frame, "data": data}

        tab_button.set_handle_tab_select(partial(self.tab_select, tab_index))
        tab_button.set_handle_tab_close(partial(self.del_tab, tab_index))

        # 修改frame的size
        tab_frame.place_forget()
        tab_frame.configure(
            width=self["width"],
            height=self["height"] - tab_button.winfo_reqheight() - self.get_btn_frame_distance()
        )

        if hasattr(tab_frame, "on_size_change"):
            tab_frame.on_size_change()

        self.add_tab_index()
        self.do_layout()

        if self.on_add_tab:
            self.on_add_tab(tab_index)

        if is_select_tab:
            self.tab_select(tab_index)

    def tab_select(self, tab_index):
        """
        切换tab
        :param tab_index:要切换到的tab
        :return:None
        """
        cur_tab = self.get_cur_tab()
        if cur_tab == tab_index:
            return

        new_tab_frame = self.get_tab_frame(tab_index)
        if not new_tab_frame:
            return

        new_tab_button = self.get_tab_button(tab_index)
        if not new_tab_button:
            return

        # 隐藏之前的Frame
        if cur_tab is not None:
            cur_tab_button = self.get_tab_button(cur_tab)
            if hasattr(cur_tab_button, "on_tab_cancel_selected"):
                cur_tab_button.on_tab_cancel_selected()
            cur_tab_frame = self.get_tab_frame(cur_tab)
            cur_tab_frame.place_forget()

        # 显示新Frame
        new_tab_frame.place(x=0, y=new_tab_button.winfo_reqheight() + self.get_btn_frame_distance(), anchor="nw")
        if hasattr(new_tab_button, "on_tab_selected"):
            new_tab_button.on_tab_selected()

        self.set_cur_tab(tab_index)
        if self.on_select_tab:
            self.on_select_tab(tab_index)

    def del_tab(self, tab_index):
        """
        删除一个tab
        :param tab_index:要删除的tab
        :return:None
        """
        if tab_index not in self.tabs:
            return

        tab_frame = self.get_tab_frame(tab_index)
        if tab_frame:
            tab_frame.destroy()

        tab_button = self.get_tab_button(tab_index)
        if tab_button:
            tab_button.destroy()

        # 删除控件回调
        if self.on_del_tab:
            self.on_del_tab(tab_index)

        del self.tabs[tab_index]

        # 重新布局界面
        self.do_layout()

        # 如果删除的是当前选中的则选中第一个
        if self.get_cur_tab() == tab_index:
            self.set_cur_tab(None)
            self.select_first()

    def select_first(self):
        """
        todo:选中第一个tab,以后考虑改成选中上次选中的
        :return:None
        """
        if len(self.tabs) == 0:
            self.set_cur_tab(None)
            return

        first_tab = sorted(self.tabs.keys())[0]
        self.tab_select(first_tab)

    def do_layout(self):
        """
        重新布局界面
        :return:None
        """
        tab_buttons = [self.tabs[k]["btn"] for k in sorted(self.tabs.keys())]
        pos_x = 0
        for tab_button in tab_buttons:
            tab_button.place_configure(x=pos_x, y=0, anchor="nw")
            pos_x += tab_button.winfo_reqwidth() + self.get_col_distance()