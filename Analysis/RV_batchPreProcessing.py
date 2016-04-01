# -*- coding: utf-8 -*-
"""
Batch pre-processing of "rat videogame" sessions (with Bonsai)

@author: Adam
"""
import os
import subprocess
import sys

# Specify the folder list file
folderListFile = r'D:/Repositories/Rat_Videogame/Analysis/Folder Lists/GenericFolderList.txt'

# Specify relevant  Paths
bonsaiPath = r'C:\Users\IntelligentSystems\AppData\Local\Bonsai\Bonsai64.exe'
#bonsaiPath = r'C:\Users\Lory\AppData\Local\Bonsai\Bonsai64.exe'???
workflowPath = r'D:/Repositories/Rat_Videogame/Analysis/RV_preProcessing.bonsai'

# Read the folder list file
folderFile = open(folderListFile, "r")
folderList = folderFile.readlines()
folderFile.close()

# Go through every "session" folder and pre-process the IR video
for subjectFolder in folderList:
    sessionFolders = os.listdir(subjectFolder.rstrip('\n'))
    for sessionFolder in sessionFolders:            
        try:
            # Remove whitespace from string
            sessionFolder = sessionFolder.strip()
            sessionFolder = os.path.join(subjectFolder.rstrip('\n'),
                                         sessionFolder)
                                         
            # Generate analysis folder
            analysisFolder = os.path.join(sessionFolder, 'Analysis')
            if not os.path.exists(analysisFolder):
                os.mkdir(analysisFolder)
            else:
                print "Skipped... folder already exists!"
                continue
        
            # Report progress
            print "Analyzing " + sessionFolder + "!"
            sys.stdout.flush()
            
            # Create the Bonsai command line params
            moviePath  = r'IR.avi'
            argFilePath = r'-p:FileName='  + moviePath
        
            # Run Bonsai (in Session Folder) with command line Args
            os.chdir(sessionFolder)
            print moviePath
            subprocess.call([bonsaiPath, workflowPath, argFilePath, r'--noeditor'])
        except Exception as e:
            print e.__doc__
            print e.message
            continue
    
print "Done!!"
# FIN

for subjectFolder in folderList:
    sessionFolders = os.listdir(subjectFolder.rstrip('\n'))
    for sessionFolder in sessionFolders:
        print sessionFolder
