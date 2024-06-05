from datetime import date
from datetime import datetime
import logging
import shutil
import argparse

scriptDescription = "Script Will Sort files in specified --PATH and Sort Files into Preset Folder Types. Setting --DELETE to TRUE will remove originals."
import os

parser = argparse.ArgumentParser(description=scriptDescription)
parser.add_argument('-p','-P','--PATH', '--path', action="store", dest='path', default=0, help='STRING: provide full path to the downloads (or any) folder to be sorted by types')
parser.add_argument('-d','-D','--DELETE','--delete', action="store", dest='delete', default=False, help='BOOLEAN: Specify if original files are to be deleted after sorting, False By Default')
args = parser.parse_args()

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

DOWNLOADS_DIR = args.path
FOLDER_TYPES = ["Text Files", "Images", "PDFs", "Executables", "Compressed", "Misc and Unsorted"]


## Get List of all The Files
def findFileNames():
	files = [f for f in os.listdir(DOWNLOADS_DIR) if os.path.isfile(os.path.join(DOWNLOADS_DIR, f))]	
	logger.info("Filenames Are added to the List")
	return files

## Sorting files in the Dictionary
def sortFiles(fileList):
	for file in fileList:
		name, extension = os.path.splitext(file)
		if extension.strip('.') in filesTypes:
			filesDict[extension.strip('.')].append(file)
		else:
			filesDict["misc"].append(file)

## Creates SunFolders inside new Destination Folder
def createSubFolders(sortedDir):
	for folder in FOLDER_TYPES:
		path = os.path.join(sortedDir, folder)
		os.mkdir(path)
		logger.info("Folder {} created".format(folder))

## Deletes Original Files if --delete set to TRUE
def deleteFiles():
	if args.delete:
		for item in findFileNames():
			logger.info("Deleting File: {}".format(item))
			os.remove(os.path.join(DOWNLOADS_DIR, item))
	else:
		logger.info("NO FILES WERE DELETED")

		
## Sorts and Copies files into new Folders				
def copyFilesToNewDir():
	newDirName = ("SortedFiles ")
	path = os.path.join(DOWNLOADS_DIR, newDirName)
	dateandtime = datetime.now()
	path = path + (dateandtime.strftime("%Y-%m-%d-%H-%M-%S"))
	os.mkdir(path)
	createSubFolders(path)

	for key in filesDict:
		tempList = filesDict[key]
		for item in tempList:
			src = os.path.join(DOWNLOADS_DIR, item)
			if key == "txt":
				dest = os.path.join(path, FOLDER_TYPES[0])
				logger.info("Copying {} files to {}".format(item, dest))
				shutil.copy(src, dest)
			if key == "jpg" or key == "jpeg" or key == "png":
				dest = os.path.join(path, FOLDER_TYPES[1])
				logger.info("Copying {} files to {}".format(item, dest))
				shutil.copy(src, dest)
			if key == "pdf":
				dest = os.path.join(path, FOLDER_TYPES[2])
				logger.info("Copying {} files to {}".format(item, dest))
				shutil.copy(src, dest)
			if key == "exe":
				dest = os.path.join(path, FOLDER_TYPES[3])
				shutil.copy(src, dest)
			if key == "rar" or key == "zip":
				dest = os.path.join(path, FOLDER_TYPES[4])
				logger.info("Copying {} files to {}".format(item, dest))
				shutil.copy(src, dest)
			if key == "misc":
				dest = os.path.join(path, FOLDER_TYPES[5])
				logger.info("Copying {} files to {}".format(item, dest))
				shutil.copy(src, dest)

	
sortFiles(findFileNames())
copyFilesToNewDir()
deleteFiles()