import sys
import os
import requests
import shutil
import stat
import json
from git import Repo

#	getArgs
#
#	Gets given arguments
#	Return given arguments (except the filename)
def getArgs():
	arguments = sys.argv[1:] # Skip the first argument

	return arguments

#	removeReadOnly
#
#	Prevent shutil.rmtree from "Access Denied" error, by removing file read-only property
def removeReadOnly(func, path, excinfo):
	os.chmod(path, stat.S_IWRITE)
	func(path)

#	checkFolder
#
#	Check if the <current_dir>/tmp directory exists or not
#	Delete the /tmp folder if exists
def checkFolder(tmp):
	if os.path.isdir(tmp):
		print("WARNING : /tmp file exists, deleting it.")
		shutil.rmtree(tmp, onerror=removeReadOnly)
		print("Done !")
	else:
		print("Everything is correct with the directory.")

#	gitClone
#
#	Simply clone the repositery given in argument
def gitClone(git_url, path):
	git_path = path + "/git"
	print("Cloning Git repositery...")
	Repo.clone_from(git_url, git_path)
	print("Done !")

#	workshopDownload
#
#	Download the .gma file using the Steam API. Learn more : https://lab.xpaw.me/steam_api_documentation.html#ISteamRemoteStorage_GetPublishedFileDetails_v1
def workshopDownload(item_id, path):
	ws_path = path + "/ws/"
	api = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
	r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data={'itemcount' : 1, 'publishedfileids[0]': item_id})

	if r.status_code != 200:
		print("ERROR : A problem occured when trying to get download URL of .gma.")
		return False

	data = json.loads(r.text) # JSON to Python list
	data = data['response']['publishedfiledetails']
	
	for value in data:
		try:
			filename = value["publishedfileid"]
			app_id = value['creator_app_id']
			url = value['file_url']
		except Exception as e:
			print("ERROR : ", e)
			print("We can't find the addon .gma URL, please try again.") # There's always a file ID

			return False

	if not app_id or app_id != 4000:
		print("ERROR: This is not a GMod addon, please retry.")
		return False

	print("Downloading .gma file from Steam Workshop...")
	gma_file = requests.get(url, stream = True)
	if gma_file.status_code != 200:
		print("ERROR : A problem occured when downloading .gma.")
		return False

	if not os.path.exists(ws_path):
		os.makedirs(ws_path)

	with open(ws_path + filename + ".gma", 'wb') as f:
		gma_file.raw.decode_content = True
		shutil.copyfileobj(gma_file.raw, f)

	print("Done !")

	return True

#	Downloads
#
#	Download all required files
def Downloads():
	arguments = getArgs()
	tmp = os.path.dirname(os.path.realpath(__file__)) + "/tmp"

	checkFolder(tmp)

	gitClone(arguments[0], tmp)
	# Now the repo is cloned, we can download workshop files

	error = workshopDownload(1308262997, tmp)
	if not error:
		return

	print("All files are downloaded in the temporary directory (<__file_directory__/tmp).")

#	extractWorkshop
#
#	Extract the files contained in the .gma archive
def extractWorkshop()
	# todo