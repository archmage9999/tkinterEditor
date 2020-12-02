#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from tkinter import INSERT, END, Toplevel, Text
from code import InteractiveInterpreter
from WidgetRedirector import WidgetRedirector

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


class DebugInterpreter(InteractiveInterpreter):

    def __init__(self, master, locals=sys.modules["__main__"].__dict__):
        InteractiveInterpreter.__init__(self, locals=locals)
        self.master = master
        sys.stdout.write = master.debug_write
        sys.stderr.write = master.debug_error_write

    def send_msg(self, msg):
        """
        发送消息
        :param msg: 消息
        :return: None
        """
        file_name = "DebugInterpreter"
        lines = msg.split("\n")

        symbol = "single"
        if len(lines) > 1:
            symbol = "exec"

        self.runsource(msg, file_name, symbol)


class DebugInterpreterFrame(Toplevel):

    def __init__(self, master=None, cnf={}, **kw):
        Toplevel.__init__(self, master, cnf, **kw)
        self.input_width = 10
        self.input_height = 1
        self.input_pos_y = 1
        self.output_width = 10
        self.output_height = 1
        self.debug_history = []                             # 存储调试历史信息
        self.cur_debug_history_index = 0                    # 当前调试历史信息索引
        self.max_debug_history = 50                         # 最多存储调试历史条数
        self.debug_interpreter = DebugInterpreter(self)

    def set_input_width(self, input_width):
        if self.input_width == input_width:
            return
        self.input_width = input_width
        self.do_layout()

    def get_input_width(self):
        return self.input_width

    def set_input_height(self, input_height):
        if self.input_height == input_height:
            return
        self.input_height = input_height
        self.do_layout()

    def get_input_height(self):
        return self.input_height

    def set_output_width(self, output_width):
        if self.output_width == output_width:
            return
        self.output_width = output_width
        self.do_layout()

    def get_output_width(self):
        return self.output_width

    def set_output_height(self, output_height):
        if self.output_height == output_height:
            return
        self.output_height = output_height
        self.do_layout()

    def get_output_height(self):
        return self.output_height

    def set_input_pos_y(self, input_pos_y):
        if self.input_pos_y == input_pos_y:
            return
        self.input_pos_y = input_pos_y
        self.do_layout()

    def get_input_pos_y(self):
        return self.input_pos_y

    @property
    def debug_input(self):
        return self.children.get("debug_input", None)

    @property
    def debug_output(self):
        return self.children.get("debug_output", None)

    def on_update(self):
        """
        初始化后会被调用，在这里创建输入框和输出框
        :return: None
        """
        input_prop = {
            "background": "white", "foreground": "black",
            "width": self.get_input_width(), "height": self.get_input_height(),
        }
        create_default_component(self, "Text", "debug_input", input_prop)

        output_prop = {
            "background": "black", "foreground": "white",
            "width": self.get_output_width(), "height": self.get_output_height()
        }
        create_default_component(self, "Text", "debug_output", output_prop)
        self.do_layout()

        copy_right = 'Type "help", "copyright", "credits" or "license" for more information.'
        self.debug_interpreter.write("Python %s on %s\n%s\n(%s)\n" % (sys.version, sys.platform, copy_right,self.__class__.__name__))

        redir = WidgetRedirector(self.debug_input)

        def input_insert(*args):
            if args[1] == "\n":
                self.save_debug_history()
            original_insert(*args)

        def input_delete(*args):
            original_delete(*args)

        original_insert = redir.register("insert", input_insert)
        original_delete = redir.register("delete", input_delete)

        def send_msg():
            msg = self.debug_input.get(0.0, "end")
            msg = msg.strip("\n")
            if not msg:
                return
            self.save_debug_history()
            self.debug_interpreter.send_msg(msg)
            self.debug_input.delete(0.0, "end")
            return "break"

        def press_alt_up(event):
            self.insert_debug_history(-1)
            return 'break'

        def press_alt_down(event):
            self.insert_debug_history(1)
            return 'break'

        self.debug_input.bind("<Alt-Key-Return>", lambda event: send_msg())
        self.debug_input.bind("<Alt-Key-s>", lambda event: send_msg())
        self.debug_input.bind("<Alt-Up>", lambda event: press_alt_up(event))
        self.debug_input.bind("<Alt-Down>", lambda event: press_alt_down(event))

    def save_debug_history(self):
        """
        保存调试历史信息
        :return: None
        """
        line_row_no = self.debug_input.index("insert").split('.')[0]
        msg = self.debug_input.get('{}.0'.format(line_row_no), 'insert')
        if not msg:
            return

        self.debug_history.append(msg)
        if len(self.debug_history) >= self.max_debug_history:
            self.debug_history.pop(0)
        self.cur_debug_history_index = len(self.debug_history)

    def insert_debug_history(self, step):
        """
        插入历史信息
        :param step: 步长
        :return: None
        """
        if len(self.debug_history) == 0:
            return

        new_index = self.cur_debug_history_index + step
        line_row_no = self.debug_input.index("insert").split('.')[0]
        self.debug_input.delete('%s.0' % line_row_no, 'insert')

        if step > 0 and new_index >= len(self.debug_history):
            return

        if step < 0 and new_index < 0:
            new_index = len(self.debug_history) - 1

        self.cur_debug_history_index = new_index

        history = self.debug_history[self.cur_debug_history_index]
        self.debug_input.insert('%s.0' % line_row_no, history)

    def do_layout(self):
        """
        布局
        :return: None
        """
        # todo：之后输入与输出框改成动态计算的，目前先不处理

        self.debug_output.configure(width=self.get_output_width(), height=self.get_output_height())
        self.debug_input.configure(width=self.get_input_width(), height=self.get_input_height())
        self.debug_output.place(x=0, y=0, anchor='nw')
        self.debug_input.place(x=0, y=self.get_input_pos_y(), anchor='nw')

    def debug_write(self, msg):
        """
        调试窗口写函数回调
        :param msg: 写的内容
        :return: None
        """
        if msg == "\n":
            return

        str_output = ">>> "
        self.debug_output.insert("end", str_output + msg + "\n")
        self.debug_output.see("end")

    def debug_error_write(self, msg):
        """
        调试窗口error函数回调
        :param msg: error的内容
        :return: None
        """
        str_output = ">>> "
        self.debug_output.insert("end", str_output + msg + "\n")
        self.debug_output.see("end")
