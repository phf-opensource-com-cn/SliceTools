#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : object.py
@Time    : 2019/6/13 17:33
@Author  : panhongfa
@Email   : panhongfas@163.com
@Software: PyCharm
@Description : 
"""
__author__ = 'panhongfa'
__project__ = 'SliceTools'

import os


class Object(object):
    def __init__(self, filepaths, excel, exist=1):
        self._paths = filepaths
        self._excel = excel
        self._exist = exist

    def check(self):
        # 验证文件路径是否存在
        if not self._paths:
            print('filepaths is none')
            return False

        elif isinstance(self._paths, (tuple, list)):
            for path in self._paths:
                if not os.path.exists(path):
                    print('path not exists, path: %s' % path)
                    return False

        else:
            if not os.path.exists(self._paths):
                print('path not exists, path: %s' % self._paths)
                return False
            else:
                self._paths = tuple(self._paths)

        # 验证excel文件是否存在
        if os.path.isfile(self._excel) is False:
            print('excel not exists, file: %s' % self._excel)
            return False

        return True

    def modfiyname(self, case_id, small_id, total_id, file, root, exname):
        newname = '{0}_{1}_{2}.{3}'.format(case_id, small_id, total_id, exname)
        oldpath = os.path.join(root, file)
        newpath = os.path.join(root, newname)

        if os.path.exists(newpath):
            newpath = os.path.join(root, '_{0}'.format(newname))
            os.rename(oldpath, newpath)
            print('Repeat file name, root: %s, file: %s, newpath: %s' % (root, file, newpath))
        else:
            os.rename(oldpath, newpath)
            print('Modify file name, root: %s, file: %s, newfile: %s' % (root, file, newname))

    def filter(self, case_id, files):
        samecase = [i for i, x in enumerate(files) if x.find(case_id) != -1]
        return samecase

    def travers(self, path):
        pass

    def writer(self, cases):
        pass


class KfbObject(Object):
    def rename(self, case_id, small_id, total_id, file, root):
        super(KfbObject, self).modfiyname(case_id, small_id, total_id, file, root, exname='kfb')

    def process(self):
        case_set = set()
        for path in self._paths:
            if os.path.exists(path):
                cases = self.travers(path)
            case_set.update(cases)
        self.writer(case_set)

class UnicObject(Object):
    def rename(self, case_id, small_id, total_id, file, root):
        super(UnicObject, self).modfiyname(case_id, small_id, total_id, file, root, exname='TMAP')

    def process(self):
        case_set = set()
        for path in self._paths:
            if os.path.exists(path):
                cases = self.travers(path)
            case_set.update(cases)
        self.writer(case_set)