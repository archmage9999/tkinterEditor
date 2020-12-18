#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Canvas, Event
from functools import partial
from componentProperty import get_pixel_height, get_pixel_width


class ResizingEvent(Event):

    def __init__(self):
        self.add_width = None


class SelectedCanvas(Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        Canvas.__init__(self, master, cnf, **kw)
        self.is_sizing = False
        self.last_width = 0
        self.last_height = 0
        self.last_x = 0
        self.last_y = 0
        self.last_root_x = 0
        self.last_root_y = 0
        self.last_pos_x = 0
        self.last_pos_y = 0
        self.on_resize_complete = None
        self.handle_resizing_end = None

    def set_on_resize_complete(self, on_resize_complete):
        self.on_resize_complete = on_resize_complete

    def set_handle_resizing_end(self, handle_resizing_end):
        self.handle_resizing_end = handle_resizing_end

    def on_update(self):
        """
        初始化后会被调用，在这里绘制矩形
        :return: None
        """
        self.create_rectangle(-1, -1, -2, -2, tag='side', dash=3, outline='red')
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.create_rectangle(-1, -1, -2, -2, tag=name, outline='red')
            self.tag_bind(name, "<Enter>", partial(self.on_mouse_enter, name))
            self.tag_bind(name, "<Leave>", partial(self.on_mouse_leave, name))
            self.tag_bind(name, "<Button-1>", partial(self.on_mouse_click, name))
            self.tag_bind(name, "<B1-Motion>", partial(self.on_mouse_move, name))
            self.tag_bind(name, "<ButtonRelease-1>", partial(self.on_mouse_release, name))

    def show(self, is_fill=False):
        """
        显示
        :param is_fill: 是否填充
        :return: None
        """
        width = get_pixel_width(self)
        height = get_pixel_height(self)
        self.coords('side', 6, 6, width - 6, height - 6)
        self.coords('nw', 0, 0, 7, 7)
        self.coords('sw', 0, height - 8, 7, height - 1)
        self.coords('w', 0, (height - 7) / 2, 7, (height - 7) / 2 + 7)
        self.coords('n', (width - 7) / 2, 0, (width - 7) / 2 + 7, 7)
        self.coords('s', (width - 7) / 2, height - 8, (width - 7) / 2 + 7, height - 1)
        self.coords('ne', width - 8, 0, width - 1, 7)
        self.coords('se', width - 8, height - 8, width - 1, height - 1)
        self.coords('e', width - 8, (height - 7) / 2, width - 1, (height - 7) / 2 + 7)

        fill_color = ''
        if is_fill:
            fill_color = 'red'

        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.itemconfig(name, fill=fill_color)

    def hide(self):
        """
        隐藏
        :return: None
        """
        self.coords('side', -1, -1, -2, -2,)
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.coords(name, -1, -1, -2, -2)

    def on_mouse_enter(self, tag_name, event):
        """
        鼠标进入事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if tag_name in ("nw", "sw", "ne", "se"):
            self["cursor"] = "sizing"
        elif tag_name in ("w", "e"):
            self["cursor"] = "sb_h_double_arrow"
        else:
            self["cursor"] = "sb_v_double_arrow"

    def on_mouse_leave(self, tag_name, event):
        """
        鼠标离开事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if self.is_sizing:
            return
        self["cursor"] = "arrow"

    def on_mouse_click(self, tag_name, event):
        """
        鼠标点击事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        self.is_sizing = True
        self.last_width = self.winfo_width()
        self.last_height = self.winfo_height()
        self.last_x = event.x
        self.last_y = event.y
        self.last_root_x = event.x_root
        self.last_root_y = event.y_root
        self.last_pos_x = int(self.place_info()['x'])
        self.last_pos_y = int(self.place_info()['y'])

    def on_mouse_move(self, tag_name, event):
        """
        鼠标移动事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if not self.is_sizing:
            return

        add_width = add_height = width = height = None
        add_pos_x = add_pos_y = x = y = None

        if 'e' in tag_name:
            add_width = event.x - self.last_x
            self.last_width = width = max(0, self.last_width + add_width)
            self.last_x = event.x

        if 'w' in tag_name:
            add_width = add_pos_x = self.last_root_x - event.x_root
            self.last_width = width = max(0, self.last_width + add_pos_x)
            self.last_root_x = event.x_root
            x = self.last_pos_x = self.last_pos_x - add_pos_x

        if 's' in tag_name:
            add_height = event.y - self.last_y
            self.last_height = height = max(0, self.last_height + add_height)
            self.last_y = event.y

        if 'n' in tag_name:
            add_height = add_pos_y =  self.last_root_y - event.y_root
            self.last_height = height = max(0, self.last_height + add_pos_y)
            self.last_root_y = event.y_root
            y = self.last_pos_y = self.last_pos_y - add_pos_y

        self.on_resizing_end(
            x=x, y=y, width=width, height=height,
            add_pos_x=add_pos_x, add_pos_y=add_pos_y, add_width=add_width, add_height=add_height
        )

    def on_resizing_end(self, **args):

        if self.handle_resizing_end is None:
            configure_data = {}
            for arg in ("width", "height", "x", "y"):
                if args[arg] is None:
                    continue
                configure_data[arg] = args[arg]
            self.place_configure(configure_data)
            self.after_idle(self.show)
            return

        self.handle_resizing_end(**args)

    def on_mouse_release(self, tag_name, event):
        """
        鼠标松开事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        self.is_sizing = False
        if self.on_resize_complete is not None:
            self.on_resize_complete()

        self["cursor"] = "arrow"
