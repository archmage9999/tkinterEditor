#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
geometry_pattern = re.compile("(\d+)x(\d+)\+(-?\d+)\+(-?\d+)")


# 可拖拽模块
class ComponentDragAble:

    def __init__(self):
        # 拖拽起始坐标x
        self.start_x = 0
        # 拖拽起始坐标y
        self.start_y = 0
        # 是否允许横向拖拽
        self.is_able_x = True
        # 是否允许纵向拖拽
        self.is_able_y = True
        # 是否进行横向边缘检测
        self.is_check_side_x = False
        # 是否进行纵向边缘检测
        self.is_check_side_y = False
        # 是否正在拖拽
        self.is_dragging = False
        # 禁止移动
        self.can_not_move = ()

    def set_is_able_x(self, is_able_x):
        if self.is_able_x == is_able_x:
            return
        self.is_able_x = is_able_x

    def set_is_able_y(self, is_able_y):
        if self.is_able_y == is_able_y:
            return
        self.is_able_y = is_able_y

    def set_is_check_side_x(self, is_check_side_x):
        if self.is_check_side_x == is_check_side_x:
            return
        self.is_check_side_x = is_check_side_x

    def set_is_check_side_y(self, is_check_side_y):
        if self.is_check_side_y == is_check_side_y:
            return
        self.is_check_side_y = is_check_side_y

    @staticmethod
    def get_parent_geometry(component):
        geometry = component.master.master.winfo_geometry()
        matched = geometry_pattern.match(geometry)
        return matched.groups()

    def on_begin_drag(self):
        """
        开始拖拽时触发
        :return:None
        """
        self.is_dragging = True

    def on_end_drag(self, component):
        """
        结束拖拽时触发
        :param component: 控件
        :return:None
        """
        self.is_dragging = False
        if hasattr(self.get_real_component(component).master, "master") and \
                self.get_real_component(component).master.master is not None and \
                hasattr(self.get_real_component(component).master.master, "on_end_drag_master"):
            component.master.master.master.on_end_drag_master()

    def on_dragging(self):
        """
        拖拽中触发
        :return:
        """
        pass

    def handle_mouse_click(self, event, component):
        """
        点击鼠标左键触发
        :param event: event
        :param component: 控件
        :return: None
        """
        if event is None:
            return

        if component.__class__.__name__ in self.can_not_move:
            return

        if self.is_able_x:
            self.start_x = event.x

        if self.is_able_y:
            self.start_y = event.y

        if self.is_able_x or self.is_able_y:
            self.on_begin_drag()

    def change_pos_x(self, component, pos_x):
        """
        修改x
        :param component: 控件
        :param pos_x: x
        :return: None
        """
        component.place_configure(x=pos_x)

    def change_pos_y(self, component, pos_y):
        """
        修改y
        :param component: 控件
        :param pos_y: y
        :return: None
        """
        component.place_configure(y=pos_y)

    def get_real_component(self, component):
        return component

    def get_real_component_x(self, component):
        return int(self.get_real_component(component).place_info()["x"])

    def get_real_component_y(self, component):
        return int(self.get_real_component(component).place_info()["y"])

    def handle_mouse_motion(self, event, component):
        """
        鼠标左键点击并移动
        :param event:事件
        :param component: 控件
        :return:None
        """
        if event is None:
            return

        if component.__class__.__name__ in self.can_not_move:
            return

        if not self.is_dragging:
            return

        # 获取parent宽高
        groups = self.get_parent_geometry(component)

        if self.is_able_x:
            # 计算要设置的位置
            to_x = event.x - self.start_x + self.get_real_component_x(component)
            # 对位置进行边缘检测
            if self.is_check_side_x:
                if to_x < 0:
                    to_x = 0
                elif to_x + component.winfo_width() > int(groups[0]):
                    to_x = int(groups[0]) - component.winfo_width()

            # 设置坐标
            if component.__class__.__name__ not in self.can_not_move:
                self.change_pos_x(component, to_x)

        if self.is_able_y:
            # 计算要设置的位置
            to_y = event.y-self.start_y+self.get_real_component_y(component)
            # 对位置进行边缘检测
            if self.is_check_side_y:
                if to_y < 0:
                    to_y = 0
                elif to_y + component.winfo_height() > int(groups[1]):
                    to_y = int(groups[1]) - component.winfo_height()

            # 设置坐标
            if component.__class__.__name__ not in self.can_not_move:
                self.change_pos_y(component, to_y)

        if self.is_able_x or self.is_able_y:
            self.on_dragging()

    def handle_mouse_release(self, event, component):
        """
        鼠标左键释放触发
        :param event:事件
        :param component: 控件
        :return:None
        """
        if event is None:
            return

        if component.__class__.__name__ in self.can_not_move:
            return

        if self.is_able_x:
            self.start_x = 0

        if self.is_able_y:
            self.start_y = 0

        if self.is_able_x or self.is_able_y:
            self.on_end_drag(component)
