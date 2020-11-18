#!/usr/bin/python
# -*- coding: UTF-8 -*-

import configparser


# 默认的configParser会强制转换大写为小写
class ToolConfigParser(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


