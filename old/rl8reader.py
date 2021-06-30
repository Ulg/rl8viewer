#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import colorsys
import ctypes
import math
import struct
import time

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from skimage import data, img_as_float
from skimage import exposure
from skimage import io


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

class Header(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("file_signature", ctypes.c_char * 4),
                ("file_version", ctypes.c_int),
                ("GOLFileParams", TGOLFileParams),
                ("RLIFileParams", TRLIFileParams),
                ("SynthParams", TSynthParams),
                ("aligningPointsCount", ctypes.c_uint32),
                ("rangeCompressionCoef", ctypes.c_float),
                ("azimuthCompressionCoef", ctypes.c_float)]

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


HEADER_SIZE = 16384


raw_data = []

class HistNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, clip=False):
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        pass


def amp_modulus(data):
    return [math.sqrt(p[0] * p[0] + p[1] * p[1]) for p in data]
    # amplitudeModulus[i / 2] = (float)Math.Sqrt(sampleData[i] * sampleData[i] +
    #                            sampleData[i + 1] * sampleData[i + 1]);

with open('test/dataset.rl8', 'rb') as fp:
    header = Header.from_buffer_copy(fp.read(HEADER_SIZE))

    if header.RLIFileParams.type == 2:
        point_fmt = '<f'
    elif header.RLIFileParams.type == 3:
        point_fmt = '<2f'
    else:
        raise Exception # Unknown point format

    chunk_header_size = ctypes.sizeof(TRLIStrHeader)
    chunk_size = chunk_header_size + header.RLIFileParams.width * struct.calcsize(point_fmt)
    for chunk in iter(lambda: fp.read(chunk_size), b''):
        points = struct.iter_unpack(point_fmt, chunk[chunk_header_size:])

        if header.RLIFileParams.type == 2:
            points = [p[0] for p in points]
        elif header.RLIFileParams.type == 3:
            points = amp_modulus(points)
        
        raw_data.append(points)
        
raw_data = np.array(raw_data)

#========== Do some magic... ==================================================#
image = np.array(raw_data)
image *= 1.0 / image.max()
reference = io.imread('test/dataset.bmp')

# Normalize image histogram
# start = time.perf_counter()
# bins_num = 1000
# img_hist, bins = np.histogram(image.flatten(), bins_num, density=True)
# cdf = img_hist.cumsum()
# image = np.interp(image, bins[:-1], cdf)
# end = time.perf_counter()
# print(end-start)

# img = exposure.equalize_hist(image)

def draw(axes, img, name):
    # cols = int(len(fig.axes) / 3) + 1

    # ax, ax_hist = axes
    # ax_cdf = ax_hist.twinx()
    
    # ax.set_title(name)
    # ax.imshow(img, cmap='gray')

    # # Display histogram
    # ax_hist.hist(img.ravel(), bins=256, histtype='step', color='black')
    # ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    # ax_hist.set_xlabel('Pixel intensity')
    # ax_hist.set_xlim(0, 1)
    # ax_hist.set_yticks([])

    # # Display cumulative distribution
    # img_cdf, bins = exposure.cumulative_distribution(img, 256)
    # ax_cdf.plot(bins, img_cdf, 'r')
    # ax_cdf.set_yticks([])

    # return ax, ax_hist, ax_cdf
    """Plot an image along with its histogram and cumulative histogram.

    """
    bins = 256
    image = img_as_float(img)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(image, cmap=plt.cm.gray)
    ax_img.set_axis_off()
    ax_img.set_title(name)

    # Display histogram
    ax_hist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf

# image = data.moon()
fig = plt.figure(figsize=(15, 6), tight_layout=True)

axes = np.zeros((2, 5), dtype=np.object)
axes[0, 0] = fig.add_subplot(2, 5, 1)
for i in range(1, 5):
    axes[0, i] = fig.add_subplot(2, 5, 1+i, sharex=axes[0,0], sharey=axes[0,0])
for i in range(0, 5):
    axes[1, i] = fig.add_subplot(2, 5, 6+i)

draw(axes[:, 0], reference, 'Reference (RLView.exe)')
draw(axes[:, 1], image, 'Original image')

img = exposure.equalize_hist(image)
draw(axes[:, 2], img, 'Histogram equalization')

p_start_val = 0.1
p_end_val = 98.7
p_start, p_end = np.percentile(image, (p_start_val, p_end_val))
img = exposure.rescale_intensity(image, in_range=(p_start, p_end))
draw(axes[:, 3], img, f'Contrast stretching (p{p_start_val} - p{p_end_val})')

clip = 0.015
img = exposure.equalize_adapthist(image, clip_limit=clip)
draw(axes[:, 4], img, f'Adaptive equalization (clip = {clip})')


fig = plt.figure(figsize=(6, 6), tight_layout=True)

axes = np.zeros((2, 2), dtype=np.object)
axes[0, 0] = fig.add_subplot(2, 2, 1)
for i in range(1, 2):
    axes[0, i] = fig.add_subplot(2, 2, 1+i, sharex=axes[0,0], sharey=axes[0,0])
for i in range(0, 2):
    axes[1, i] = fig.add_subplot(2, 2, 3+i)

draw(axes[:, 0], reference, 'Reference (RLView.exe)')

p_start_val = 0.0
p_end_val = 98.7
p_start, p_end = np.percentile(image, (p_start_val, p_end_val))
img = exposure.rescale_intensity(image, in_range=(p_start, p_end))
draw(axes[:, 1], img, f'Contrast stretching (p{p_start_val} - p{p_end_val})')

plt.show()
