import re
import os
from datetime import date
import logging

logger = logging.getLogger(__name__)
filesTypes = ["txt", "jpg", "jpeg", "pdf", "exe", "rar", "zip", "png"]
filesDict = {
			"txt": [],
			"jpg": [],
			"jpeg": [],
			"pdf": [],
			"exe": [],
			"zip": [],
			"rar": [],
			"png": [],
			"misc": []
}

#DOWNLOADS_DIR = "C:/Users/XIII/Downloads" ## TODO Change to Universal Later
DOWNLOADS_DIR = "C:/Users/nikit/Downloads"
FOLDER_TYPES = ["Text Files", "Images", "PDFs", "Executables", "Compressed", "Misc and Unsorted"]


## Get List of all The Files
def findFileNames():
	#files = os.listdir(DOWNLOADS_DIR)
	files = [f for f in os.listdir(DOWNLOADS_DIR) if os.path.isfile(os.path.join(DOWNLOADS_DIR, f))]	
	return files

## Sorting files in the Dictionary
def sortFiles(fileList):
	for file in fileList:
		for type in filesTypes:
			if (file.endswith(type)):
				filesDict[type].append(file)
			else:
				filesDict["misc"].append(file)

def createSubFolders(sortedDir):
	for folder in FOLDER_TYPES:
		path = os.path.join(sortedDir, folder)
		os.mkdir(path)
		logger.info("Folder {} created".format(folder))

				
def copyFilesToNewDir():
	newDirName = ("SortedFiles " + str(date.today()))
	path = os.path.join(DOWNLOADS_DIR, newDirName)
	#os.mkdir(path)
	#createSubFolders(path)

	for key in filesDict:
		if key == "txt":
			

	##TODO Create Folder for file Types
	##TODO Sort Files into Correct Folders
	
sortFiles(findFileNames())
copyFilesToNewDir()