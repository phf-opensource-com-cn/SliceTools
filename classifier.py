#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : classifier.py
@Time    : 2019/6/21 14:18
@Author  : panhongfa
@Email   : panhongfas@163.com
@Software: PyCharm
@Description : 
"""
__author__ = 'panhongfa'
__project__ = 'SliceTools'

import os
import re
from openpyxl import *
from object import Object


class Classifier(Object):
    def __init__(self, filepaths, excel, exist=1):
        super(Classifier, self).__init__(filepaths, excel, exist)
        self._case_class_set = {}

    def rename(self, root, key, path, name):
        oldpath = os.path.join(root, name)
        newpath = os.path.join(path, key, name)
        if key not in root and oldpath != newpath:
            if os.path.exists(newpath):
                pass
            else:
                os.rename(oldpath, newpath)

    def process(self):
        titles = ('甲状腺', '乳腺', '上消化道', '下消化道')
        self._case_class_set = self.reader(titles)
        for path in self._paths:
            if os.path.exists(path):
                for title in titles:
                    title_path = os.path.join(path, title)
                    if not os.path.exists(title_path):
                        os.mkdir(title_path)
                self.travers(path)

    def reader(self, titles):
        if not titles:
            return None

        case_class_set = {}
        wb = load_workbook(self._excel)
        for ws in wb:
            if ws.title not in titles:
                continue

            key = ws.title
            case_set = set()
            for row in ws.iter_rows(min_row=2):
                case_id = row[0].value
                case_id = str(case_id)
                case_set.add(case_id)
            case_class_set[key] = case_set

        return case_class_set

    def travers(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                [fname, fename] = os.path.splitext(file)
                if fename in ('.kfb', '.TMAP') and not fname.startswith('_'):
                    units = re.split('[-_]', fname)
                    if len(units) == 3:
                        case_id = units[0]
                        for key, case_set in self._case_class_set.items():
                            if case_id in case_set:
                                self.rename(root, key, path, file)
                            else:
                                pass
