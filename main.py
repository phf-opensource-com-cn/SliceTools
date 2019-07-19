#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2019/6/5 20:03
@Author  : panhongfa
@Email   : panhongfas@163.com
@Software: PyCharm
@Description : 
"""
__author__ = 'panhongfa'
__project__ = 'SelectKfb'

import os
import re
import sys
import getopt
from kfbscan import KfbScan
from kfbserver import KfbServer
from unicscan import UnicScan
from classifier import Classifier


def check_opts(opts):
    param = {}
    for key, value in opts:
        if key in ['-h', '--help']:
            print('江丰服务器拷贝帮助工具')
            print('参数：')
            print('-h\t 显示帮助信息')
            print('-c\t 包含江丰病理图像的目录')
            print('-b\t 包含麦克奥迪病理图像的基础目录')
            print('-f\t 保存待合并切片信息的excel格式文件路径')
            print('-m\t 需要清理的病理图像目录的类型')
            print('-v\t 标记是否切片是否存在的值')
            return False, None
        if key in ['-c', '--clear']:
            clearpaths = re.split('[,_ ]', value)
            for clearpath in clearpaths:
                if not os.path.exists(clearpath):
                    print('目录不存在，请检查输入参数')
                    return False, None

            if len(clearpaths) > 0:
                param['clearpath'] = clearpaths
            else:
                print('输入非法，请检查输入参数')
                return False, None

        if key in ['-b', '--base']:
            basepath = value
            if not os.path.exists(basepath):
                print('目录不存在，请检查输入参数')
                return False, None
            else:
                param['basepath'] = basepath

        if key in ['-f', '--file']:
            filepath = value
            if os.path.isfile(filepath) is False:
                print('保存待合并切片信息的excel格式文件不存在，请检查输入参数')
                return False, None
            else:
                param['filepath'] = filepath

        if key in ['-m', '--model']:
            model = value
            if model not in ('motic', 'jfserver', 'jfscan', 'unicscan', 'class'):
                print('需要清理的病理图像目录的类型错误，请检查输入参数')
                return False, None
            else:
                param['model'] = model

        if key in ['-v', '--value']:
            exist = int(value)
            if not exist:
                print('数字切片存在标记取值非法，请检查输入参数')
                return False, None
            else:
                param['exist'] = exist

    return True, param

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hb:c:f:m:v:', ['base=', 'clear=', 'file=', 'model=', 'value=', 'help'])
    res, param = check_opts(opts)
    if res is False:
        sys.exit(0)

    if 'model' in param and param['model'] == 'jfscan':
        if 'clearpath' in param and 'filepath' in param:
            clear_paths = param['clearpath']
            excel_path = param['filepath']

            if 'exist' in param:
                exist_value = param['exist']
                kfb = KfbScan(clear_paths, excel_path, exist=exist_value)
            else:
                kfb = KfbScan(clear_paths, excel_path)

            if kfb.check():
                kfb.process()
        else:
            pass

    elif 'model' in param and param['model'] == 'jfserver':
        if 'clearpath' in param and 'filepath' in param:
            clear_paths = param['clearpath']
            excel_path = param['filepath']

            if 'exist' in param:
                exist_value = param['exist']
                kfb = KfbServer(clear_paths, excel_path, exist=exist_value)
            else:
                kfb = KfbServer(clear_paths, excel_path)

            if kfb.check():
                kfb.process()
        else:
            pass

    elif 'model' in param and param['model'] == 'unicscan':
        if 'clearpath' in param and 'filepath' in param:
            clear_paths = param['clearpath']
            excel_path = param['filepath']

            if 'exist' in param:
                exist_value = param['exist']
                unic = UnicScan(clear_paths, excel_path, exist=exist_value)
            else:
                unic = UnicScan(clear_paths, excel_path)

            if unic.check():
                unic.process()
        else:
            pass

    elif 'model' in param and param['model'] == 'class':
        if 'clearpath' in param and 'filepath' in param:
            clear_paths = param['clearpath']
            excel_path = param['filepath']

            cls = Classifier(clear_paths, excel_path)

            if cls.check():
                cls.process()
        else:
            pass
