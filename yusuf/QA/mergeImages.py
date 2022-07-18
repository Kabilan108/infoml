#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 15:20:42 2018

@author: yusuf
"""

import sys
import numpy as np
import argparse
from PIL import Image,ImageFont,ImageDraw
import math

## sample: python ~/repo/code/python/mergeImages.py -o merged.png -n 3 -i connectomes/C1map.png ICOV/C1ICOVMap.png PartialCorrelation/C1Correlationmap.png
parser = argparse.ArgumentParser(description='merges a number of given images into a single image file')
parser.add_argument('-o','--outputPath', help='path of the output image file', required=True)
parser.add_argument('-n','--numInputs', help='number of input images to be merged horizontally', required=True,type=int)
parser.add_argument('-g','--grid', help='number of rows and columns for putting images in a grid like structure', required=False,type=int,nargs=2)
parser.add_argument('-s','--size', help='size for the output image, if you would like to force the end image to have a certain size', required=False,nargs=2, type=int)
parser.add_argument('-if','--inputFolder', help='paths of the folder that contains the images to be merged (should have / at the end of the path)', required=False,type=str,default="")
parser.add_argument('-i','--inputPaths', help='paths of the files to be merged', required=True,nargs='*', type=str)
parser.add_argument('-t','--titles', help='titles for each image', required=False,nargs='*', type=str)
parser.add_argument('--noTitle', help='display plot', required=False,action='store_true')

args = vars(parser.parse_args())
outputPath=args['outputPath']
numInputs=args['numInputs']
noTitle=args['noTitle']
inputFolder=args['inputFolder']
inputPaths=[]
for i in range(numInputs):
    inputPaths.append(inputFolder+args['inputPaths'][i])

titles=[]    
if(parser.parse_args().titles):
    for i in range(numInputs):
        titles.append(args['titles'][i])
else:
    for i in range(numInputs):
        titles.append(inputPaths[i].split("/")[-1].split(".")[0])


if(parser.parse_args().grid):
    numRows=args['grid'][0]
    numCols=args['grid'][1]
    if(numRows*numCols<numInputs):
        print("incorrect grid layout entered. Please check again! Exiting!...")
        exit(1)
    
else:
    numRows=1
    numCols=numInputs

images=[]
widths=np.zeros(numInputs,dtype=int)
heights=np.zeros(numInputs,dtype=int)
for i in range(numInputs):
    images.append(Image.open(inputPaths[i]))
    widths[i], heights[i] = images[i].size 

#images = map(Image.open, inputPaths)
#widths, heights = zip(*(i.size for i in images))
if(noTitle==False):
    extraHeight=int(max(heights)*0.05) ### expand each image upwards to add title by 5%
else:
    extraHeight=0

if(numRows==1):
    width = sum(widths)
    height = max(heights)+extraHeight
else:
    width_rows=[]
    height_rows=[]
    for i in range(numRows):
        widthTemp=sum(widths[i*numCols:(i+1)*numCols])
        heightTemp=max(heights[i*numCols:(i+1)*numCols])+extraHeight
        width_rows.append(widthTemp)
        height_rows.append(heightTemp)
    width = max(width_rows)
    height = sum(height_rows)
    
new_im = Image.new('RGB', (width, height),(255, 255, 255))
draw = ImageDraw.Draw(new_im)

fontSize=int(max(heights)*0.03) ### set the font size of the title to be 3% of the height of the image
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", fontSize)

y_offset=extraHeight
for i in range(numInputs):
    row=int(math.floor(float(i)/float(numCols)))
    col=i%numCols
    if(col==0):
        x_offset = 0
    if(row>0 and col==0):
        y_offset += height_rows[row-1]
    new_im.paste(images[i], (x_offset,y_offset))
    textOffset=(images[i].size[0]-len(titles[i])*(fontSize/4.0))/2.0 # set the title to the middle of the subfigure
    if(noTitle==False):
        draw.text((x_offset+textOffset, y_offset-extraHeight),titles[i],(0,0,0),font=font)
    x_offset += images[i].size[0]

if(parser.parse_args().size):
    sizeX=args['size'][0]
    sizeY=args['size'][1]
    new_im.resize((sizeX,sizeY),Image.ANTIALIAS)

new_im.save(outputPath)
