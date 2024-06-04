import re
import os
from datetime import date

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

DOWNLOADS_DIR = "C:/Users/XIII/Downloads" ## TODO Change to Universal Later

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
				
def copyFilesToNewDir():
	newDirName = ("SortedFiles " + str(date.today()))
	path = os.path.join(DOWNLOADS_DIR, newDirName)
	if os.mkdir(path):
		print ("Path Created")
	else:
		print("Error Occured Creating a Folder")
	
	
	
copyFilesToNewDir()