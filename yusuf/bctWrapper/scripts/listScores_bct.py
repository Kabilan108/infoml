#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:56:39 2020

@author: yusuf
"""
import argparse
import numpy as np
from numpy.lib.recfunctions import append_fields,rename_fields,drop_fields

## --subjectsList /home/yusuf/repo/projects/tbiStructureAndFunction/results/brainLes++/data/src/subjects_qa.txt --measuresFolder /home/yusuf/repo/projects/tbiStructureAndFunction/results/brainLes++/08_bctFeatures/features/raw_gmvmivol --measuresList /home/yusuf/repo/projects/tbiStructureAndFunction/results/brainLes++/08_bctFeatures/featureList.txt --similarityScores /home/yusuf/repo/projects/tbiStructureAndFunction/results/brainLes++/01_matching/results/processed/raw_gmvmivol/direct/connectomeLevel/accuracy_healthy_direct.res --outputFolder /home/yusuf/repo/projects/tbiStructureAndFunction/results/brainLes++/08_bctFeatures/raw_gmvmivol_

######################main code####################
##### get command line parameters
parser = argparse.ArgumentParser(description='Gather values for a random variable in male/female populations')
parser.add_argument('-ml','--measuresList', help='path to the file that contains list of graph theory measures to be calculated', required=False,type=str,default="")
parser.add_argument('-m','--measure', help='name of the single graph theory measures to be calculated', required=False,type=str,default="")
parser.add_argument('-ss','--similarityScores', help='path of the matching similarity scores', required=True,type=str,default="")
parser.add_argument('-mf','--measuresFolder', help='folder path that contains the node features per subject for multiple feature types', required=True)
parser.add_argument('-sl','--subjectsList', help='file path containing subjectIDs', required=True)
parser.add_argument('-d','--demographics', help='file path containing demographics info and cognitive scores', required=True)
parser.add_argument('-out','--outputFolder', help='file path to save the distribution of values for the two populations', required=True)

args = vars(parser.parse_args())
measuresListPath=args['measuresList']
singleMeasure=args['measure']
similarityScoresPath=args['similarityScores']
measuresFolder=args['measuresFolder']
subjectListPath=args['subjectsList']
outputFolder=args['outputFolder']
demographicsPath=args['demographics']

#########load subject list
subjectList=np.loadtxt(subjectListPath,dtype=str).tolist()

##############load results of the structure-function coupling experiment###################
scores=np.zeros(len(subjectList))
if(similarityScoresPath!='none'):
    fileContent =  open(similarityScoresPath,"r").read().splitlines()
    numNodes = int(fileContent[1].split('\t')[0])
    numSubjects = int(fileContent[1].split('\t')[1])
    measureType = str(fileContent[3]) 
    scoreName = str(fileContent[5]) 
    for i in range(numSubjects):
        scores[i] = float(fileContent[7].split('\t')[i])

#######################load cognitive scores########################
###load subjects info
subjectsInfo = np.genfromtxt(demographicsPath, names=True, delimiter=',', dtype=None, missing_values='.', filling_values='-10000',encoding=None)
samples = subjectsInfo['Subject'].tolist()

######################make the matching score and cognitive score table to be consisting of same set of subjects##########################
removeList=[]
for i in reversed(range(len(samples))):
    if samples[i] not in subjectList:
        removeList.append(i)
subjectsInfo = np.delete(subjectsInfo,removeList,axis=0)
samples = subjectsInfo['Subject'].tolist()

removeList=[] #also remove the subjects which do not pass QA
for i in reversed(range(len(subjectList))):
    if subjectList[i] not in samples:
        removeList.append(i)
subjectList = np.delete(subjectList,removeList,axis=0)


############### update the subjectsInfo table by dropping the unnecessary columns and renaming the rest of the columns to fit my standards
subjectsInfo=rename_fields(subjectsInfo,{'Subject':'subjectId','Group':'timePoint','Gender':'gender','PSIT': 'PS', 'ReyT':'VL', 'PTA_Estimated':'PTA','Age':'age','DaysSinceInjury':'DSI'})
subjectsInfo=drop_fields(subjectsInfo, ['Status', 'GCS_Total', 'PTA_Duration', 'Days_to_follow_commands', 'Education_Coded', 'Trails_B__TScore', 'DSBT', 'LNST', 'COWAT', 'CWITT'])

# calculate baseline age at the first scan to add as another column to the table
age_baseline = np.zeros(len(subjectsInfo))
unique_subjects=[]
min_age=[]
for order,ID in enumerate(subjectList):
    uniqueID = ID.split("_")[0]
    if(uniqueID not in unique_subjects):
        unique_subjects.append(uniqueID)
        min_age.append(subjectsInfo['age'][order])
    else:
        if(min_age[-1] > subjectsInfo['age'][order]):
            min_age[-1] = subjectsInfo['age'][order]
for order,ID in enumerate(subjectList):
    uniqueID = ID.split("_")[0]
    age_baseline[order] = min_age[unique_subjects.index(uniqueID)]
subjectsInfo=append_fields(subjectsInfo, 'ageBaseline', age_baseline, int)

# update the way we store subject IDs and timepoint information
for i in range(len(subjectsInfo)):
    subjectsInfo[i]['subjectId']=subjectsInfo[i]['subjectId'].split('_')[0]
    if(subjectsInfo[i]['timePoint']=="CON"):
        subjectsInfo[i]['timePoint']="c"
    else:
        subjectsInfo[i]['timePoint']="s"+subjectsInfo[i]['timePoint'][1]

######################load graph theory measures
###below are all possible global measures that the code generates
globalMeasures=["degree_avg","degree_interHemisphere_avg","degree_intraHemisphere_avg","degree_withinModule_avg","degree_betweenModule_avg",
                "strength_global","strength_global_offDiagonal","strength_interHemisphere_global","strength_intraHemisphere_global","strength_selfConnections_global",
                "node_betweenness_centrality_avg","eigenvector_centrality_avg","participation_coefficient_avg",
                "clustering_coefficient_avg","clustering_coefficient_zhang_avg","eccentricity_avg",
                "small_worldness","characteristic_path_length","global_efficiency","radius","diameter","modularity_global","assortativity","density",
                "degree_neg_avg","degree_interHemisphere_neg_avg","degree_intraHemisphere_neg_avg","degree_withinModule_neg_avg","degree_betweenModule_neg_avg",
                "strength_global_neg","strength_global_offDiagonal_neg","strength_interHemisphere_global_neg","strength_intraHemisphere_global_neg",
                "participation_coefficient_pos_avg","participation_coefficient_neg_avg","clustering_coefficient_neg_avg","clustering_coefficient_zhang_neg_avg","modularity_global_neg"]
                
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
    measuresList = globalMeasures

### sort out measures list into connectome/system/node level
measureNames=[]
for measure in measuresList:
    if(measure not in globalMeasures):
        print("Measure <%s> that was asked among measures to calculate cannot be processed by the script as it's not recognized by the script. Execution will continue with the rest of the measures (if any)." % measure)
        if(len(measuresList)==1): # if this was the only measure (which ended up being incorrect), then exit execution
            exit()
    elif(measure in globalMeasures):
        measureNames.append(measure)

# load connectome level (i.e., global) BCT measures
measures=[]
for measureName in measureNames:
    measures.append(np.loadtxt(measuresFolder+"/"+measureName+".txt"))
measures=np.array(measures) ### measures matrix is of dimension: (numMeasures x numSubjects)
numMeasures=len(measureNames)

# add loaded measures into the subjectsInfo table
for i in range(numMeasures):
    subjectsInfo=append_fields(subjectsInfo, measureNames[i], measures[i], np.double)
    
#### separate patient and healthy data
subjectsInfoPatient=subjectsInfo[subjectsInfo['timePoint']!="c"]
subjectsInfoHealthy=subjectsInfo[subjectsInfo['timePoint']=="c"]


####### save table into file
reportFile=open(outputFolder+"allScores.txt",'w')
reportFile.write("subjectId\ttimePoint\tage\tageBaseline\tgender\tDSI\tsimilarity\tEF\tPS\tVL\tPTA\tGOSE\tDRS")
for i in range(12,len(subjectsInfoPatient.dtype.names)):
    reportFile.write("\t%s" %subjectsInfoPatient.dtype.names[i])
reportFile.write("\n")
for i in range(len(subjectsInfoPatient)):
    reportFile.write("%s\t%s\t%d\t%d\t%s\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f" % (subjectsInfoPatient['subjectId'][i],subjectsInfoPatient['timePoint'][i],subjectsInfoPatient['age'][i],subjectsInfoPatient['ageBaseline'][i],subjectsInfoPatient['gender'][i],subjectsInfoPatient['DSI'][i],scores[i], subjectsInfoPatient['EF'][i],subjectsInfoPatient['PS'][i],subjectsInfoPatient['VL'][i],subjectsInfoPatient['PTA'][i],subjectsInfoPatient['GOSE'][i],subjectsInfoPatient['DRS'][i]))
    for j in range(12,len(subjectsInfoPatient.dtype.names)):
        featureName=subjectsInfoPatient.dtype.names[j]
        reportFile.write("\t%f" %subjectsInfoPatient[featureName][i])
    reportFile.write("\n")
reportFile.close()  

reportFile=open(outputFolder+"allScores_healthy.txt",'w')
reportFile.write("subjectId\tage\tgender\tsimilarity1\tEF1\tPSI1\tVL1")
for i in range(12,len(subjectsInfoHealthy.dtype.names)):
    reportFile.write("\t%s" %subjectsInfoHealthy.dtype.names[i])
reportFile.write("\n")
for i in range(len(subjectsInfoHealthy)):
    reportFile.write("%s\t%d\t%s\t%f\t%f\t%f\t%f" % (subjectsInfoHealthy['subjectId'][i],subjectsInfoHealthy['age'][i],subjectsInfoHealthy['gender'][i],scores[i], subjectsInfoHealthy['EF'][i],subjectsInfoHealthy['PS'][i],subjectsInfoHealthy['VL'][i]))
    for j in range(12,len(subjectsInfoHealthy.dtype.names)):
        featureName=subjectsInfoHealthy.dtype.names[j]
        reportFile.write("\t%f" %subjectsInfoHealthy[featureName][i])
    reportFile.write("\n")
reportFile.close()  