#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jul 02 17:10:09 2020

@author: yusuf

"""

import argparse
import os
import numpy as np
import bct
from glob import glob


############### calculate nodal measures for degree and strength ################################
######## total
def calculate_strength_total(connectome_,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            mask=connectome[i]>0
            strength[i] = np.sum(connectome[i][mask])
    elif(sign=="negative"):
        for i in range(numNodes):
            mask=connectome[i]<0
            strength[i] = np.sum(connectome[i][mask])
    return strength

def calculate_degree_total(connectome_,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    degree = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i]>0)
    elif(sign=="negative"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i]<0)
    return degree

########hemispheric
### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_strength_intraHemisphere(connectome_,hemisphereMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            mask=connectome[i][hemisphereMaps==hemisphereMaps[i]]>0
            strength[i] = np.sum(connectome[i][hemisphereMaps==hemisphereMaps[i]][mask])
    elif(sign=="negative"):
        for i in range(numNodes):
            mask=connectome[i][hemisphereMaps==hemisphereMaps[i]]<0
            strength[i] = np.sum(connectome[i][hemisphereMaps==hemisphereMaps[i]][mask])
    return strength
    
### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_strength_interHemisphere(connectome_,hemisphereMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            mask=connectome[i][hemisphereMaps!=hemisphereMaps[i]]>0
            strength[i] = np.sum(connectome[i][hemisphereMaps!=hemisphereMaps[i]][mask])
    elif(sign=="negative"):
        for i in range(numNodes):
            mask=connectome[i][hemisphereMaps!=hemisphereMaps[i]]<0
            strength[i] = np.sum(connectome[i][hemisphereMaps!=hemisphereMaps[i]][mask])
    return strength 


### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_degree_intraHemisphere(connectome_,hemisphereMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    degree = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][hemisphereMaps==hemisphereMaps[i]]>0)
    elif(sign=="negative"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][hemisphereMaps==hemisphereMaps[i]]<0)
    return degree

### @hemisphereMaps: has 0 for indicating left hemisphere, 1 for right hemisphere
def calculate_degree_interHemisphere(connectome_,hemisphereMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    degree = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][hemisphereMaps!=hemisphereMaps[i]]>0)
    elif(sign=="negative"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][hemisphereMaps!=hemisphereMaps[i]]<0)
    return degree

########Modular
### @systemMaps: has system maps per node
def calculate_strength_withinModule(connectome_,systemMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            mask=connectome[i][systemMaps==systemMaps[i]]>0
            strength[i] = np.sum(connectome[i][systemMaps==systemMaps[i]][mask])
    elif(sign=="negative"):
        for i in range(numNodes):
            mask=connectome[i][systemMaps==systemMaps[i]]<0
            strength[i] = np.sum(connectome[i][systemMaps==systemMaps[i]][mask])
    return strength

### @systemMaps: has system maps per node
def calculate_strength_betweenModule(connectome_,systemMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    strength = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            mask=connectome[i][systemMaps!=systemMaps[i]]>0
            strength[i] = np.sum(connectome[i][systemMaps!=systemMaps[i]][mask])
    elif(sign=="negative"):
        for i in range(numNodes):
            mask=connectome[i][systemMaps!=systemMaps[i]]<0
            strength[i] = np.sum(connectome[i][systemMaps!=systemMaps[i]][mask])
    return strength

### @systemMaps: has system maps per node
def calculate_degree_withinModule(connectome_,systemMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    degree = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][systemMaps==systemMaps[i]]>0)
    elif(sign=="negative"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][systemMaps==systemMaps[i]]<0)
    return degree

### @systemMaps: has system maps per node
def calculate_degree_betweenModule(connectome_,systemMaps,sign="positive"):
    connectome=np.copy(connectome_)
    np.fill_diagonal(connectome,0)
    numNodes = len(connectome)
    degree = np.zeros(numNodes)
    if(sign=="positive"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][systemMaps!=systemMaps[i]]>0)
    elif(sign=="negative"):
        for i in range(numNodes):
            degree[i] = np.sum(connectome[i][systemMaps!=systemMaps[i]]<0)
    return degree

## -conn /home/yusuf/repo/projects/sexDifference_graphMeasures/results/data/dti_det/Schaefer114/ -s /home/yusuf/repo/projects/sexDifference_graphMeasures/results/data/src/list_schaefer114_strFunc.txt -sm /home/yusuf/data/atlases/yeoSubnetworks/Yeo_7system_in_Schaefer114_functionalOrder.txt -hm /home/yusuf/repo/projects/sexDifference_graphMeasures/results/data/src/hemispehereMaps_Schaefer114.txt  -out  /home/yusuf/repo/projects/sexDifference_graphMeasures/results/b_graphMetrics/
## -conn /home/yusuf/repo/projects/streamlineLoss/data/connectomes/custom_1mm/raw/ -sid all -sm /home/yusuf/data/atlases/birkanSubnetworks/Birkan_11System_in_Desikan86.txt -hm /home/yusuf/data/atlases/Desikan86/hemisphereMaps_Desikan86.txt -out /home/yusuf/repo/projects/streamlineLoss/01_scalars/ --numNodes 86
## -ml /home/yusuf/repo/projects/streamlineLoss/01_scalars/featureList.txt -conn /home/yusuf/repo/projects/streamlineLoss/data/connectomes/custom_1mm/raw/ -sid 100002_t0 -sm /home/yusuf/data/atlases/birkanSubnetworks/Birkan_11System_in_Desikan86.txt -hm /home/yusuf/data/atlases/Desikan86/hemisphereMaps_Desikan86.txt -out /home/yusuf/repo/projects/streamlineLoss/01_scalars/test/ --numNodes 86
## -m node_betweenness_centrality -conn /home/yusuf/repo/projects/streamlineLoss/data/connectomes/5TT_Basic_1mm/raw/ -sid 100002_t0 -sm /home/yusuf/data/atlases/birkanSubnetworks/Birkan_11System_in_Desikan86.txt -hm /home/yusuf/data/atlases/Desikan86/hemisphereMaps_Desikan86.txt -out /home/yusuf/repo/projects/streamlineLoss/01_scalars/test/ --numNodes 86 --normalizeConnectomes

######################main code####################
##### get command line parameters
parser = argparse.ArgumentParser(description='Gather values for a random variable in male/female populations')
parser.add_argument('-ml','--measuresList', help='path to the file that contains list of graph theory measures to be calculated', required=False,type=str,default="")
parser.add_argument('-m','--measure', help='name of the single graph theory measures to be calculated', required=False,type=str,default="")
parser.add_argument('-conn','--connectomesFolder', help='folder path that contains the result matrices', required=False,default="")
parser.add_argument('-sl','--subjectsList', help='path to the file that contains list of subjects to be processed', required=False,type=str,default="")
parser.add_argument('-sid','--subjectID', help='filename of the subject, if a single subject is to be processed, or <all> if you want all the subjects under conenctome folder to be processed', required=False,type=str,default="")
parser.add_argument('-sm','--systemMaps', help='file path that contains the community affiliations for the nodes', required=False,default="")
parser.add_argument('-hm','--hemisphereMaps', help='file path that contains the hemispehere information for the nodes', required=False,default="")
parser.add_argument('-out','--outputFolder', help='file path to save the distribution of values for the two populations', required=False,default="./")
parser.add_argument('--outputExtension', help='file extension to save measures in (such as txt or csv)', required=False,default="txt")
parser.add_argument('--outputDelimiter', help='Delimiter to use while saving measures in output file (such as comma,tab, or space)', required=False,default=" ")
parser.add_argument('--numNodes', help='number of ROIs in the atlas', required=False,type=int,default=-1)
parser.add_argument('--printFullMeasureList', help='print the full list of measures to standard output that the script can calculate', required=False,action='store_true',default=False)
parser.add_argument('--normalizeConnectomes', help='use normalized connectomes in the calculation of measures by making total sum of edges equal across the samples, or maximum edge being equal to 1 in each subject, or max edge across the sample being equal to one', required=False,choices=['totalSum1_subject','maxEdge1_sample','maxEdge1_subject','none'],default='none')
parser.add_argument('--scaleUp', help='scale up edges to make min nonzero edge equal to 1', required=False,action='store_true',default=False)
parser.add_argument('--verbose', help='print error/warning messages', required=False,action='store_true',default=False)

args = vars(parser.parse_args())
measuresListPath=args['measuresList']
singleMeasure=args['measure']
connectomesFolder=args['connectomesFolder']
subjectListPath=args['subjectsList']
subjectID=args['subjectID']
systemMapsPath=args['systemMaps']
hemisphereMapsPath=args['hemisphereMaps']
outputFolder=args['outputFolder']
outputExtension=args['outputExtension']
outputDelimiter=args['outputDelimiter']
numNodes=args['numNodes']
printFullMeasureList=args['printFullMeasureList']
normalizeConnectomes=args['normalizeConnectomes']
scaleUp=args['scaleUp']
verbose=args['verbose']

###below are all possible measures htat the code generates, that are separated into two groups (nodal/global)
nodalMeasures=["degree","degree_interHemisphere","degree_intraHemisphere","degree_withinModule","degree_betweenModule",
               "strength_noSelf","strength_interHemisphere","strength_intraHemisphere","strength_withinModule","strength_betweenModule", "strength_selfConnections_nodal",
               "node_betweenness_centrality","eigenvector_centrality","local_efficiency","modularity_nodal","participation_coefficient",
               "clustering_coefficient","clustering_coefficient_zhang","eccentricity","local_assortativity","rich_club_coefficient","rich_club_coefficient_normalized",
               "degree_neg","degree_interHemisphere_neg","degree_intraHemisphere_neg","degree_withinModule_neg","degree_betweenModule_neg",
               "strength_noSelf_neg","strength_interHemisphere_neg","strength_intraHemisphere_neg","strength_withinModule_neg","strength_betweenModule_neg",
               "participation_coefficient_pos","participation_coefficient_neg","modularity_nodal_neg","clustering_coefficient_neg","clustering_coefficient_zhang_neg","local_assortativity_neg"]

globalMeasures=["degree_avg","degree_interHemisphere_avg","degree_intraHemisphere_avg","degree_withinModule_avg","degree_betweenModule_avg",
                "strength_global","strength_global_offDiagonal","strength_interHemisphere_global","strength_intraHemisphere_global","strength_selfConnections_global",
                "node_betweenness_centrality_avg","eigenvector_centrality_avg","participation_coefficient_avg",
                "clustering_coefficient_avg","clustering_coefficient_zhang_avg","eccentricity_avg",
                "small_worldness","characteristic_path_length","global_efficiency","radius","diameter","modularity_global","assortativity","density",
                "degree_neg_avg","degree_interHemisphere_neg_avg","degree_intraHemisphere_neg_avg","degree_withinModule_neg_avg","degree_betweenModule_neg_avg",
                "strength_global_neg","strength_global_offDiagonal_neg","strength_interHemisphere_global_neg","strength_intraHemisphere_global_neg",
                "participation_coefficient_pos_avg","participation_coefficient_neg_avg","clustering_coefficient_neg_avg","clustering_coefficient_zhang_neg_avg","modularity_global_neg"]
                

if(printFullMeasureList==True):
    print('\n'.join(["####Nodal Measures"]+nodalMeasures+["####Global Measures"]+globalMeasures))
    exit()

#########load list of graph theory measures to be calculated
if(measuresListPath!="" and singleMeasure!=""):
    print("You should either provide a list of measures with --measuresList or single measure with --measure parameters. You cannot provide both!!! Exiting...")
    exit()
elif(measuresListPath!=""): #if a measure list is provided, then load it as the measures to be generated,
    with open(measuresListPath) as fl:
        loaded = fl.read().splitlines()
        measuresList = [x for x in loaded if x[0]!='#'] 
elif(singleMeasure!=""): # else if a sinle measure is provided, generate results for this measure
    measuresList = [singleMeasure]
else: #otherwise generate results for all available measures
    measuresList = nodalMeasures+globalMeasures

measureList_tmp=[]
for measure in measuresList:
    if(measure not in nodalMeasures+globalMeasures):
        print("Measure <%s> that was asked among measures to calculate cannot be processed by the script as it's not recognized by the script. Execution will continue with the rest of the measures (if any)." %measure)
        if(len(measuresList)==1): # if this was the only measure (which ended up being incorrect), then exit execution
            exit()
    else:
        measureList_tmp.append(measure)
measuresList=measureList_tmp.copy()

#########load system maps for nodes, if the parameter is provided when running the script
if(systemMapsPath!=""):
    systemMaps = np.array(np.loadtxt(systemMapsPath))

#########load system maps for nodes, if the parameter is provided when running the script
if(hemisphereMapsPath!=""):
    hemisphereMaps = np.array(np.loadtxt(hemisphereMapsPath))

#########load connectomes and subject list
#load filenames for connectome files
if (subjectListPath=="" and subjectID==""):
    print("You should either provide (a list of files | parameter 'all') using --subjectListPath flag, or identify a single subject using --subjectID flag! Exiting...")
    exit(1)
elif(subjectID=="all"): # generate connectomes for all subjects included under the timeseries folder
    subjectList=np.array([x.split(".")[0] for x in sorted(os.listdir(connectomesFolder))])
elif(subjectID!=""): #ogenerate connectomes for a single subject, whose ID is provided
    subjectList=np.array([subjectID])
elif(subjectListPath!=""): #if a subject list is provided, then generate connectome only for those subjects
    subjectList=np.loadtxt(subjectListPath,dtype=str).tolist()
else:
    print("Incorrect parameter entered for which subjects to process!!! Exiting...")
    exit(1)

#load connectomes
connectomesFileList = np.array([connectomesFolder + x for x in sorted(os.listdir(connectomesFolder)) if x.split(".")[0] in subjectList]) #get the subject id by discarding extension from filename
#Note: connectomes are defined in terms of the relation between regions (the more the two are related, the higher is the pairwise relation value)
if(len(connectomesFileList)==0):
    print("No connectome file found in the path that is provided: < %s > !!! Check the path that you provided to --connectomesFolder parameter! Exiting..." %connectomesFolder)
    exit()

# discard connectomes which has missing node
if(numNodes==-1):
    print("Number of nodes are not provided!! Use --numNodes parameter to provide expected number of nodes in each conenctomes! Exiting...")
    exit()
    
weightedConnectomes = []
dropList=[]
for i in range(len(connectomesFileList)):
    tempConn=np.loadtxt(connectomesFileList[i])
    if(len(tempConn)==numNodes): # discard connectomes which has missing node
        weightedConnectomes.append(tempConn)
    else:
        dropList.append(i)
        print("Subject %s has missing node in the connectome!!! Will be discarded from the analysis...\n" % subjectList[i])
weightedConnectomes=np.array(weightedConnectomes)
###remove the discarded subjects from subject list
subjectList=np.delete(subjectList,dropList)
connectomesFileList=np.delete(connectomesFileList,dropList)

#TODO: remove edge weights that are less than 1, if the matrix consists of all positive numbers


if("strength_selfConnections_nodal" in measuresList):
    selfEdges_nodal=np.array([x.diagonal() for x in weightedConnectomes])
    np.savetxt(outputFolder+"strength_selfConnections_nodal."+outputExtension,selfEdges_nodal,fmt='%0.6g',delimiter=outputDelimiter)
    measuresList.remove("strength_selfConnections_nodal")
if("strength_selfConnections_global" in measuresList):
    selfEdges_global=np.array([np.trace(x) for x in weightedConnectomes])
    np.savetxt(outputFolder+"strength_selfConnections_global."+outputExtension,selfEdges_global,fmt='%0.6g',delimiter=outputDelimiter)
    measuresList.remove("strength_selfConnections_global")
if("strength_global" in measuresList):
    strength_global=np.array([np.trace(x) + calculate_strength_total(x).sum()/2 for x in weightedConnectomes])
    np.savetxt(outputFolder+"strength_global."+outputExtension,strength_global,fmt='%0.6g',delimiter=outputDelimiter)
    measuresList.remove("strength_global")
if("strength_global_neg" in measuresList):
    strength_global=np.array([np.trace(x) + calculate_strength_total(x,sign="negative").sum()/2 for x in weightedConnectomes])
    np.savetxt(outputFolder+"strength_global_neg."+outputExtension,strength_global,fmt='%0.6g',delimiter=outputDelimiter)
    measuresList.remove("strength_global_neg")   

#remove self edges from connectomes if exist
for i in range(len(weightedConnectomes)):
    np.fill_diagonal(weightedConnectomes[i],0)

##normalize connectomes
# 'totalSum1_subject','maxEdge1_sample','maxEdge1_subject','none'
if(normalizeConnectomes=='maxEdge1_subject'):
    weightedConnectomes_norm = weightedConnectomes/np.array([np.max(np.abs(x)) for x in weightedConnectomes])[:,np.newaxis,np.newaxis] # normalize each conenctome within itself with max node having value 1 in each connectome
elif(normalizeConnectomes=='maxEdge1_sample'):    
    weightedConnectomes_norm = weightedConnectomes / np.max(np.abs(weightedConnectomes)) # bct.utils.weight_conversion(weightedConnectomes,"normalize") # normalize connectomes across the population, with the largest edge across the population getting value 1, and the rest scaled accordingly using formula weightedConnectomes/np.max(np.abs(weightedConnectomes)) 
elif(normalizeConnectomes=='totalSum1_subject'): 
    weightedConnectomes_norm = weightedConnectomes/np.array([np.sum(x) for x in weightedConnectomes])[:,np.newaxis,np.newaxis]

if(scaleUp==True):
    weightedConnectomes_norm = weightedConnectomes_norm / np.min(np.abs(weightedConnectomes_norm[np.nonzero(weightedConnectomes_norm)])) 
    weightedConnectomes = weightedConnectomes / np.min(np.abs(weightedConnectomes[np.nonzero(weightedConnectomes)])) 

##invert the connectomes since we will use them for distance calculations
#weightedConnectomes_length = bct.utils.weight_conversion(weightedConnectomes,"lengths") # 1.0/(weightedConnectomes+1e-12 )
if(normalizeConnectomes!='none'):
    weightedConnectomes_length_norm = bct.utils.weight_conversion(weightedConnectomes_norm,"lengths") # calculate length (by inverting edge weights) using normalized connectomes

##calculate distance matrix over the conenctomes
#weightedConnectomes_dist_length = np.array([bct.distance_wei(x)[0] for x in weightedConnectomes_length]) # input to bct.distance_wei is Directed/undirected connection-length matrix. (that is, it is the weightedConnectomes_length matrix. It is not the adjacency matrix of connections) 
if(normalizeConnectomes!='none'):
    weightedConnectomes_dist_length_norm = np.array([bct.distance_wei(x)[0] for x in weightedConnectomes_length_norm]) # input to bct.distance_wei is Directed/undirected connection-length matrix. (that is, it is the weightedConnectomes_length matrix. It is not the adjacency matrix of connections)

###NOTE: naming convention of weightedConnectomes is as follows: read the order of operations done on matrices from right to left 
## (eg: _dist_length_norm means connectomes are first normalized, then lengths are calculated, and then distances are calculated)
## weightedConnectomes_length : length is calculated by inversing weights
## weightedConnectomes_norm   : weigths are normalized relative to the largest edge weight across the population
## weightedConnectomes_length_norm : weights are first normalized, then lengths are calculated by taking the inverse of normalized edge weights
## weightedConnectomes_dist_length : all pairs shortest path between nodes are calculated using weightedConnectomes_length matrix
## weightedConnectomes_dist_length_norm : all pairs shortest path between nodes are calculated using weightedConnectomes_norm_length matrix

### if normalizeConnectomes flag was set, then use normalized connectomes for the majority of the calculations below (some of the measures will use normalized connectomes in any case!)
if(normalizeConnectomes!='none'):
    connectomes=weightedConnectomes_norm
else:
    connectomes=weightedConnectomes

numSubjects=len(connectomes)

##############
for measure in measuresList:
    if measure in nodalMeasures:
        measure_matrix=np.zeros(shape=(numSubjects,numNodes))
    elif measure in globalMeasures:
        measure_matrix=np.zeros(numSubjects)
        
    print(measure)
    
    for i in range(numSubjects):
        if(verbose==True):
            print("%s " %(subjectList[i]),end='',flush=True)
        
        ###nodal degree related measures
        #positive
        if(measure == "degree"):
            measure_matrix[i]=calculate_degree_total(connectomes[i])
        elif(measure == "degree_interHemisphere"):
            measure_matrix[i]=calculate_degree_interHemisphere(connectomes[i],hemisphereMaps)
        elif(measure == "degree_intraHemisphere"):
            measure_matrix[i]=calculate_degree_intraHemisphere(connectomes[i],hemisphereMaps)
        elif(measure == "degree_withinModule"):
            measure_matrix[i]=calculate_degree_withinModule(connectomes[i],systemMaps)
        elif(measure == "degree_betweenModule"):
            measure_matrix[i]=calculate_degree_betweenModule(connectomes[i],systemMaps)
        #negative
        elif(measure == "degree_neg"):
            measure_matrix[i]=calculate_degree_total(connectomes[i],sign="negative")
        elif(measure == "degree_interHemisphere_neg"):
            measure_matrix[i]=calculate_degree_interHemisphere(connectomes[i],hemisphereMaps,sign="negative")
        elif(measure == "degree_intraHemisphere_neg"):
            measure_matrix[i]=calculate_degree_intraHemisphere(connectomes[i],hemisphereMaps,sign="negative")
        elif(measure == "degree_withinModule_neg"):
            measure_matrix[i]=calculate_degree_withinModule(connectomes[i],systemMaps,sign="negative")
        elif(measure == "degree_betweenModule_neg"):
            measure_matrix[i]=calculate_degree_betweenModule(connectomes[i],systemMaps,sign="negative")
        
        #nodal strength related measures
        #positive
        elif(measure == "strength_noSelf"):
            measure_matrix[i]=calculate_strength_total(connectomes[i])
        elif(measure == "strength_self"):
            measure_matrix[i]=connectomes[i].diagonal()
        elif(measure == "strength_interHemisphere"):
            measure_matrix[i]=calculate_strength_interHemisphere(connectomes[i],hemisphereMaps)
        elif(measure == "strength_intraHemisphere"):
            measure_matrix[i]=calculate_strength_intraHemisphere(connectomes[i],hemisphereMaps)
        elif(measure == "strength_withinModule"):
            measure_matrix[i]=calculate_strength_withinModule(connectomes[i],systemMaps)
        elif(measure == "strength_betweenModule"):
            measure_matrix[i]=calculate_strength_betweenModule(connectomes[i],systemMaps)
        #negative
        elif(measure == "strength_noSelf_neg"):
            measure_matrix[i]=calculate_strength_total(connectomes[i],sign="negative")
        elif(measure == "strength_interHemisphere_neg"):
            measure_matrix[i]=calculate_strength_interHemisphere(connectomes[i],hemisphereMaps,sign="negative")
        elif(measure == "strength_intraHemisphere_neg"):
            measure_matrix[i]=calculate_strength_intraHemisphere(connectomes[i],hemisphereMaps,sign="negative")
        elif(measure == "strength_withinModule_neg"):
            measure_matrix[i]=calculate_strength_withinModule(connectomes[i],systemMaps,sign="negative")
        elif(measure == "strength_betweenModule_neg"):
            measure_matrix[i]=calculate_strength_betweenModule(connectomes[i],systemMaps,sign="negative")
            
        #nodal BCT measures
        elif(measure == "node_betweenness_centrality"):
            measure_matrix[i]=bct.edge_betweenness_wei(weightedConnectomes_length_norm[i])[1]/float((numNodes-1)*(numNodes-2)) #normalize the betwenness centrality. Note that, input being weightedConnectomes_length_norm or weightedConnectomes_length doesn't affect the output of this function, as expected
            #NOTE:The input matrix must be a connection-length matrix, typically obtained via a mapping from weight to length. For instance, in a weighted 
            #correlation network higher correlations are more naturally interpreted as shorter distances and the input matrix should consequently be some 
            #inverse of the connectivity matrix. Betweenness centrality may be normalised to the range [0,1] as BC/[(N-1)(N-2)], where N is the number of nodes in the network.
        elif(measure == "eigenvector_centrality"):
            measure_matrix[i]=bct.eigenvector_centrality_und(connectomes[i]) #input is binary/weighted undirected adjacency matrix
        elif(measure == "local_efficiency"):
            measure_matrix[i]=bct.efficiency_wei(weightedConnectomes_norm[i],local=True) #input is the undirected weighted connection matrix (all weights in input matrix must be between 0 and 1) (NOTE: input is not 1/W_ij distance matrix!!)
        elif(measure == "local_assortativity"): ## NOTE: I updated the bct.local_assortativity_wu_sign function to make bct.local_assortativity_wu_pos where local_assortativity is calculated only for the positive values, in order to avoid getting the error message when running the code with matrices which only has positive edges
            measure_matrix[i]=bct.local_assortativity_wu_pos(connectomes[i]) #input is undirected connection matrix with positive and negative weights (output 0 is positive local_assortativity)
        elif(measure == "local_assortativity_neg"):
            measure_matrix[i]=bct.local_assortativity_wu_sign(connectomes[i])[1] #input is undirected connection matrix with positive and negative weights (output 0 is positive local_assortativity)
        elif(measure == "modularity_nodal"):
            measure_matrix[i]=bct.modularity_louvain_und(connectomes[i])[0] #input is undirected weighted/binary connection matrix, output is the assigned modules for each node
        elif(measure == "modularity_nodal_neg"):
            measure_matrix[i]=bct.modularity_louvain_und_sign(connectomes[i])[0] #input is undirected weighted/binary connection matrix with positive and negative weights, output is the assigned modules for each node
        elif(measure == "participation_coefficient"):
            measure_matrix[i]=bct.participation_coef(connectomes[i],systemMaps,'undirected') #input is binary/weighted directed/undirected connection matrix (not distance matrix!)
        elif(measure == "participation_coefficient_pos"):
            measure_matrix[i]=bct.participation_coef_sign(connectomes[i],systemMaps)[0]
        elif(measure == "participation_coefficient_neg"):
            measure_matrix[i]=bct.participation_coef_sign(connectomes[i],systemMaps)[1]
        elif(measure == "clustering_coefficient"):
            measure_matrix[i]=bct.clustering_coef_wu_sign(connectomes[i],coef_type='default')[0] #input is weighted directed connection matrix,  coef_type='default'  uses Onnela version of the formula
        elif(measure == "clustering_coefficient_neg"):
            measure_matrix[i]=bct.clustering_coef_wu_sign(connectomes[i],coef_type='default')[1] #input is weighted directed connection matrix,  coef_type='default'  uses Onnela version of the formula
        elif(measure == "clustering_coefficient_zhang"):
            measure_matrix[i]=bct.clustering_coef_wu_sign(connectomes[i],coef_type='zhang')[0] #input is weighted directed connection matrix, coef_type='zhang' makes the denominator to be weighted as well, Reduces sensitivity of the measure toweights directly connected to the node of interest. See Yeh et al., 2016, NIMG Appendix C for justification of using this over Onnela et al. version of the measure
        elif(measure == "clustering_coefficient_zhang_neg"):
            measure_matrix[i]=bct.clustering_coef_wu_sign(connectomes[i],coef_type='zhang')[1] #input is weighted directed connection matrix, coef_type='zhang' makes the denominator to be weighted as well, Reduces sensitivity of the measure toweights directly connected to the node of interest. See Yeh et al., 2016, NIMG Appendix C for justification of using this over Onnela et al. version of the measure
        elif(measure == "eccentricity"):
            measure_matrix[i]=bct.charpath(weightedConnectomes_dist_length_norm[i])[2] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        elif(measure == "rich_club_coefficient"): ## see Van Den Heuvel, M.P. and Sporns, O., 2011. Rich-club organization of the human connectome. Journal of Neuroscience, 31(44), pp.15775-15786.
            tmpMeasure=bct.rich_club_wu(connectomes[i],klevel=None) #input matrix is weighted undirected connection matrix, and klevel is the max level in which rich club coefficieent will be calculated,
            #output is a Kx1 vector of rich-club coefficients for levels 1 to klevel, if klevel=None, it will take k=maxDegree of the network
            maxDegree=np.max(np.sum((connectomes[i]!=0),axis=0))
            measure_matrix[i,numNodes-maxDegree:]=tmpMeasure
        elif(measure == "rich_club_coefficient_normalized"): ## see Van Den Heuvel, M.P. and Sporns, O., 2011. Rich-club organization of the human connectome. Journal of Neuroscience, 31(44), pp.15775-15786.
            if(verbose==True):
                print("%s: Calculating rich_club_coefficient_normalized:" %subjectList[i])
            tmpMeasure=bct.rich_club_wu(connectomes[i],klevel=None) #input matrix is weighted undirected connection matrix, and klevel is the max level in which rich club coefficieent will be calculated,
            #output is a Kx1 vector of rich-club coefficients for levels 1 to klevel, if klevel=None, it will take k=maxDegree of the network
            maxDegree=np.max(np.sum((connectomes[i]!=0),axis=0))
            numRandomNetworks=100
            numItr=5
            random_richClubCoefficients=np.zeros((numRandomNetworks,maxDegree)) # all randomly shuffled networks will have the same K, since shuffling is degree distribution preserving
            for j in range(numRandomNetworks):
                shuffledMatrix=bct.randmio_und(connectomes[i],numItr,seed=j)[0] #randomize network while preserving degree distribution
                random_richClubCoefficients[j]=bct.rich_club_wu(shuffledMatrix,klevel=None)
                if(verbose==True):
                    print("Rand shuffling: %d / %d" %(j,numRandomNetworks))
            # calculate average rich club coefficients of the randomly shuffled networks by taking the mean
            avgRandMeasures=np.zeros(maxDegree)
            for j in range(maxDegree):
                avgRandMeasures[j]=np.nansum(random_richClubCoefficients[:,j])/float(numRandomNetworks)
            # normalization of rich club coefficients: divide actual rich club coefficeints with the coefficients that you obtained from random networks
            tmpMeasure=tmpMeasure/avgRandMeasures  #both measures in this division has the same number of elements, which is equal to maxDegree calculated below, since randomization is degree preserving
            measure_matrix[i,numNodes-maxDegree:]=tmpMeasure
        
        
        ###global degree related measures
        #positive
        elif(measure == "degree_avg"):
            measure_matrix[i]=calculate_degree_total(connectomes[i]).mean()
        elif(measure == "degree_interHemisphere_avg"):
            measure_matrix[i]=calculate_degree_interHemisphere(connectomes[i],hemisphereMaps).mean()
        elif(measure == "degree_intraHemisphere_avg"):
            measure_matrix[i]=calculate_degree_intraHemisphere(connectomes[i],hemisphereMaps).mean()
        elif(measure == "degree_withinModule_avg"):
            measure_matrix[i]=calculate_degree_withinModule(connectomes[i],systemMaps).mean()
        elif(measure == "degree_betweenModule_avg"):
            measure_matrix[i]=calculate_degree_betweenModule(connectomes[i],systemMaps).mean()
        #negative
        elif(measure == "degree_neg_avg"):
            measure_matrix[i]=calculate_degree_total(connectomes[i],sign="negative").mean()
        elif(measure == "degree_interHemisphere_neg_avg"):
            measure_matrix[i]=calculate_degree_interHemisphere(connectomes[i],hemisphereMaps,sign="negative").mean()
        elif(measure == "degree_intraHemisphere_neg_avg"):
            measure_matrix[i]=calculate_degree_intraHemisphere(connectomes[i],hemisphereMaps,sign="negative").mean()
        elif(measure == "degree_withinModule_neg_avg"):
            measure_matrix[i]=calculate_degree_withinModule(connectomes[i],systemMaps,sign="negative").mean()
        elif(measure == "degree_betweenModule_neg_avg"):
            measure_matrix[i]=calculate_degree_betweenModule(connectomes[i],systemMaps,sign="negative").mean()
        
        #global strength related measures
        #positive
        elif(measure == "strength_global_offDiagonal"):
            measure_matrix[i]=calculate_strength_total(connectomes[i]).sum()/2
        elif(measure == "strength_interHemisphere_global"):
            measure_matrix[i]=calculate_strength_interHemisphere(connectomes[i],hemisphereMaps).sum()/2
        elif(measure == "strength_intraHemisphere_global"):
            measure_matrix[i]=calculate_strength_intraHemisphere(connectomes[i],hemisphereMaps).sum()/2
        #negative
        elif(measure == "strength_global_offDiagonal_neg"):
            measure_matrix[i]=calculate_strength_total(connectomes[i],sign="negative").sum()/2
        elif(measure == "strength_interHemisphere_global_neg"):
            measure_matrix[i]=calculate_strength_interHemisphere(connectomes[i],hemisphereMaps,sign="negative").sum()/2
        elif(measure == "strength_intraHemisphere_global_neg"):
            measure_matrix[i]=calculate_strength_intraHemisphere(connectomes[i],hemisphereMaps,sign="negative").sum()/2
        
        #average of nodal features
        #"node_betweenness_centrality_avg","eigenvector_centrality_avg","participation_coefficient_avg","participation_coefficient_pos_avg","participation_coefficient_neg_avg",
        #"clustering_coefficient_avg","clustering_coefficient_neg_avg","clustering_coefficient_zhang_avg","clustering_coefficient_zhang_neg_avg","eccentricity_avg","local_assortativity_avg","local_assortativity_neg_avg",
        elif(measure == "node_betweenness_centrality_avg"):
            measure_matrix[i]=np.mean(bct.edge_betweenness_wei(weightedConnectomes_length_norm[i])[1]/float((numNodes-1)*(numNodes-2))) #normalize the betwenness centrality. Note that, input being weightedConnectomes_length_norm or weightedConnectomes_length doesn't affect the output of this function, as expected
            #NOTE:The input matrix must be a connection-length matrix, typically obtained via a mapping from weight to length. For instance, in a weighted 
            #correlation network higher correlations are more naturally interpreted as shorter distances and the input matrix should consequently be some 
            #inverse of the connectivity matrix. Betweenness centrality may be normalised to the range [0,1] as BC/[(N-1)(N-2)], where N is the number of nodes in the network.
        elif(measure == "eigenvector_centrality_avg"):
            measure_matrix[i]=np.mean(bct.eigenvector_centrality_und(connectomes[i])) #input is binary/weighted undirected adjacency matrix
        elif(measure == "participation_coefficient_avg"):
            measure_matrix[i]=np.mean(bct.participation_coef(connectomes[i],systemMaps,'undirected')) #input is binary/weighted directed/undirected connection matrix (not distance matrix!)
        elif(measure == "participation_coefficient_pos_avg"):
            measure_matrix[i]=np.mean(bct.participation_coef_sign(connectomes[i],systemMaps)[0])
        elif(measure == "participation_coefficient_neg_avg"):
            measure_matrix[i]=np.mean(bct.participation_coef_sign(connectomes[i],systemMaps)[1])
        elif(measure == "clustering_coefficient_avg"):
            measure_matrix[i]=np.mean(bct.clustering_coef_wu_sign(connectomes[i],coef_type='default')[0]) #input is weighted directed connection matrix,  coef_type='default'  uses Onnela version of the formula
        elif(measure == "clustering_coefficient_neg_avg"):
            measure_matrix[i]=np.mean(bct.clustering_coef_wu_sign(connectomes[i],coef_type='default')[1]) #input is weighted directed connection matrix,  coef_type='default'  uses Onnela version of the formula
        elif(measure == "clustering_coefficient_zhang_avg"):
            measure_matrix[i]=np.mean(bct.clustering_coef_wu_sign(connectomes[i],coef_type='zhang')[0]) #input is weighted directed connection matrix, coef_type='zhang' makes the denominator to be weighted as well, Reduces sensitivity of the measure toweights directly connected to the node of interest. See Yeh et al., 2016, NIMG Appendix C for justification of using this over Onnela et al. version of the measure
        elif(measure == "clustering_coefficient_zhang_neg_avg"):
            measure_matrix[i]=np.mean(bct.clustering_coef_wu_sign(connectomes[i],coef_type='zhang')[1]) #input is weighted directed connection matrix, coef_type='zhang' makes the denominator to be weighted as well, Reduces sensitivity of the measure toweights directly connected to the node of interest. See Yeh et al., 2016, NIMG Appendix C for justification of using this over Onnela et al. version of the measure
        elif(measure == "eccentricity_avg"):
            measure_matrix[i]=np.mean(bct.charpath(weightedConnectomes_dist_length_norm[i])[2]) #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        
        #global BCT measures
        elif(measure == "small_worldness"):
            clusteringCoeff=np.mean(bct.clustering_coef_wu_sign(connectomes[i],coef_type='zhang')[0]) #input is weighted directed connection matrix,  coef_type='default'  uses Onnela version of the formula
            charPathLength=bct.charpath(weightedConnectomes_dist_length_norm[i])[0] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            numRandomNetworks=100
            clusteringCoeffRand=np.zeros(numRandomNetworks)
            charPathLengthRand=np.zeros(numRandomNetworks)
            if(verbose==True):
                print("\nRand shuffling out of %d:" %numRandomNetworks,flush=True,end='')
            for j in range(numRandomNetworks):
                if(verbose==True):
                    print("%d," %(j),flush=True,end='')
                randConnectome,_=bct.null_model_und_sign(connectomes[i],seed=j)
                randConnectome_dist_length_norm=bct.distance_wei(bct.utils.weight_conversion(bct.utils.weight_conversion(randConnectome,"normalize"),"lengths"))[0]
                clusteringCoeffRand[j]=np.mean(bct.clustering_coef_wu_sign(randConnectome,coef_type='zhang')[0])
                charPathLengthRand[j]=bct.charpath(randConnectome_dist_length_norm)[0]
            if(verbose==True):
                print("\n",flush=True,end='')
            clusteringCoeffRand_avg=clusteringCoeffRand.mean()
            charPathLengthRand_avg=charPathLengthRand.mean()
            measure_matrix[i]=(clusteringCoeff/clusteringCoeffRand_avg)/(charPathLength/charPathLengthRand_avg)
                
        elif(measure == "characteristic_path_length"):
            measure_matrix[i]=bct.charpath(weightedConnectomes_dist_length_norm[i])[0] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        elif(measure == "global_efficiency"): ## NOTE: bct.efficiency_wei() and bct.charpath() calculate global_efficiency and results are the same. The only difference is, bct.efficiency_wei expects input to be normalized into [0,1]. We normalized the connectomes across the population and ran bct.charpath() with these connectomes. Thus, results would have been the same anyways.
            measure_matrix[i]=bct.charpath(weightedConnectomes_dist_length_norm[i])[1] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        elif(measure == "radius"):
            measure_matrix[i]=bct.charpath(weightedConnectomes_dist_length_norm[i])[3] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        elif(measure == "diameter"):
            measure_matrix[i]=bct.charpath(weightedConnectomes_dist_length_norm[i])[4] #input is distance matrix, which we obtained by calling bct.distance_wei while loading connectomes
            #NOTE: output of this function is lambda (characteristic path length), efficiency(global efficiency), ecc( Nx1 np.ndarray denoting eccentricity at each vertex) ,radius (radius of graph), and diameter (diameter of graph)
        elif(measure == "modularity_global"):
            measure_matrix[i]=bct.modularity_louvain_und(connectomes[i])[1] #input is undirected weighted/binary connection matrix, output is an optimized modularity metric
            #NOTE: The modularity is a statistic that quantifies the degree to which the network may be subdivided into such clearly delineated groups.
        elif(measure == "modularity_global_neg"):
            measure_matrix[i]=bct.modularity_louvain_und_sign(connectomes[i])[1] #input is undirected weighted/binary connection matrix with positive and negative weights, output is an optimized modularity metric
            #NOTE: The modularity is a statistic that quantifies the degree to which the network may be subdivided into such clearly delineated groups.
        elif(measure == "density"):
            measure_matrix[i]=bct.density_und(connectomes[i])[0] #input matrix is weighted directed/undirected connection matrix, outputs are density, numnodes, num edges
        elif(measure == "assortativity"):
            measure_matrix[i]=bct.assortativity_wei(connectomes[i],flag=0) #input matrix is weighted directed/undirected connection matrix, flag=0 indicates that matrix is undirected
        else:
            print("Undefined measure requested, exiting...\n")
            exit(1)
    print("") #print an empty line for separation
        
    np.savetxt(outputFolder+measure+"."+outputExtension,measure_matrix,fmt='%0.6g',delimiter=outputDelimiter)
print("Done!!!")