#!/usr/bin/env python3

from PIL import Image, ImageStat
from functools import reduce

def detect_color_image(file, thumb_size=100, MSE_cutoff=50, MSE_bw_cutoff=30, adjust_color_bias=True):
    pil_img = Image.open(file)
    bands = pil_img.getbands()
    if bands == ('R','G','B') or bands== ('R','G','B','A'):
        thumb = pil_img.resize((thumb_size,thumb_size))
        thumbhsv = thumb.convert("HSV")
        SSE_gs  = 0
        SSE_gs2  = 0
        SSE_bw  = 0 
        bias = [0,0,0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias)/3 for b in bias ]
        for pixel in thumb.getdata():
            mu = sum(pixel)/3
            SSE_gs += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
        for pixelhsv in thumbhsv.getdata():
            SSE_bw += min(255-pixelhsv[2], pixelhsv[2])
        MSE_gs = float(SSE_gs)/(thumb_size*thumb_size)
        MSE_bw = float(SSE_bw)/(thumb_size*thumb_size)
        if MSE_gs <= MSE_cutoff:
            if MSE_bw <= MSE_bw_cutoff:
                print("is in fact blackandwhite")
            else:
                print("is in fact grayscale")
        else:
            print("is indeed color")
        print("( MSE=",MSE_gs,", MSE_bw=",MSE_bw," )")
    elif pil_img.mode == "L":
        SSE_bw  = 0
        thumb = pil_img.resize((thumb_size,thumb_size))
        for pixel in thumb.getdata():
            SSE_bw += min(255-pixel, pixel)
        MSE_bw = float(SSE_bw)/(thumb_size*thumb_size)
        if MSE_bw <= MSE_bw_cutoff:
            print("is in fact blackandwhite")
        else:
            print("is indeed grayscale")
    elif pil_img.mode == "1":
        print("black and white")
    else:
        print("cannot recognize the image", bands)

files = ["bwencodedasgrayscale.tif"]
for file in files:
    print(file)
    detect_color_image("images/"+file)
