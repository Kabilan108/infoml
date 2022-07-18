#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:51:28 2019

@author: yusuf
"""
import os
import numpy as np
import nibabel as nib
import argparse
from numpy import linalg as LA
from matplotlib.ticker import FuncFormatter


def y_fmt(y):
    import numpy as np
    decades = [1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6, 1e-9 ]
    suffix  = ["G", "M", "k", "" , "m" , "u", "n"  ]
    if y == 0:
        return str(0)
    for i, d in enumerate(decades):
        if np.abs(y) >=d:
            val = y/float(d)
            signf = len(str(val).split(".")[1])
            if signf == 0:
                return '{val:d} {suffix}'.format(val=int(val), suffix=suffix[i])
            else:
                if signf == 1:
                    #print(val,signf)
                    if str(val).split(".")[1] == "0":
                       return '{val:d} {suffix}'.format(val=int(round(val)), suffix=suffix[i]) 
                tx = "{"+"val:.{signf}f".format(signf = signf) +"} {suffix}"
                return tx.format(val=val, suffix=suffix[i])
    return y

def calculateZScore(data,controlGroupOrder):
    import numpy as np
    
    newData=np.zeros(data.shape)
    for i in range(len(data)):
        if(i<len(controlGroupOrder)):
            controls=np.delete(controlGroupOrder,np.where(controlGroupOrder==i))
        meanControl = np.mean(data[controls])
        stdControl = np.std(data[controls])
        if(stdControl>0.000001):
            newData[i] = (data[i]-meanControl)/stdControl
        else:
            newData[i] = (data[i]-meanControl)            
    return newData

def drawBoxPlot(data,dataLabels,title,outputPath,xLabel="",yLabel="matching accuracy (%)",color='darkorchid',rotation=0,plotScatter=True,yLim=[],threshold=0,nameOutliers=False,subjectIDs=[]): 
    import matplotlib.pylab as plt
    import numpy as np
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    ax.set_xlabel(xLabel,fontsize=12)
    ax.set_ylabel(yLabel,fontsize=12)
    ax.tick_params(axis='y',labelsize=6)
    ax.tick_params(axis='x',labelsize=6)
    if(len(yLim)==2):#use this line to set the y limits of the plot, useful for opening up space above the bars to put stars at postprocessing
        plt.ylim(yLim[0],yLim[1])
    #plt.yticks(range(size), size=7)

    boxprops = dict(linestyle='-', linewidth=4)
    if(plotScatter==False):
        markersize=4
    else:
        markersize=0
    flierprops = dict(marker='.', markerfacecolor='grey', markeredgecolor='none',markersize=markersize,linestyle='none') #outliers
    medianprops = dict(linestyle='-', linewidth=0, color='firebrick') #median line
    meanpointprops = dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick')#to put apoint to the mean instead of a line
    meanlineprops = dict(linestyle='-', linewidth=0.5, color='firebrick') # mean line
    whiskerprops=dict(linestyle='--',linewidth=0.5,color='grey') # lines extending the boxes
    capprops=dict(linestyle='-',linewidth=0.5,color='grey') # caps perpendicular to whiskers
    boxplot_parts = ax.boxplot(data,whiskerprops=whiskerprops,boxprops=boxprops,capprops=capprops,medianprops=medianprops,meanprops=meanlineprops,meanline=True,showmeans=True,notch=False,flierprops=flierprops,patch_artist=True,zorder=0)
    for i in range(len(boxplot_parts['boxes'])):
        boxplot_parts['boxes'][i].set_edgecolor(color)
        boxplot_parts['boxes'][i].set_facecolor('none')
        boxplot_parts['boxes'][i].set_linewidth(0.5)
    
    if(threshold!=0):
        ax.axhline(y=threshold,linewidth=0.5, color='r',zorder=1)
        ax.axhline(y=-threshold,linewidth=0.5, color='r',zorder=1)
    
    if(plotScatter==True):
        xScattered = []
        for i,dataChunk in enumerate(data):
            xScattered.append(np.random.normal(i+1,0.02,len(dataChunk)))
        for i in range(len(data)):
            plt.scatter(xScattered[i],data[i],color=color,alpha=0.5,s=4,edgecolors='dimgray',linewidth=0.3,zorder=1)
    
    if(nameOutliers==True and len(subjectIDs)>0):
        for i in range(len(data)):
            for j in range(len(data[i])):
                if(data[i][j]>=threshold or data[i][j]<=-threshold):
                    if(plotScatter==True):
                        ax.annotate(subjectIDs[j],(xScattered[i][j]+0.03,data[i][j]),size=3,alpha=0.5) ### -0.05 and +0.5 are for offsetting the annotation in x,y directions
                    else:
                        ax.annotate(subjectIDs[j],(range(len(dataLabels)+1)[1:][i],data[i][j]),size=3,alpha=0.5) ### -0.05 and +0.5 are for offsetting the annotation in x,y directions
    
    plt.xticks(range(len(dataLabels)+1)[1:], dataLabels, rotation=rotation)
    plt.title(title)
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')

def drawBoxPlot_subplots(data,xLabels,yLabels,title,outputPath,color='darkorchid',plotScatter=True,yLim=[],threshold=0,nameOutliers=False,subjectIDs=[]): 
    import matplotlib.pylab as plt
    import numpy as np
    
    if(plotScatter==False):
        markersize=4
    else:
        markersize=0
    flierprops = dict(marker='.', markerfacecolor='grey', markeredgecolor='none',markersize=markersize,linestyle='none') #outliers
    medianprops = dict(linestyle='-', linewidth=0, color='firebrick') #median line
    meanpointprops = dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick')#to put apoint to the mean instead of a line
    meanlineprops = dict(linestyle='-', linewidth=0.5, color='firebrick') # mean line
    whiskerprops=dict(linestyle='--',linewidth=0.5,color='grey') # lines extending the boxes
    capprops=dict(linestyle='-',linewidth=0.5,color='grey') # caps perpendicular to whiskers
    boxprops = dict(linestyle='-', linewidth=4)
    
    numPlots=len(data)
    
    fig,axs=plt.subplots(1,numPlots)
    fig.tight_layout(pad=3.0)
    
    for ax_id in range(len(axs)):
        data_ptr=data[ax_id]
        
        axs[ax_id].set_xlabel(xLabels[ax_id],fontsize=6)
        axs[ax_id].set_ylabel(yLabels[ax_id],fontsize=6)
        axs[ax_id].tick_params(axis='y',labelsize=6)
        axs[ax_id].tick_params(axis='x',which='both',labelsize=0,width=0)
        axs[ax_id].yaxis.set_major_formatter(FuncFormatter(y_fmt))
        if(len(yLim)==2):#use this line to set the y limits of the plot, useful for opening up space above the bars to put stars at postprocessing
            plt.ylim(yLim[0],yLim[1])
        #plt.yticks(range(size), size=7)
    
        
        boxplot_parts = axs[ax_id].boxplot(data_ptr,whiskerprops=whiskerprops,boxprops=boxprops,capprops=capprops,medianprops=medianprops,meanprops=meanlineprops,meanline=True,showmeans=True,notch=False,flierprops=flierprops,patch_artist=True,zorder=0,widths=(0.5))
        boxplot_parts['boxes'][0].set_edgecolor('grey')
        boxplot_parts['boxes'][0].set_facecolor('none')
        boxplot_parts['boxes'][0].set_linewidth(0.5)

        if(plotScatter==True):
            xScattered = np.random.normal(1,0.02,len(data_ptr))
            axs[ax_id].scatter(xScattered,data_ptr,color=color,alpha=0.5,s=4,edgecolors='dimgray',linewidth=0.3,zorder=1)
        
        if(threshold!=0):
            std=np.std(data_ptr)
            mean=np.mean(data_ptr)
            axs[ax_id].axhline(y=mean+threshold*std,linewidth=0.5, color='r',zorder=1)
            axs[ax_id].axhline(y=mean-threshold*std,linewidth=0.5, color='r',zorder=1)
        
            if(nameOutliers==True and len(subjectIDs)>0):
                for j in range(len(data_ptr)):
                    if(data_ptr[j]>=mean+threshold*std or data_ptr[j]<=mean-threshold*std):
                        if(plotScatter==True):
                            axs[ax_id].annotate(subjectIDs[j],(xScattered[j]+0.03,data_ptr[j]),size=4,alpha=0.5) ### -0.05 and +0.5 are for offsetting the annotation in x,y directions
                        else:
                            axs[ax_id].annotate(subjectIDs[j],(1,data_ptr[j]),size=4,alpha=0.5) ### -0.05 and +0.5 are for offsetting the annotation in x,y directions
        
    #plt.xticks(range(len(dataLabels)+1)[1:], dataLabels, rotation=rotation)
    fig.suptitle(title)
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')

### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_strength_intraHemisphere(connectome,hemisphereMaps):
    numNodes = len(connectome)
    strength = 0
    for i in range(numNodes):
        strength[i] = np.sum(connectome[i][hemisphereMaps==hemisphereMaps[i]])
    return strength
    
### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_strength_interHemisphere(connectome,hemisphereMaps):
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    for i in range(numNodes):
        strength[i] = np.sum(connectome[i][hemisphereMaps!=hemisphereMaps[i]])
    return strength

# python qaConnectivity.py -i /home/yusuf/data/TBI/connectomes/Schaefer118/raw/ -nn 118 -hm /home/yusuf/data/atlases/Schaefer/hemisphereMaps/Schaefer118.txt --plotPath /home/yusuf/data/TBI/connectomes/QA/Schaefer118/connectivity/Schaefer118_connectivity.png --reportFile /home/yusuf/data/TBI/connectomes/QA/Schaefer118/connectivity/Schaefer118_connectivity.txt --standardDeviation 4
parser = argparse.ArgumentParser(description='calculate correlation between the age and matching accuracies of the subjects')
parser.add_argument('-i','--inputFolder', help='paths of the folder of images to be merged', required=True, type=str)
parser.add_argument('-s','--subjectsList', help='path to the file that contains path to the connectomes', required=False,default="")
parser.add_argument('--fileNameTrailer', help='trailing text that follows subjectID in the file name', required=False, default=".txt")
parser.add_argument('-nn','--numNodes', help='number of ROIs in the atlas. Use this flag if the region IDs are sequential', required=True, type=int)
parser.add_argument('-hm','--hemisphereMaps', help='file path that contains the hemispehere information for the nodes', required=False,default="")
parser.add_argument('-r','--reportFile', help='file path to write the statistics in text', required=True)
parser.add_argument('-p','--plotPath', help='folder/file path to save the box plot of connectivity statistics', required=False,default="")
parser.add_argument('-std','--standardDeviation', help='label subjects as problematic for being this many standard deviations away from the healthy controls', required=False, type=int, default=2.33)
parser.add_argument('--dropLastNode', help='drop last node of the connectome (brainStem) from strength calculations across hemispheres', required=False,default=False, action='store_true')
parser.add_argument('--modality', help='structural or functional connectome?', required=False,choices=['structure','function'],default='structure')
parser.add_argument('--zeroDiagonals', help='set diagonal entries to zero', required=False,action='store_true',default=False)
parser.add_argument('-t','--title', help='title for plot', required=False, type=str, default='') #You can escape white space in the title from command line with "\ " as in <two\ words>


args = vars(parser.parse_args())
inputFolderPath=args['inputFolder']
subjectListPath=args['subjectsList']
fileNameTrailer=args['fileNameTrailer']
numNodes=args['numNodes']
hemisphereMapsPath=args['hemisphereMaps']
reportFilePath=args['reportFile']
plotFilePath=args['plotPath']
standardDeviation=np.abs(args['standardDeviation'])
dropLastNode=args['dropLastNode']
modality=args['modality']
zeroDiagonals=args['zeroDiagonals']
title=args['title']

### get list of connectome paths
if(subjectListPath!=""):
    subjectList = [x+fileNameTrailer for x in open(subjectListPath,"r").read().splitlines()]
else:
    subjectList = sorted(os.listdir(inputFolderPath))


### obtain subject names from the file names
### NOTE: this line is very much specific to the dataset. Below, I'm assuming that the filenames contain subject names at the beggining in the form of c001_s1_blah_blah where c001_s1 is the subjectID
subjectNames=[("_".join(x.split("/")[-1].split("_")[:2])).split(".")[0] for x in subjectList]


###load connectomes
####check if all connectomes have same number of nodes, if not, drop that connectome
connectomes=[]
discardedSubjectNodeCount=[]
discardedSubjectNames=[]
for i in range(len(subjectList)):
    tempConn=np.loadtxt(inputFolderPath+subjectList[i],dtype=float)
    
    if(zeroDiagonals==True):
        np.fill_diagonal(tempConn,0)
    
    if(len(tempConn)!=numNodes):
        discardedSubjectNames.append(subjectNames[i])
        discardedSubjectNodeCount.append(len(tempConn))
    else:
        connectomes.append(tempConn.copy())


numSubjects=len(connectomes)
subjectsOrder=np.arange(numSubjects)

### lists to keep statistics and their names
statisticsData=[]
statisticsNames=[]

#########calculate conenctivitystrength
###load hemisphere for nodes, if the parameter is provided when running the script
if(hemisphereMapsPath!=""):
    hemisphereMaps = np.array(np.loadtxt(hemisphereMapsPath),dtype=bool)
else:
    hemisphereMaps=np.ones(numNodes,dtype=bool)
    hemisphereMaps[0:int(numNodes/2)]=False


if(dropLastNode==True):
    hemisphereMaps[-1]=0
    invertedHemisphereMaps=np.invert(hemisphereMaps)
    invertedHemisphereMaps[-1]=0
else:
    invertedHemisphereMaps=np.invert(hemisphereMaps)
    
        
strengths=np.zeros(numSubjects)
for i in range(len(connectomes)):
    strengths[i]=np.sum(connectomes[i]*(connectomes[i]>0))/2.0 + np.trace(connectomes[i]*(connectomes[i]>0))/2.0
statisticsData.append(strengths)
statisticsNames.append("total\nconnectivity")

if(zeroDiagonals==False):
    strengths_offDiag=np.zeros(numSubjects)
    strengths_diag=np.zeros(numSubjects)
    for i in range(len(connectomes)):
        tempConn=np.copy(connectomes[i])
        strengths_diag[i]=np.trace(tempConn)
        np.fill_diagonal(tempConn,0)
        strengths_offDiag[i]=np.sum(tempConn*(tempConn>0))/2.0
    statisticsData.append(strengths_offDiag)
    statisticsNames.append("total off diagonal\nconnectivity")
    statisticsData.append(strengths_diag)
    statisticsNames.append("self\nedges")


strengths_intra=np.zeros(numSubjects)
for i in range(len(connectomes)):
    strengths_intra[i]=(np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(hemisphereMaps,hemisphereMaps))+np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(invertedHemisphereMaps,invertedHemisphereMaps)))/2.0
statisticsData.append(strengths_intra)
statisticsNames.append("intrahemispheric\nconnectivity")

strengths_inter=np.zeros(numSubjects)
for i in range(len(connectomes)):
    strengths_inter[i]=(np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(hemisphereMaps,invertedHemisphereMaps))+np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(invertedHemisphereMaps,hemisphereMaps)))/2.0
statisticsData.append(strengths_inter)
statisticsNames.append("interhemispheric\nconnectivity")


if(modality=="function"):
    strengths_neg=np.zeros(numSubjects)
    for i in range(len(connectomes)):
        strengths_neg[i]=np.sum(connectomes[i]*(connectomes[i]>0))/2.0
    statisticsData.append(strengths_neg)
    statisticsNames.append("total conn.(-)")

    strengths_intra_neg=np.zeros(numSubjects)
    for i in range(len(connectomes)):
        strengths_intra_neg[i]=(np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(hemisphereMaps,hemisphereMaps))+np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(invertedHemisphereMaps,invertedHemisphereMaps)))/2.0
    statisticsData.append(strengths_intra_neg)
    statisticsNames.append("intrahemispheric conn.(-)")
    
    strengths_inter_neg=np.zeros(numSubjects)
    for i in range(len(connectomes)):
        strengths_inter_neg[i]=(np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(hemisphereMaps,invertedHemisphereMaps))+np.sum(connectomes[i]*(connectomes[i]>0)*np.outer(invertedHemisphereMaps,hemisphereMaps)))/2.0
    statisticsData.append(strengths_inter_neg)
    statisticsNames.append("interhemispheric conn.(-)")


########calculate density
density=np.zeros(numSubjects)
for i in range(len(connectomes)):
    density[i]=np.sum(connectomes[i]>0)*100.0/float(numNodes*(numNodes-1))
statisticsData.append(density)
statisticsNames.append("density")

if(modality=="function"):
    density_neg=np.zeros(numSubjects)
    for i in range(len(connectomes)):
        density_neg[i]=np.sum(connectomes[i]<0)*100.0/float(numNodes*(numNodes-1))
    statisticsData.append(density_neg)
    statisticsNames.append("density neg.")
    
    
    
#####calculate z scores, if indicated by command line argument
# Need to do statistics[:,0] for k (subjects) x n(num of stats) statistics
statisticsData_z=[calculateZScore(x,subjectsOrder) for x in statisticsData]


### draw box plot, where a threshold will be drawn for the std deviation above and below zero, as well as outliers' names will be printed
### use the following line to plot z-scores of the measures
#drawBoxPlot(statisticsData_z,dataLabels=statisticsNames,title=title,outputPath=plotFilePath,xLabel="Statistic Type",yLabel="Connectivity Score (z score)", color='darkorchid',rotation=0,plotScatter=True,threshold=standardDeviation,nameOutliers=True,subjectIDs=subjectNames)
### use the following lines to plot actual measures (without z-scores) with +-2 standard deviation being marked with red lines
#plotFilePath2=plotFilePath.split(".")[0]+"_subplot.png"
yLabels=["# streamline","# streamline","# streamline","# streamline","# streamline","percent"]
drawBoxPlot_subplots(statisticsData,xLabels=statisticsNames,yLabels=yLabels,title=title,outputPath=plotFilePath,color='darkorchid',plotScatter=True,threshold=standardDeviation,nameOutliers=True,subjectIDs=subjectNames)

    
### get a list of the subjects that has very large/small ROIs relative to healthy control population
problemSubjects_names_small=[]
problemSubjects_scores_small=[]
problemSubjects_std_small=[]
for i in range(len(statisticsData)):
    problemSubjects_names_small.append([subName for subName,truth in zip(subjectNames,statisticsData_z[i]<=-standardDeviation) if truth])
    problemSubjects_scores_small.append([score for score,truth in zip(statisticsData[i],statisticsData_z[i]<=-standardDeviation) if truth])
    problemSubjects_std_small.append([score for score,truth in zip(statisticsData_z[i],statisticsData_z[i]<=-standardDeviation) if truth])
    
problemSubjects_names_large=[]
problemSubjects_scores_large=[]
problemSubjects_std_large=[]
for i in range(len(statisticsData)):
    problemSubjects_names_large.append([subName for subName,truth in zip(subjectNames,statisticsData_z[i]>standardDeviation) if truth])
    problemSubjects_scores_large.append([score for score,truth in zip(statisticsData[i],statisticsData_z[i]>standardDeviation) if truth])
    problemSubjects_std_large.append([score for score,truth in zip(statisticsData_z[i],statisticsData_z[i]>standardDeviation) if truth])

### save list of subjects with outlier ROIs
reportFile=open(reportFilePath,'w')
reportFile.write("============== discarded subjects due to missing node ==============\n" )
for i in range(len(discardedSubjectNames)):
    reportFile.write("%s : %d\n" %(discardedSubjectNames[i],discardedSubjectNodeCount[i]))

reportFile.write("\n============== outlier statistics that are larger by %0.2f standard deviation ==============\n" %standardDeviation)
for i in range(len(statisticsNames)):
    reportFile.write("%s == > " % statisticsNames[i])
    for j in range(len(problemSubjects_names_large[i])):
        reportFile.write("(%s:%0.2f -- %0.2f)\t" % (problemSubjects_names_large[i][j], problemSubjects_scores_large[i][j],problemSubjects_std_large[i][j]) )
    reportFile.write("\n")
reportFile.write("\n============== outlier statistics that are smaller than by %0.2f standard deviation ==============\n" %standardDeviation)
for i in range(len(statisticsNames)):
    reportFile.write("%s == > " % statisticsNames[i])
    for j in range(len(problemSubjects_names_small[i])):
        reportFile.write("(%s:%0.2f -- %0.2f)\t" % (problemSubjects_names_small[i][j], problemSubjects_scores_small[i][j],problemSubjects_std_small[i][j]) )
    reportFile.write("\n")    
reportFile.close()
