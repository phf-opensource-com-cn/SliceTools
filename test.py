#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/6/12 18:09
@Author  : panhongfa
@Email   : panhongfas@163.com
@Software: PyCharm
@Description : 
"""
__author__ = 'panhongfa'
__project__ = 'SliceTools'

import numpy
from tifffile import tifffile as tif


if __name__ == '__main__':
    data0 = numpy.random.randint(0, 255, (301, 219, 3), 'uint8')
    data1 = numpy.random.randint(0, 255, (421, 301, 3), 'uint8')

    subsampling = ['444', '422', '420', '411']
    for subsampling in ['444', '422', '420', '411']:
        filename = 'compress_jpeg_%s.tif' % (subsampling)
        subsampling, atol = {'444': [(1, 1), 5],
                             '422': [(2, 1), 10],
                             '420': [(2, 2), 20],
                             '411': [(4, 1), 40], }[subsampling]

        with tif.TiffWriter(filename) as tiff:
            tiff.save(data0, compress=('JPEG', 99), subsampling=subsampling, tile=(32, 32))
            tiff.save(data1, compress=('JPEG', 99), photometric='RGB', rowsperstrip=32)
