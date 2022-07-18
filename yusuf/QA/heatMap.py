# -*- coding: utf-8 -*-
"""
Given a matrix containing numerical values,
this program plots the heatmap of the matrix into a png file.

sample: python heatMap.py -i ./actualMatchingMatrixFull.txt -o ./heatmap.png --threshold 5 --color w --display
"""
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
import argparse

##### get command line parameters
parser = argparse.ArgumentParser(description='Plot heat map of given matrix')
parser.add_argument('-i','--inputPath', help='source path to the matrix to be plotted', required=True,type=str)
parser.add_argument('-o','--outputPath', help='destination path to save the png file', required=False,type=str)
parser.add_argument('-t','--threshold', help='min threshold for the magnitude of the cell values (i.e., a threshold of absolute values)', required=False, type=float, default=0)
parser.add_argument('-s','--sign', help='plot the whole matrix, or positive/negative side?', required=False,choices=['full','positive','negative'],default='full')
parser.add_argument('-bc','--bcolor', help='background color', required=False, default='k', type=str)
parser.add_argument('-ext','--extension', help='plot extension', required=False, default='png', type=str)
# parser.add_argument('--permutation', help='Reoreder the matrix', required=False, type=str)
parser.add_argument('--interpolation', help='interpolation', required=False, default='none', type=str, choices=['none','nearest'])
parser.add_argument('--colorMap', help='color map', required=False, default='jet', type=str)
parser.add_argument('--display', help='display plot', required=False,action='store_true')
parser.add_argument('--logScale', help='log scale connectivity', required=False,action='store_true')
parser.add_argument('--nonZeroDiagonals', help='don\'t zero out the diagonal entries', required=False,action='store_true')
parser.add_argument('--minRange', help='min range of the plot', required=False, type=float)
parser.add_argument('--maxRange', help='max range of the plot', required=False, type=float)
parser.add_argument('--symmetricRangeAroundZero', help='if the data contains values above and below zero, set the middle point of the range to zero while displaying', required=False,action='store_true')

parsed=parser.parse_args()
args = vars(parsed)
inputPath=args['inputPath']
sign=args['sign']
threshold=args['threshold']
backgroundColor=args['bcolor']
extension=args['extension']
interpolation=args['interpolation']
colorMap=args['colorMap']
displayPlotFlag=args['display']
logScale=args['logScale']
nonZeroDiagonals=args['nonZeroDiagonals']
symmetricRangeAroundZero=args['symmetricRangeAroundZero']

#if output path is not provided, then save the output image under the same folder 
#with input image by only changing the file extension
if parsed.outputPath:
    outputPath = args['outputPath'] 
else:
	outputPath = inputPath.rsplit(".",1)[0] + "." + extension

#print("read from " + inputPath)
matrix = np.loadtxt(inputPath)

# make sure that the diagonal is set to zero
if(nonZeroDiagonals==False):
    np.fill_diagonal(matrix,0)
    
# if log scale flag is set, log scale edges: but make sure, you are scaling the values grater than 1, and setting the values less than 1 to zero.
if(logScale==True):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if(matrix[i,j]>=1):
                matrix[i,j]=np.log(matrix[i,j])
            else:
                matrix[i,j]=0
            

if parser.parse_args().permutation:
    mapping = np.loadtxt(args['permutation'],dtype=int)
    permutation = np.array(mapping[:,1]-1)
    matrix = matrix[:,permutation][permutation,:]

# remove small values wrt zero (i.e., small in magnitude, both in positive and negative)
matrix[np.absolute(matrix)<threshold]=0
if(sign=='positive'):
    matrix[matrix<0]=0
if(sign=='negative'):
    matrix[matrix>0]=0
    matrix*=-1

#set the color map
cmap_=mpl.cm.get_cmap(colorMap)
cmap_.set_under(backgroundColor)

# plot the heatmap
if (symmetricRangeAroundZero==True):
    maxNum = np.max(np.abs(matrix))
    plt.imshow(matrix, interpolation=interpolation,vmin=-maxNum,vmax=maxNum,cmap=cmap_)
elif (not parsed.minRange and not parsed.maxRange):
    plt.imshow(matrix, interpolation=interpolation,cmap=cmap_)
elif (parsed.minRange and not parsed.maxRange):
    plt.imshow(matrix, interpolation=interpolation,vmin=args['minRange'],cmap=cmap_)
elif (not parsed.minRange and parsed.maxRange):
    plt.imshow(matrix, interpolation=interpolation,vmax=args['maxRange'],cmap=cmap_)
elif (parsed.minRange and parsed.maxRange):
    plt.imshow(matrix, interpolation=interpolation,vmin=args['minRange'],vmax=args['maxRange'],cmap=cmap_)


cbar=plt.colorbar(spacing='proportional',orientation='vertical', shrink=1.0, format="%.2f")
cbar.ax.tick_params(labelsize=10)

print("save to " + outputPath)
plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')

#display the plot
if displayPlotFlag:
    plt.show()


plt.close()
