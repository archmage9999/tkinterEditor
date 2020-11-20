#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import uuid
import time
import shutil
from copy import deepcopy

from functools import partial

from tkinter import Tk, Menu, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

from componentMgr import componentMgr
from componentEdited import editComponent
from toolConfigParser import ToolConfigParser
from componentProperty import get_default_component_info
from components import create_component_from_dict, create_default_component


EDITOR_THEME_DEFAULT = 0
EDITOR_THEME_BLACK = 1
EDITOR_THEME_WHITE = 2

EDITOR_THEME = {
    EDITOR_THEME_DEFAULT: "#252b39",
    EDITOR_THEME_BLACK: "black",
    EDITOR_THEME_WHITE: "white",
}


class tkinterEditor(componentMgr):

    def __init__(self, master, gui_path):
        componentMgr.__init__(self, master)
        self.config_parser = ToolConfigParser()
        self.config_parser.read("default.ini", encoding="utf-8-sig")
        self.load_from_xml(master, gui_path, True)
        self.theme = EDITOR_THEME_DEFAULT                                       # 主题
        self.right_edit_menu = None                                             # 鼠标右键edit菜单
        self.edit_components = {}                                               # 存储可编辑的控件
        self.selected_component = None                                          # 当前被选中的控件
        self.created_time = 0                                                   # 创建控件时的时间
        self.created_pos_x = 0                                                  # 创建控件时的坐标x
        self.created_pos_y = 0                                                  # 创建控件时的坐标y
        self.is_new_project_show = True                                         # 创建新project界面是否显示
        self.copied_component = None                                            # 复制的控件信息
        self.init_frame()

    @property
    def editor_window(self):
        return self.master.children.get("editor_window", None)

    @property
    def file_tab_window(self):
        return self.editor_window.children.get("file_tab_window", None)

    @property
    def property_list(self):
        return self.editor_window.children.get("property_list", None)

    @property
    def quick_list(self):
        return self.editor_window.children.get("quick_list", None)

    @property
    def treeview(self):
        return self.editor_window.children.get("treeview", None)

    @property
    def top_level(self):
        return self.editor_window.children.get("top_level", None)

    @property
    def entry_location(self):
        return self.top_level.children.get("entry_location", None)

    @property
    def entry_name(self):
        return self.top_level.children.get("entry_name", None)

    def set_selected_component(self, selected_component):
        if self.selected_component is selected_component:
            return
        self.selected_component = selected_component

    def get_selected_component(self):
        return self.selected_component

    def init_frame(self):
        """
        初始化ui
        :return: None
        """
        self.init_menu()
        self.init_theme()
        self.init_file_tab_window()
        self.init_property_list()
        self.init_treeview()
        self.init_quick_btn()
        self.init_top_level()
        self.init_hot_key()

    ################################################ menu ################################################

    def init_menu(self):
        """
        初始化菜单
        :return:None
        """
        main_menu = Menu(self.master, tearoff=0, name="menu")
        self.right_edit_menu = Menu(self.master, tearoff=0)

        for menu_name in self.config_parser.options("menu"):
            menu = Menu(main_menu, tearoff=0, name=menu_name)
            for sub_menu_name_var in self.config_parser.get("menu", menu_name).split(","):
                sub_menu_name, shortcut_key = sub_menu_name_var.split("#")
                menu.add_command(label=sub_menu_name, accelerator=shortcut_key, command=getattr(self, sub_menu_name))
                if menu_name == "edit":
                    self.right_edit_menu.add_command(label=sub_menu_name, accelerator=shortcut_key, command=getattr(self, sub_menu_name))
            main_menu.add_cascade(label=menu_name, menu=menu)
        self.master.config(menu=main_menu)

    ################################################ theme ################################################

    def init_theme(self):
        """
        初始化主题
        :return:None
        """
        theme = int(self.config_parser.get("default", "theme"))
        self.set_theme(theme)

    def get_theme(self):
        return self.theme

    def set_theme(self, theme):
        if self.theme == theme:
            return
        self.theme = theme
        self.on_theme_change()

    def on_theme_change(self):
        """
        当主题切换时调用
        :return: None
        """
        self.file_tab_window.configure(background=EDITOR_THEME[self.theme])
        cur_tab = self.file_tab_window.get_cur_tab()
        if cur_tab is not None:
            frame = self.file_tab_window.get_tab_frame(cur_tab)
            frame.slide_window.configure(background=EDITOR_THEME[self.theme])

        self.config_parser.set("default", "theme", str(self.theme))
        with open('default.ini', 'w', encoding="utf-8-sig") as f:
            self.config_parser.write(f)

    ############################################## tab control ##############################################

    def init_file_tab_window(self):
        """
        初始化file_tab_window
        :return:
        """
        self.file_tab_window.set_on_add_tab(self.on_gui_open)
        self.file_tab_window.set_on_select_tab(self.on_gui_select)
        self.file_tab_window.set_on_del_tab(self.on_gui_close)

    def on_gui_open(self, tab_num):
        """
        当文件读取成功时调用
        :param tab_num: tab编号
        :return: None
        """
        tab_frame = self.file_tab_window.get_tab_frame(tab_num)
        data = self.file_tab_window.get_data(tab_num)

        edit_component = editComponent(self, tab_frame.get_child_master(), {"component_name": "None"}, None, None)
        self.edit_components[data["path"]] = edit_component

        components = self.load_from_xml(tab_frame.get_child_master(), data["path"], False, partial(self.on_component_create, tab_num, False))
        edit_component.set_component_info(components)
        tab_frame.update_scroll()

    def create_component_by_info(self, master, component_info, is_init_main, on_create_success=None):
        """
        暂时重写componentMgr的创建控件函数，主要是为了选中控件时的效果，以后可能会去掉
        :param master: 父控件
        :param component_info: 控件信息
        :param is_init_main: 是否是初始化主界面时调用的
        :param on_create_success: 创建成功回调
        :return: 控件
        """
        # 初始化调用的话直接调父类的就可以
        if is_init_main:
            return componentMgr.create_component_by_info(self, master, component_info, is_init_main, on_create_success)

        gui_type = component_info.get("gui_type", "None")
        if gui_type == "None":
            return None

        # toplevel直接调父类的
        if gui_type == "Toplevel":
            return componentMgr.create_component_by_info(self, master, component_info, is_init_main, on_create_success)

        # 创建一个frame套在真正的控件外面
        frame_prop = {
            "background": master["background"], "highlightcolor": "red",
        }
        frame, info = create_default_component(master, "Frame", "None", frame_prop, False)

        # 创建控件
        component = create_component_from_dict(frame, component_info)
        frame.configure(width=component.winfo_reqwidth() + 4, height=component.winfo_reqheight() + 4)

        # 以下控件需要重新修改宽和高
        if gui_type in ("Progressbar", "Scrollbar", "Separator"):
            frame.configure(width=int(component_info["width"]) + 4, height=int(component_info["height"]) + 4)

        frame.place_configure(x=component_info["x"], y=component_info["y"], anchor=component_info["anchor"])
        component.place_configure(x=0, y=0, anchor="nw")

        if on_create_success:
            on_create_success(component, component_info, master)

        # 创建children
        for child in component_info.get("children", ()):
            if component == None:
                print("create_component error component=" + child["component_name"])
                continue
            master2 = component.get_child_master()
            self.create_component_by_info(master2, child, is_init_main, on_create_success)

        return component

    def on_component_create(self, tab_num, is_quick_create, component, component_info, master):
        """
        控件创建成功回调
        :param tab_num: 标签编号
        :param is_quick_create: 是否是从功能快捷键创建的
        :param component: 控件
        :param component_info: 控件信息
        :param master: 父控件
        :return: None
        """
        data = self.file_tab_window.get_data(tab_num)

        master_edit_component = self.find_edit_component_by_component(master, data["path"])
        if master_edit_component is None:
            print("create component error", component_info)
            return

        if not hasattr(component, "get_child_master"):
            component.get_child_master = partial(self.default_get_child_master, component)

        edit_component = editComponent(self, component, component_info, master, master_edit_component)
        master_edit_component.add_child(edit_component, is_quick_create)

        child_master = component.get_child_master()
        child_master.bind("<Button-1>", partial(self.on_edit_component_selected, edit_component, False))
        child_master.bind("<Button-3>", partial(self.on_edit_component_button_3_click, edit_component))
        child_master.bind("<B1-Motion>", partial(self.on_edit_component_motion, edit_component))
        child_master.bind("<ButtonRelease-1>", partial(self.on_edit_component_btn_release, edit_component))

    def find_edit_component_by_component(self, component, path):
        """
        根据控件获取编辑的控件
        :param component: 控件
        :return: EditComponent
        """
        if path not in self.edit_components:
            return None
        return self.edit_components[path].find_edit_component(component)

    def default_get_child_master(self, component):
        """
        此函数是为了支持我自己写的控件
        :param component: 控件
        :return: 控件
        """
        return component

    def on_gui_select(self, tab_num):
        """
        文件读取成功并且被选中后调用
        :param tab_num: tab编号
        :return: None
        """
        self.cancel_select_component()
        self.property_list.hide_rows()
        data = self.file_tab_window.get_data(tab_num)
        self.refresh_tree()
        self.edit_components[data["path"]].select_first_child()

    def cancel_select_component(self):
        """
        取消控件选中
        :return:None
        """
        if self.get_selected_component() is None:
            return

        self.get_selected_component().on_edit_component_cancel_select()
        self.set_selected_component(None)

    def on_edit_component_selected(self, edit_component, is_tree_select, event):
        """
        当控件被选中
        :param edit_component: 编辑控件
        :param event: event
        :return: None
        """
        edit_component.component.master.focus_force()
        edit_component.handle_mouse_click(event, edit_component.component)
        if self.get_selected_component() is edit_component:
            return

        self.cancel_select_component()
        self.set_selected_component(edit_component)
        edit_component.on_edit_component_select(is_tree_select)

        return "break"

    def on_edit_component_button_3_click(self, edit_component, event):
        """
        鼠标右键控件
        :param edit_component: 编辑控件
        :param event: event
        :return: None
        """
        edit_component.component.event_generate("<Button-1>")
        self.right_edit_menu.post(event.x_root, event.y_root)

    def on_edit_component_motion(self, edit_component, event):
        """
        当控件移动时
        :param edit_component: 编辑控件
        :param event: event
        :return: None
        """
        edit_component.handle_mouse_motion(event, edit_component.component)

    def on_edit_component_btn_release(self, edit_component, event):
        """
        当控件移动停止时
        :param edit_component: 编辑控件
        :param event: event
        :return: None
        """
        edit_component.handle_mouse_release(event, edit_component.component)

    def on_gui_close(self, tab_num):
        """
        当文件关闭
        :param tab_num: tab编号
        :return: None
        """
        data = self.file_tab_window.get_data(tab_num)
        self.edit_components.pop(data["path"])
        self.set_selected_component(None)
        self.property_list.hide_rows()
        self.treeview.clear_all_node()

    ############################################## property list ##############################################

    def init_property_list(self):
        """
        初始化property_list
        :return: None
        """
        self.property_list.set_editor(self)

    ################################################# treeview #################################################

    def init_treeview(self):
        """
        初始化treeview
        :return: None
        """
        # 修改第一列的宽度
        self.treeview.tree.column("#0", width=int(self.treeview["width"]) - 20)

        self.treeview.set_on_select_tree(self.on_select_tree)
        self.treeview.set_editor(self)

    def refresh_tree(self):
        """
        刷新树
        :return: None
        """
        cur_tab = self.file_tab_window.get_cur_tab()
        if cur_tab is None:
            return

        def add_child(parent, parent_index):
            for child in parent.children:
                node_index = self.treeview.add_node(parent_index, child.name, child, "end", child.name)
                add_child(child, node_index)

        data = self.file_tab_window.get_data(cur_tab)
        path = data["path"]
        self.treeview.clear_all_node()

        index = self.treeview.add_root_node(path, path, "root")
        add_child(self.edit_components[path], index)
        self.treeview.open_all_node("root")

    def on_select_tree(self, event):
        """
        选中树节点
        :param event: event
        :return: None
        """
        index = self.treeview.tree.focus()
        component = self.treeview.get_data_by_index(index)
        if not component:
            return

        self.on_edit_component_selected(component, True, None)

    ############################################## quick button ###############################################

    def init_quick_btn(self):
        """
        初始化功能快捷按键
        :return: None
        """
        prop = {"y": 5, "activebackground": "red", "borderwidth": 3, "width": 0,}
        for quick_name in self.config_parser.options("quick_btn"):
            gui_name = self.config_parser.get("quick_btn", quick_name)
            prop.update({"text": quick_name})
            btn = self.quick_list.add_col(prop, False)
            btn.bind("<ButtonRelease-1>", partial(self.on_quick_btn_click, quick_name, gui_name))
        self.quick_list.do_layout_col()

    def on_quick_btn_click(self, quick_name, gui_name, event):
        """
        点击快捷键
        :param gui_name:模块名
        :return:None
        """
        if quick_name == "LoadXml":
            self.load_xml_to_edit_component()
            return

        self.create_control(quick_name, gui_name)

    def load_xml_to_edit_component(self):
        """
        读取xml后创建到当前编辑的component中
        :return: None
        """
        edit_component = self.get_selected_component()
        if edit_component is None:
            return

        file_path = askopenfilename(title=u"选择文件", filetypes=[("xml files", "xml"), ("all files", "*")])
        if not file_path:
            return

        cur_tab = self.file_tab_window.get_cur_tab()
        components = self.load_from_xml(edit_component.component.get_child_master(), file_path, False, partial(self.on_component_create, cur_tab, False))
        for parent_name, component_info in components.items():
            if component_info.get("is_main", "0") == "1":
                component_info["is_main"] = 0
            edit_component.component_info.setdefault("children", []).append(component_info)

        self.refresh_tree()
        self.treeview.tree.selection_set(edit_component.name)

    def create_control(self, quick_name, gui_name, property_dict=None):
        """
        创建控件
        :param quick_name: 快捷按钮名字
        :param gui_name: 控件名字
        :return: None
        """
        if self.get_selected_component() is None:
            return

        child_master = self.get_selected_component().component.get_child_master()
        if time.time() - self.created_time > 2:
            self.created_pos_x = 0
            self.created_pos_y = 0

        control_name = self.create_random_name(gui_name)
        prop = {
            "background": "white", "x": self.created_pos_x, "y": self.created_pos_y,
            "component_name": control_name, "gui_type": gui_name,
        }

        if child_master["background"]== "white":
            prop["background"] = "grey"

        # 创建一个frame套在真正的控件外面
        frame_prop = {
            "background": child_master["background"], "highlightcolor": "red",
        }
        frame, info = create_default_component(child_master, "Frame", "None", frame_prop, False)

        # 创建控件
        if property_dict is not None:
            property_dict["component_name"] = control_name
            property_dict["is_main"] = 0
            property_dict["x"] = prop["x"]
            property_dict["y"] = prop["y"]
            component = create_component_from_dict(frame, property_dict)
        else:
            component, property_dict = create_default_component(frame, gui_name, control_name, prop)

        frame.configure(width=component.winfo_reqwidth() + 4, height=component.winfo_reqheight() + 4)

        # 以下控件需要重新修改宽和高
        if gui_name in ("Progressbar", "Scrollbar", "Separator"):
            frame.configure(width=int(property_dict["width"]) + 4, height=int(property_dict["height"]) + 4)

        frame.place_configure(x=property_dict["x"], y=property_dict["y"], anchor=property_dict["anchor"])
        component.place_configure(x=0, y=0, anchor="nw")

        self.on_component_create(self.file_tab_window.get_cur_tab(), True, component, property_dict, child_master)

        self.created_time = time.time()
        self.created_pos_x += 10
        self.created_pos_y += 10

    ################################################ file menu ################################################

    def new_gui(self, file_path=None, prop=None, component_name=None):
        """
        新建ui
        :param file_path: 文件路径
        :param prop: 额外属性
        :param component_name: 控件名字
        :return: None
        """
        if file_path is None:
            file_path = asksaveasfilename(title=u"选择文件", filetypes=[("xml files", "xml"),])

        if not file_path:
            return

        if not file_path.endswith(".xml"):
            file_path += ".xml"

        if component_name is None:
            component_name = self.create_random_name("frame")

        bg = "grey" if self.get_theme() == EDITOR_THEME_WHITE else "white"
        prop_update = {
            "gui_type": "Frame",
            "is_main": 1,
            "component_name": component_name,
            "title": "demo",
            "background": bg,
        }

        component_info = get_default_component_info("Frame", prop_update)
        if prop is not None:
            component_info.update(prop)

        self.xml_parser.write_dict_to_xml(file_path, {component_name : component_info,}, "root", ("self_component", "parent_component",))
        self._open_gui(file_path)

    def create_random_name(self, gui_name):
        """
        随机生成一个名字
        :param gui_name: 控件名字
        :return: string
        """
        return gui_name.lower() + "_" + str(uuid.uuid1().hex)

    def _open_gui(self, file_path):
        """
        读取ui公共操作
        :param file_path: 文件路径
        :return: None
        """
        file_name = os.path.basename(file_path)
        bg = EDITOR_THEME[self.theme]
        self.file_tab_window.add_tab({"label_text": file_name}, {"background": bg, "is_always_show_scroll": 0,}, {"path": file_path})

    def open_gui(self):
        """
        读取ui文件
        :return: None
        """
        file_path = askopenfilename(title=u"选择文件", filetypes=[("xml files", "xml"), ("all files", "*")])
        if not file_path:
            return

        if file_path in self.edit_components:
            messagebox.showinfo(title='提示', message='该文件已经打开')
            return

        self._open_gui(file_path)

    def save_gui(self):
        """
        保存ui文件
        :return: None
        """
        cur_tab = self.file_tab_window.get_cur_tab()
        if cur_tab is None:
            return None

        data = self.file_tab_window.get_data(cur_tab)
        if not data:
            return None

        self.saves(data["path"], self.edit_components[data["path"]].get_component_info())
        messagebox.showinfo(title='提示', message='保存成功')

    def save_as(self):
        """
        另存为
        :return: None
        """
        cur_tab = self.file_tab_window.get_cur_tab()
        if cur_tab is None:
            return None

        data = self.file_tab_window.get_data(cur_tab)
        if not data:
            return None

        file_path = asksaveasfilename(title=u"选择文件", filetypes=[("xml files", "xml"), ])
        if not file_path:
            return

        if not file_path.endswith(".xml"):
            file_path += ".xml"

        self.saves(file_path, self.edit_components[data["path"]].get_component_info())
        messagebox.showinfo(title='提示', message='保存成功')

    def new_project(self):
        """
        新项目
        :return: None
        """
        self.change_new_project_ui()

    ##################################################### top level ############################################

    def init_top_level(self):
        """
        初始化top_level
        :return: None
        """
        self.top_level.protocol("WM_DELETE_WINDOW", self.change_new_project_ui)
        self.top_level.resizable(width=False, height=False)
        self.top_level.positionfrom(who="program")
        self.top_level.children.get("btn_browse", None).bind("<Button-1>", self.on_top_level_browse_click)
        self.top_level.children.get("btn_cancel", None).bind("<Button-1>", self.on_top_level_cancel_click)
        self.top_level.children.get("btn_ok", None).bind("<Button-1>", self.on_top_level_ok_click)
        self.change_new_project_ui()

    def change_new_project_ui(self):
        """
        打开关闭new_project界面
        :return: None
        """
        if self.is_new_project_show:
            self.is_new_project_show = False
            self.top_level.withdraw()
            self.top_level.master.master.wm_attributes('-disabled', False)
            return
        self.is_new_project_show = True
        self.top_level.deiconify()
        self.top_level.master.master.wm_attributes('-disabled', True)

    def on_top_level_browse_click(self, event):
        """
        点击browse
        :param event: event
        :return: None
        """
        location = askdirectory()
        if not location:
            return

        self.entry_location.delete(0, "end")
        self.entry_location.insert(0, location)

    def on_top_level_cancel_click(self, event):
        """
        点击取消
        :param event: event
        :return: None
        """
        self.change_new_project_ui()
        self.top_level.master.master.deiconify()

    def on_top_level_ok_click(self, event):
        """
        点击ok
        :param event: event
        :return: None
        """
        # 获取项目名
        name = self.entry_name.get()
        if not name:
            print("must insert name")
            return

        # 获取项目目录
        location = self.entry_location.get()
        if not location:
            print("must insert location")
            return

        # 创建项目文件夹
        new_path = os.path.join(location, name)
        os.mkdir(new_path)

        # 创建py文件
        self.create_project_py(new_path, name)

        # 拷贝文件
        self.copy_file(new_path)

        # 创建gui文件
        file_path = os.path.join(new_path, name)
        self.new_gui(file_path, None, "frame_" + name)

        # 关闭界面
        self.change_new_project_ui()
        self.top_level.master.master.deiconify()

    def create_project_py(self, file_path, file_name):
        """
        创建py文件
        :param file_path:文件夹路径
        :param file_name:文件名字
        :return:None
        """
        self.create_init_py(file_path)
        self.create_main_py(file_path, file_name)

    @staticmethod
    def create_init_py(file_path):
        """
        创建init.py
        :param file_path:文件夹路径
        :return:None
        """
        file_name = os.path.join(file_path, "init.py")
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("# -*- coding: UTF-8 -*-\n")

    @staticmethod
    def create_main_py(file_path, name):
        """
        创建main.py
        :param file_path:文件夹路径
        :param name:文件名字
        :return:None
        """
        file_name = os.path.join(file_path, name + ".py")
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(
                "# -*- coding: UTF-8 -*-\n\n"
                "import os\n"
                "from tkinter import *\n"
                "from componentMgr import componentMgr\n\n\n"
                "class {0}(componentMgr):\n\n"
                "    def __init__(self, master, gui_path):\n"
                "        componentMgr.__init__(self, master)\n"
                "        self.load_from_xml(master, gui_path, True)\n\n\n"
                "def main():\n"
                "    root = Tk()\n"
                "    path = os.path.join(os.getcwd(), '{1}.xml')\n"
                "    {2}(root, path)\n"
                "    root.mainloop()\n\n\n"
                "if __name__ == \"__main__\":\n"
                "    main()\n".format(name, name, name)
            )

    @staticmethod
    def copy_file(file_path):
        """
        拷贝文件
        :param file_path:文件路径
        :return:None
        """
        cur_path = os.getcwd()
        mgr_path = os.path.join(cur_path, "componentMgr.py")
        tool_path = os.path.join(cur_path, "toolXmlParser.py")
        component_path = os.path.join(cur_path, "componentBase.py")
        property_path = os.path.join(cur_path, "componentProperty.py")

        shutil.copy(mgr_path, os.path.join(file_path, "componentMgr.py"))
        shutil.copy(tool_path, os.path.join(file_path, "toolXmlParser.py"))
        shutil.copy(component_path, os.path.join(file_path, "components.py"))
        shutil.copy(property_path, os.path.join(file_path, "componentProperty.py"))

    ################################################ edit menu ################################################

    def delete_control(self):
        """
        删除控件
        :return:None
        """
        cur_tab = self.file_tab_window.get_cur_tab()
        if cur_tab is None:
            return

        edit_component = self.get_selected_component()
        if edit_component is None:
            return

        edit_component.delete_self()

    def move_control(self, keysym, event):
        """
        移动控件
        :param keysym:Up,Down,Left,Right
        :return:None
        """
        edit_component = self.get_selected_component()
        if edit_component is None:
            return

        pos_x = int(edit_component.component_info["x"])
        pos_y = int(edit_component.component_info["y"])

        if keysym == "Up":
            edit_component.update_property({"y": pos_y - 1})
        elif keysym == "Down":
            edit_component.update_property({"y": pos_y + 1})
        elif keysym == "Left":
            edit_component.update_property({"x": pos_x - 1})
        else:
            edit_component.update_property({"x": pos_x + 1})

    def move_up(self):
        """
        向上移动控件
        :return: None
        """
        self.move_control("Up", None)

    def move_down(self):
        """
        向下移动控件
        :return: None
        """
        self.move_control("Down", None)

    def move_left(self):
        """
        向左移动控件
        :return: None
        """
        self.move_control("Left", None)

    def move_right(self):
        """
        向右移动控件
        :return: None
        """
        self.move_control("Right", None)

    def copy(self):
        """
        复制控件
        :return: None
        """
        edit_component = self.get_selected_component()
        if edit_component is None:
            return

        self.copied_component = deepcopy(edit_component.get_component_info())

    def paste(self):
        """
        粘贴控件
        :return: None
        """
        if self.copied_component is None:
            return

        gui_type = self.copied_component["gui_type"]
        self.create_control(gui_type, gui_type, deepcopy(self.copied_component))

    ################################################ view menu ################################################

    def change_theme(self):
        """
        更换主题
        :return:
        """
        self.set_theme((self.get_theme() + 1) % len(EDITOR_THEME))

    ############################################### hot key ###################################################

    def init_hot_key(self):
        """
        初始化快捷键
        :return: None
        """
        self.master.bind("<Control-s>", lambda event: self.save_gui())
        self.master.bind("<Control-o>", lambda event: self.open_gui())
        self.master.bind("<Control-n>", lambda event: self.new_gui())
        self.master.bind("<Control-p>", lambda event: self.new_project())
        self.master.bind("<Control-Delete>", lambda event: self.delete_control())
        self.master.bind("<Control-c>", lambda event: self.copy())
        self.master.bind("<Control-v>", lambda event: self.paste())
        for k in ("Up", "Down", "Left", "Right"):
            self.master.bind("<Control-{0}>".format(k), partial(self.move_control, k))


def main():
    root = Tk()
    #root.resizable(0, 0)
    path = os.path.join(os.getcwd(), "tkinterEditor.xml")
    tkinterEditor(root, path)
    root.mainloop()


if __name__ == "__main__":
    main()






