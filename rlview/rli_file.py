# -*- coding: utf-8 -*-

import ctypes
import io
import itertools
import math
import struct

import matplotlib.pyplot as plt
import numpy as np
import skimage
import skimage.io
from skimage.util.dtype import img_as_float

from rlview import tile
import rlview


class SystemTime(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("wYear", ctypes.c_ushort),
                ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort),
                ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort),
                ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort),
                ("wMilliseconds", ctypes.c_ushort)]

class TGOLFileParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("fileTime", SystemTime),
                ("fileLength", ctypes.c_int64),
                ("fileHeaderLength", ctypes.c_int64),
                ("fileTailLength", ctypes.c_int64),
                ("type", ctypes.c_char),
                ("strHeaderLength", ctypes.c_int),
                ("pad1", ctypes.c_char * 8),
                ("strSignalCount", ctypes.c_int),
                ("cadrWidth", ctypes.c_int),
                ("cadrHeight", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("pad2", ctypes.c_char * 4),
                ("pad3", ctypes.c_char * 49),
                ("dx", ctypes.c_float),
                ("dy", ctypes.c_float),
                ("pad4", ctypes.c_char * 3697),
                ("filename", ctypes.c_char * 256),
                ("pad5", ctypes.c_char * 9)]

class TRLIFileParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("fileTime", SystemTime),
                ("fileLength", ctypes.c_int64),
                ("fileHeaderLength", ctypes.c_int64),
                ("fileTailLength", ctypes.c_int64),
                ("type", ctypes.c_int8),
                ("strHeaderLength", ctypes.c_int),
                ("pad1", ctypes.c_char * 8),
                ("strSignalCount", ctypes.c_int),
                ("cadrWidth", ctypes.c_int),
                ("cadrHeight", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("frames", ctypes.c_int),
                ("processTime", SystemTime),
                ("processi", ctypes.c_int),
                ("processj", ctypes.c_int),
                ("u0", ctypes.c_float),
                ("u1", ctypes.c_float),
                ("v0", ctypes.c_int),
                ("v1", ctypes.c_int),
                ("pad2", ctypes.c_char * 8),
                ("rangeType", ctypes.c_char),
                ("dx", ctypes.c_float),
                ("dy", ctypes.c_float),
                ("flipType", ctypes.c_char),
                ("sx", ctypes.c_int),
                ("sy", ctypes.c_int),
                ("calibration_rli", ctypes.c_char),
                ("pad3", ctypes.c_char * 3687),
                ("fileName", ctypes.c_char * 256),
                ("pad4", ctypes.c_char * 9)]

class TSynthParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("processAlgorithm", ctypes.c_char),
                ("isHeaders1", ctypes.c_bool),
                ("isHeaders2", ctypes.c_bool),
                ("D0", ctypes.c_float),
                ("dD", ctypes.c_float),
                ("board", ctypes.c_char),
                ("reserved1", ctypes.c_char * 48),
                ("VH", ctypes.c_float),
                ("Lambda", ctypes.c_float),
                ("Fn", ctypes.c_float),
                ("reserved2", ctypes.c_char * 842),
                ("isProcessAlli", ctypes.c_bool),
                ("i1", ctypes.c_int),
                ("i2", ctypes.c_int),
                ("isProcessAllj", ctypes.c_bool),
                ("j1", ctypes.c_int),
                ("j2", ctypes.c_int),
                ("reserved3", ctypes.c_char * 9),
                ("type", ctypes.c_char),
                ("u0", ctypes.c_float),
                ("u1", ctypes.c_float),
                ("v0", ctypes.c_int),
                ("v1", ctypes.c_int),
                ("comments", ctypes.c_char * 512),
                ("reserved4", ctypes.c_char * 20),
                ("cadrWidth", ctypes.c_int),
                ("cadrHeight", ctypes.c_int),
                ("rangeType", ctypes.c_char),
                ("flipType", ctypes.c_char),
                ("polarization", ctypes.c_char),
                ("angle_zond", ctypes.c_float),
                ("reserved5", ctypes.c_char * 678),
                ("rgg_SY", ctypes.c_int),
                ("reserved51", ctypes.c_char * 205),
                ("rhgName", ctypes.c_char * 128),
                ("reserved6", ctypes.c_char * 1576)]

class Header(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("file_signature", ctypes.c_char * 4),
                ("file_version", ctypes.c_int),
                ("GOLFileParams", TGOLFileParams),
                ("RLIFileParams", TRLIFileParams),
                ("SynthParams", TSynthParams),
                ("aligningPointsCount", ctypes.c_uint32),
                ("rangeCompressionCoef", ctypes.c_float),
                ("azimuthCompressionCoef", ctypes.c_float),
                ("pad1", ctypes.c_char * 4076)]

class TRLIStrHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("isNavigation", ctypes.c_bool),
                ("time", SystemTime),
                ("LatSNS", ctypes.c_double),
                ("LongSNS", ctypes.c_double),
                ("Hsns", ctypes.c_double),
                ("latitude", ctypes.c_double),
                ("longtitude", ctypes.c_double),
                ("H", ctypes.c_double),
                ("V", ctypes.c_double),
                ("Ve", ctypes.c_double),
                ("Vn", ctypes.c_double),
                ("a", ctypes.c_double),
                ("g", ctypes.c_double),
                ("f", ctypes.c_double),
                ("w", ctypes.c_double),
                ("Vu", ctypes.c_double),
                ("WH", ctypes.c_double),
                ("reserved", ctypes.c_char * 119)]


class RLIFile():
    """Common operations with RLI file"""

    def __init__(self):
        self.header = None
        self.data = None

    def __init__(self, file):
        self.header = None
        self.data = None
        self.path = file

        with open(file, 'rb') as f:
            self.load(f)


    @property
    def height(self):
        """Image height in points"""
        return self.header.RLIFileParams.height

    @property
    def width(self):
        """Image width in points"""
        return self.header.RLIFileParams.width

    @property
    def point_size(self):
        """Point size in bytes"""

        if self.header.RLIFileParams.type == 2:
            return ctypes.sizeof(ctypes.c_float)
        elif self.header.RLIFileParams.type == 3:
            return ctypes.sizeof(ctypes.c_float * 2)
        else:
            raise ValueError

    @property
    def _point_type(self):
        """Point struct format"""

        if self.header.RLIFileParams.type == 2:
            return '<f'
        elif self.header.RLIFileParams.type == 3:
            return '<2f'
        else:
            raise ValueError


    def _get_max_value(self, file):
        file.seek(ctypes.sizeof(self.header), io.SEEK_SET)
        
        line_data_size = self.point_size * self.width
        max_val = 0

        while True:
            file.seek(ctypes.sizeof(TRLIStrHeader), io.SEEK_CUR)
            line = file.read(line_data_size)
            
            if not line:
                break
            
            line = itertools.chain(*struct.iter_unpack(self._point_type, line))
            
            if self.header.RLIFileParams.type == 3:
                line = amp_modulus(line)
            
            line_max = max(line)
            
            max_val = max_val if max_val > line_max else line_max

        return max_val

    def load(self, file: io.RawIOBase):

        print(f'Load: {self.path}')
        
        file.seek(0, io.SEEK_SET)
        self.header = Header.from_buffer_copy(file.read(ctypes.sizeof(Header)))
        self.data = []
        
        line_data_size = self.point_size * self.width

        for _ in range(self.height):
            file.seek(ctypes.sizeof(TRLIStrHeader), io.SEEK_CUR)
            line = struct.iter_unpack(self._point_type, file.read(line_data_size))
            line = list(itertools.chain.from_iterable(line))

            if len(line) != self.width:
                continue

            if self.header.RLIFileParams.type == 3:
                line = amp_modulus(line)

            self.data.append(line)
        
        self.data = np.array(self.data)

    def add(self, path):
        print(f'Add {path}')

        file2 = RLIFile(path)

        width = self.data.shape[0] if self.data.shape[0] < file2.data.shape[0] else file2.data.shape[0]
        height = self.data.shape[1] if self.data.shape[1] < file2.data.shape[1] else file2.data.shape[1]

        data1 = self.data.copy()
        data2 = file2.data.copy()
        data1.resize((width, height), refcheck=False)
        data2.resize((width, height), refcheck=False)


        self.data = np.add(data1, data2)

    def toimg(self,):
        print(f'Convert to img: {self.path}')

        img = img_as_float(self.data)

        p_start_val = 0.1
        p_end_val = 98.7
        p_start, p_end = np.percentile(img, (p_start_val, p_end_val))
        img = skimage.exposure.rescale_intensity(img, in_range=(p_start, p_end))

        return img



def read_header(path):
    with open(path, 'rb') as f:
        f.seek(0, io.SEEK_SET)
        return Header.from_buffer_copy(f.read(ctypes.sizeof(Header)))
        
def amp_modulus(data):
    return [math.sqrt(p[0] * p[0] + p[1] * p[1]) for p in data]