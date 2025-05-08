from datetime import date
from datetime import datetime
import logging
import shutil
import argparse
import os

scriptDescription = "Script Moves CC/Mods from Directory to Sims4 Mods Folder REQUIRED args: USER, PATH"


parser = argparse.ArgumentParser(description=scriptDescription)
parser.add_argument('-u','-U','--USER', '--user', action="store", dest='user', default=0, help='STRING: User Name of the account Ex: -U testUser')
parser.add_argument('-p','-P','--PATH', '--path', action="store", dest='path', default=0, help='STRING: provide full path to the CC/Mods Folder Ex: --PATH C:/AllModsFolder')
parser.add_argument('-r','-r','--REMOVE','--remove', action="store_true", dest='remove', default=False, help='BOOLEAN: Specify if original files are to be deleted after copying, False By Default EX: -r')
parser.add_argument('-d', '-D', '--DRIVE', '--drive', action="store", dest='drive', default="C:\\", help='STRING: Specify drive Location of the Installation Ex: --DRIVE C')
parser.add_argument('-o', '-O', '--OVERWRITE', '-overwrite', action="store_true", dest='overwrite', default=False, help="BOOLEAN: If Set To True Will OVERWRITE existing files in DESTINATION PATH, False by Default, EX: -o")
parser.add_argument('--DRY_RUN', action="store_true", dest='dry_run', default=False, help="BOOLEAN: If Set To True, the operation will only be simulated")


args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

DRIVE = args.drive
USERNAME = args.user
SRC_MODS_FOLDER = args.path
DEST_MODS_PATH = ""
OVERWRITE = args.overwrite
DELETE = args.remove
DRY_RUN = args.dry_run  # Flag to simulate the operation



def setModsFolder(usersname):
	global DEST_MODS_PATH
	mod_loc = "Documents\\Electronic Arts\\The Sims 4\\Mods"
	if USERNAME == 0:
		print("USERNAME is NOT Defined: USE --USER to Specify User Name, USE --help FOR MORE INFORMATION")
		exit()
	else:
		DEST_MODS_PATH = os.path.join(DRIVE, "Users", usersname ,mod_loc)
		logger.info("Mods will be Moved to: {}".format(DEST_MODS_PATH))

def checkAllArgs():
	user = False
	src_mods = False
	dest_mods = False
	if DRY_RUN:
		logger.info("RUNNING IN DRY_RUN MODE -- \"dest_mods\" ARGS FORCED TO TRUE")
		dest_mods = True
	#Checks if SRC_MODS_FOLDER Exists
	if SRC_MODS_FOLDER != 0:
		if os.path.exists(SRC_MODS_FOLDER):
			logger.info("SRC_MODS_FOLDER Found at {}".format(SRC_MODS_FOLDER))
			src_mods = True
	else:
		logger.info("SRC_MODS_FOLDER Not Found or Specified. USE --help FOR MORE INFORMATION")

	#Checks if USERNAME Defined
	if USERNAME != 0:
		logger.info("USERNAME Defined as: {}".format(USERNAME))
		user = True
		#Checks if path exists if USER NAME EXISTS
		if os.path.exists(DEST_MODS_PATH):
			logger.info("Destination MODS Folder: {}".format(DEST_MODS_PATH))
			dest_mods = True
		else:
			logger.error("SIMS4 Mods Path Not Found")
	else:
		logger.error("USERNAME Was Not Defined")

	#Verify All Required Items are Entered
	if user and src_mods and dest_mods: 
		logger.info("All Required Fields are Valid")
		#Verify Overwrite
		if OVERWRITE:
			check = input("ATTENTION THIS WILL OVERWRITE EXISTING FILES \nDO YOU WANT TO CONTINUE? [y/n]").strip().lower()
			if check == 'n' or check == 'y':
				if check == 'n':
					print("Exiting Script")
					exit()
				else:
					print("Response Confirmed. Existing Files Will be OVERWRITTEN")
			else:
				print("Invalid Response. Exiting.")
				exit()
		#Verify DELETE
		if DELETE:
			check = input("ATTENTION THIS WILL DELETE SOURCE FILES \nDO YOU WANT TO CONTINUE? [y/n]").strip().lower()
			if check == 'n' or check == 'y':
				if check == 'n':
					print("Exiting Script")
					exit()
				else:
					print("Response Confirmed. Source Files Will be DELETED")
			else:
				print("Invalid Response. Exiting.")
				exit()

		return True
	else:
		if not DRY_RUN:
			logger.error("One or More of the Required Fields is Invalid. CHECK ABOVE")
			return False
		else:
			logger.info("RUNNING IN DRY_RUN MODE -- \"CheckAllArgs\" FORCED TO TRUE")
			return True

#Moves All The Mods
def moveAllMods():
    if not checkAllArgs():
        logger.error("Invalid input arguments. Exiting script.")
        exit()

    if DRY_RUN:
    	logger.info("RUNNING IN DRY_RUN MODE")

    logger.info("Starting to move mods...")

    # Iterate over all items in the source directory
    for item in os.listdir(SRC_MODS_FOLDER):
        source_path = os.path.join(SRC_MODS_FOLDER, item)
        destination_path = os.path.join(DEST_MODS_PATH, item)

        # Check if file exists at destination, handle overwrite if needed
        if os.path.exists(destination_path):
            if OVERWRITE:
                if os.path.isdir(destination_path):
                    logger.info(f"Overwriting directory: {destination_path}")
                    if not DRY_RUN:
                        shutil.rmtree(destination_path)  # Actually delete the destination folder
                else:
                    logger.info(f"Overwriting file: {destination_path}")
                    if not DRY_RUN:
                        os.remove(destination_path)  # Actually delete the destination file
            else:
                logger.info(f"Skipping (already exists): {item}")
                continue

        # Copy item (file or directory)
        if os.path.isdir(source_path):
            logger.info(f"Copying directory: {item}")
            if not DRY_RUN:
                shutil.copytree(source_path, destination_path)  # Actually copy the directory
        else:
            logger.info(f"Copying file: {item}")
            if not DRY_RUN:
                shutil.copy2(source_path, destination_path)  # Actually copy the file

        # Optionally delete source files if REMOVE is True
        if DELETE:
            if not DRY_RUN:
                if os.path.isdir(source_path):
                    shutil.rmtree(source_path)  # Actually delete the source directory
                else:
                    os.remove(source_path)  # Actually delete the source file
            logger.info(f"Deleted source: {item}")






def runIt():
	setModsFolder(USERNAME)
	moveAllMods()

if __name__ == "__main__":
	runIt()

# TODO 
 


