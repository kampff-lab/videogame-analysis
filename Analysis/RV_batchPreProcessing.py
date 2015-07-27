# -*- coding: utf-8 -*-
"""
Batch pre-processing of "rat videogame" sessions (with Bonsai)

@author: Adam
"""
import os
import subprocess
import sys

# Specify the folder list file
folderListFile = 'C:/repositories/Rat Videogame/Analysis/Folder Lists/GenericFolderList.txt'

# Specify relevant  Paths
bonsaiPath = r'C:\Users\Adam\AppData\Local\Bonsai\Bonsai64.exe'
#bonsaiPath = r'C:\Users\Lory\AppData\Local\Bonsai\Bonsai64.exe'???
workflowPath = r'C:/repositories/Rat Videogame/Analysis/RV_preProcessing.bonsai'

# Read the folder list file
folderFile = open(folderListFile, "r")
folderList = folderFile.readlines()
folderFile.close()

# Go through every "session" folder and pre-process the IR video
for sessionFolder in folderList:

    # Remove whitespace from string
    sessionFolder = sessionFolder.strip()

    # Report progress
    print "Analyzing " + sessionFolder + "!"
    sys.stdout.flush()
    
    # Create the Bonsai command line params
    moviePath  = sessionFolder+ r'\IR.avi'
    argFilePath = r'-p:FileName='  + moviePath

    # Run Bonsai (in Session Folder) with command line Args
    os.chdir(sessionFolder)
    subprocess.call([bonsaiPath, workflowPath, argFilePath, r'--noeditor'])
    
print "Done!!"
# FIN