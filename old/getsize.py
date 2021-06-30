#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import ctypes
from sys import argv


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
	            ("lambda", ctypes.c_float),
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

class FileHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("file_signature", ctypes.c_char * 4),
                ("file_version", ctypes.c_int),
                ("GOLFileParams", TGOLFileParams),
                ("RLIFileParams", TRLIFileParams),
                ("SynthParams", TSynthParams),
                ("aligningPointsCount", ctypes.c_uint32),
                ("rangeCompressionCoef", ctypes.c_float),
                ("azimuthCompressionCoef", ctypes.c_float)]


HEADER_SIZE = 16384


with open(argv[1], 'rb') as fp:
    header = FileHeader.from_buffer_copy(fp.read(HEADER_SIZE))

print(f'cadrWidth: {header.RLIFileParams.cadrWidth}')
print(f'cadrHeight: {header.RLIFileParams.cadrHeight}')
print(f'width: {header.RLIFileParams.width}')
print(f'height: {header.RLIFileParams.height}')
