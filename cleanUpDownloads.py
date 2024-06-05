import re
import os
from datetime import date
import logging
import shutil


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
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
	logger.info("Filenames Are added to the List")
	return files

## Sorting files in the Dictionary
def sortFiles(fileList):
	for file in fileList:
		name, extension = os.path.splitext(file)
		#print(extension.strip('.'))
		if extension.strip('.') in filesTypes:
			print("Extension {}".format(extension))
			filesDict[extension.strip('.')].append(file)
		else:
			print("MISC EXTENSION FOUND")
			filesDict["misc"].append(file)

def createSubFolders(sortedDir):
	for folder in FOLDER_TYPES:
		path = os.path.join(sortedDir, folder)
		os.mkdir(path)
		logger.info("Folder {} created".format(folder))

def deleteFiles():
	for item in findFileNames():
		os.remove(os.path.join(DOWNLOADS_DIR, item))

				
def copyFilesToNewDir():
	newDirName = ("SortedFiles " + str(date.today()))
	path = os.path.join(DOWNLOADS_DIR, newDirName)
	os.mkdir(path)
	createSubFolders(path)

	print(filesDict["misc"])

	for key in filesDict:
		tempList = filesDict[key]
		for item in tempList:
			src = os.path.join(DOWNLOADS_DIR, item)
			if key == "txt":
				dest = os.path.join(path, FOLDER_TYPES[0])
				logger.info("Copying {} files to {}".format(key, dest))
				shutil.copy(src, dest)
			if key == "jpg" or key == "jpeg" or key == "png":
				dest = os.path.join(path, FOLDER_TYPES[1])
				logger.info("Copying {} files to {}".format(key, dest))
				shutil.copy(src, dest)
			if key == "pdf":
				dest = os.path.join(path, FOLDER_TYPES[2])
				logger.info("Copying {} files to {}".format(key, dest))
				shutil.copy(src, dest)
			if key == "exe":
				dest = os.path.join(path, FOLDER_TYPES[3])
				shutil.copy(src, dest)
			if key == "rar" or key == "zip":
				dest = os.path.join(path, FOLDER_TYPES[4])
				logger.info("Copying {} files to {}".format(key, dest))
				shutil.copy(src, dest)
			if key == "misc":
				dest = os.path.join(path, FOLDER_TYPES[5])
				logger.info("Copying {} files to {}".format(key, dest))
				shutil.copy(src, dest)





	##TODO Sort Files into Correct Folders
	
sortFiles(findFileNames())
copyFilesToNewDir()
#deleteFiles()