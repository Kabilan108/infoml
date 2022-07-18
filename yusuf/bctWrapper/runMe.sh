#!/bin/bash
# sample: ./runMe.sh 

experimentPath=.
samplePath=$experimentPath/src/subjects.txt
measuresList=$experimentPath/src/featureList.txt
connectomesFolder=$experimentPath/connectomes

systemMaps=$experimentPath/src/11System_in_Desikan86.txt
hemisphereMaps=$experimentPath/src/hemisphereMaps_Desikan86.txt
numNodes=86


bct_features_py=./scripts/bct_features.py


if [[ ! -e $measuresList ]]; then
	python $bct_features_py --printFullMeasureList > $measuresList
	echo "Features list file is not found!! A full features lits is generated in $measuresList . Check the file and rerun this script to generate features for connectomes. Exiting..."
	exit 1
fi

mkdir -p $experimentPath/features

python $bct_features_py --measuresList $measuresList --connectomesFolder $connectomesFolder/ --subjectsList $samplePath --systemMaps $systemMaps --hemisphereMaps $hemisphereMaps --outputFolder $experimentPath/features/ --numNodes $numNodes --verbose --normalizeConnectomes none


