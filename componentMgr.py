#!/usr/bin/python
# -*- coding: utf-8 -*-

from components import create_component_from_dict
from toolXmlParser import ToolXmlParser


class componentMgr:

    def __init__(self, master):
        self.master = master
        self.xml_parser = ToolXmlParser()

    def init_main_frame(self, master, component_info, first_child):
        """
        初始化主界面
        :param master: parent
        :param component_info: 控件信息
        :param first_child: 首个孩子
        :return: None
        """
        # 设置标题
        master.title(component_info["title"])

        # 设置大小与位置
        width = component_info["width"]
        height = component_info["height"]
        pos_x = component_info["x"]
        pos_y = component_info["y"]

        master.geometry("%sx%s+%s+%s" % (width, height, pos_x, pos_y))
        first_child.place(x=0, y=0, anchor=component_info["anchor"])

    def create_component_by_info(self, master, component_info, is_init_main, on_create_success=None):
        """
        创建控件by控件信息
        :param master: parent
        :param component_info: 控件信息
        :param is_init_main: 是否是初始化主界面时调用的
        :param on_create_success: 创建成功回调
        :return: 控件
        """
        gui_type = component_info.get("gui_type", "None")
        if gui_type == "None":
            return None

        # 创建控件
        component = create_component_from_dict(master, component_info)

        # 初始化主界面
        is_main = component_info.get("is_main", 0)
        if is_main == "1" and is_init_main:
            self.init_main_frame(master, component_info, component)

        if on_create_success:
            on_create_success(component, component_info, master)

        # 创建children
        for child in component_info.get("children", ()):
            if component == None:
                print("create_component error component=" + child["component_name"])
                continue
            master2 = component.get_child_master() if hasattr(component, "get_child_master") else component
            self.create_component_by_info(master2, child, is_init_main, on_create_success)

        return component

    def load_from_xml(self, master, gui_path, is_init_main=False, on_create_success=None):
        """
        从xml中读取并创建ui
        :param master: 在这个控件创建
        :param gui_path: 文件名称
        :param is_init_main: 是否初始化主界面
        :param on_create_success: 创建成功回调
        :return: Dict
        """
        components = self.xml_parser.load_xml_to_dict(gui_path)
        for parent_name, component_info in components.items():
            self.create_component_by_info(master, component_info, is_init_main, on_create_success)

        return components

    def saves(self, file_name, component_info):
        """
        将ui存入xml文件
        :param file_name: 文件名字(包括路径)
        :param component_info: 控件信息
        :return: None
        """
        self.xml_parser.write_dict_to_xml(file_name, component_info, "root")
