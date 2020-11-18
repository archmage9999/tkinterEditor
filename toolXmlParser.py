#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.dom.minidom as minidom
from xml.dom.minidom import Document


class ToolXmlParser:

    def __init__(self):
        pass

    def write_dict_to_doc(self, doc, node, info_dict, ignore_keys):
        """
        将info_dict写入doc
        :param doc:xml文档
        :param node:写入的节点
        :param info_dict:信息字典
        :param ignore_keys:不存储的keys
        :return:None
        """
        sorted_keys = sorted(info_dict.keys())
        for k in sorted_keys:
            if k in ignore_keys:
                continue
            v = info_dict[k]
            if isinstance(v, dict):
                child_node = doc.createElement(k)
                node.appendChild(child_node)
                self.write_dict_to_doc(doc, child_node, v, ignore_keys)
                continue
            child_node = doc.createElement(k)
            node.appendChild(child_node)
            if k == "children":
                sorted_children = sorted(v, key=lambda x: x["component_name"])
                for child in sorted_children:
                    child_node_2 = doc.createElement(child["component_name"])
                    child_node.appendChild(child_node_2)
                    self.write_dict_to_doc(doc, child_node_2, child, ignore_keys)
                continue
            text_node = doc.createTextNode(str(v))
            child_node.appendChild(text_node)

    def write_dict_to_xml(self, file_path, info_dict, root_name, ignore_keys=()):
        """
        将字典写入xml文件
        :param file_path:文件路径
        :param info_dict:将要写入的字典信息
        :param root_name:根节点名称
        :param ignore_keys:不存储的keys
        :return:None
        """
        # 创建dom文档
        doc = Document()

        # 创建根节点
        root = doc.createElement(root_name)
        doc.appendChild(root)

        # 读取info_dict
        self.write_dict_to_doc(doc, root, info_dict, ignore_keys)

        # 写入xml
        with open(file_path, "wb") as f:
            f.write(doc.toprettyxml(indent="\t", encoding="utf-8"))

    def load_node_to_dict(self, node, info_dict):
        """
        从node中读取信息到info_dict
        :param node:节点
        :param info_dict:读取到的字典
        :return:None
        """
        for child in node.childNodes:
            if child.nodeType != node.ELEMENT_NODE:
                continue
            if len(child.childNodes) == 1 and child.firstChild.nodeType == node.TEXT_NODE:
                info_dict[child.nodeName] = child.firstChild.nodeValue
                continue
            if child.nodeName == "children":
                info_dict[child.nodeName] = []
                for child_2 in child.childNodes:
                    if child_2.nodeType != node.ELEMENT_NODE:
                        continue
                    info_dict[child.nodeName].append({})
                    self.load_node_to_dict(child_2, info_dict[child.nodeName][-1])
                continue
            info_dict[child.nodeName] = {}
            self.load_node_to_dict(child, info_dict[child.nodeName])

    def load_xml_to_dict(self, file_path):
        """
        将xml读入到字典
        :param file_path:文件路径
        :return:dict
        """
        f = minidom.parse(file_path)
        root = f.documentElement

        info_dict = {}
        self.load_node_to_dict(root, info_dict)

        return info_dict


