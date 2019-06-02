#~-~-~-~-~-~-~-~-~-~-~-~-~-#
#          gSync           #
#    Gabriel Santamaria    #
#        Apache 2.0        #
#~-~-~-~-~-~-~-~-~-~-~-~-~-#

#--------------------#
#      IMPORTS       #
#--------------------#
import json, requests
import sys, os, zipfile
import urllib.request
import datetime
#--------------------#
#   CONFIGURATION    #
#--------------------#
steam = '' # Your Steam API key
github = '' # Your Github API key
gmad = '' # Your path to gmad.exe
gmpublish = '' # Your path to gmpublish.exe

#------------------------------#
#                              #
#       HELPERS FUNCTIONS      #
#                              #
#------------------------------#
#--------------------#
#        MISC        #
#--------------------#
def checkTimes(steamKey, appid, fileid, githubKey, repoName):
    return getSteamLastUpdateTime(steamKey, appid, fileid) >= getGithubLastUpdateTime(githubKey, repoName)

def isZip(ftype):
    mimes = {
        'application/zip', 
        'application/octet-stream', 
        'application/x-zip-compressed', 
        'multipart/x-zip'
    }
    for v in mimes:
        if v == ftype:
            return True
    return False

def unZip(path, fname):
    if not os.path.isfile(path + '/' + fname):
        raise Exception('A problem occurred while trying to unzip the file archive : file do not exists nor is a valid one.')
    f = zipfile.ZipFile(path + '/' + fname, 'r')
    f.extractall(path)
    f.close()

def createDirectory(dname):
    if not os.path.exists(dname):
        os.makedirs(dname)

def createEmptyFile(fname, relativeDir):
    open(relativeDir + '/' + fname, 'w').close()

# TOOK & ADAPTED FROM THIS POST : https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
def clearDirectory(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            _, ext = os.path.splitext(path)
            if os.path.isfile(path) and ext != '.json':
                os.unlink(path)
        except Exception as e:
            print(e)

def getBaseDirectory():
    blacklist = {
        'maps',
        'backgrounds',
        'gamemodes',
        'materials',
        'lua',
        'scenes',
        'models',
        'scripts',
        'particles',
        'sound',
        'resource'
    }
    i = 0
    directories = [f.path for f in os.scandir('tmp') if f.is_dir()]
    for p in directories:
        if os.path.isdir(os.path.join('tmp', p)):
            i = i + 1
    if i > 1:
        return 'tmp'
    else:
        if directories[0] in blacklist:
            return 'tmp'
        else:
            return directories[0]

#--------------------#
#     STEAM PART     #
#--------------------#
def getSteamLastUpdateTime(key, appid, fileid):
    baseUrl = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
    parameters = {
        'key': key,
        'appid': appid,
        'publishedfileids[0]': fileid,
        'itemcount': 1
    }
    r = requests.post(url = baseUrl, data = parameters)
    data = json.loads(r.text)
    try:
        data['response']['publishedfiledetails'][0]['time_updated']
    except NameError:
        raise Exception('Can\'t get the latest update time of the following WS item ' + fileid)

    time = data['response']['publishedfiledetails'][0]['time_updated']
    
    return time

def createWorkshopArchive(path, basePath):
    fullPath = os.path.dirname(os.path.realpath(__file__)) + '/' + basePath
    status = os.system(gmad + ' create -folder ' + fullPath + ' -out ' + fullPath)
    if status != 0:
        raise Exception('The GMA proccess ended with an error.')

def updateWorkshopItem(gmaPath, fileId, changes):
    fullPath = os.path.dirname(os.path.realpath(__file__)) + '/' + gmaPath
    status = os.system(gmpublish + ' update -addon "' + fullPath + '" -id "' + fileId + '" -changes "' + changes + '"')
    if status != 0:
        raise Exception('The GMPUBLISH proccess ended with an error.')

#--------------------#
#    GITHUB  PART    #
#--------------------#
def getGithubLastUpdateTime(key, repoName):
    baseUrl = 'https://api.github.com/repos/' + repoName + '/releases/latest?access_token=' + key
    r = requests.get(baseUrl)
    data = json.loads(r.text)

    try:
        iso = datetime.datetime.strptime(data['published_at'], "%Y-%m-%dT%H:%M:%S%z")
    except NameError:
        raise Exception('Can\'t fetch any attached asset to the latest release of ' + repoName)

    return iso.timestamp()

def getGithubReleaseData(key, repoName):
    baseUrl = 'https://api.github.com/repos/' + repoName + '/releases/latest?access_token=' + key
    r = requests.get(baseUrl)
    data = json.loads(r.text)

    try:
        downloadUrl = data['assets'][0]['browser_download_url']
    except NameError:
        raise Exception('Can\'t fetch any attached asset to the latest release of ' + repoName)
    try:
        data['body']
    except NameError:
        raise Exception('An error occurred while trying to access to the latest release body of ' + repoName)

    if not isZip(data['assets'][0]['content_type']):
       raise Exception('The latest update asset isn\'t a valid ZIP file')
 

    return {
        'downloadUrl': downloadUrl,
        'body': data['body'],
        'name': data['assets'][0]['name'],
        'size': data['assets'][0]['size']
    }

#------------------------------#
#                              #
#         MAIN FUNCTION        #
#                              #
#------------------------------#
def Main():
    appid = str(sys.argv[1]) # Steam's APPID
    fileid = str(sys.argv[2]) # Steam's Workshop FILEID
    repoName = str(sys.argv[3]) # Github's repositery name FORMAT : <owner/name>

    if checkTimes(steam, appid, fileid, github, repoName):
        print('Everything is up to date. Your workshop file has already been synchronized with your Github repository.')
        return 0
    
    data = getGithubReleaseData(github, repoName)

    # Checking /tmp/ directory + creating the empty file
    print('Preparing the download...')
    createDirectory('tmp')
    createEmptyFile(data['name'], 'tmp')

    # Downloading and writing the file into the previously created empty file
    t = datetime.datetime.now().timestamp()
    print('Starting to download the latest release of https://github.com/' + repoName + ' ... ' + str(data['size']) + ' ...')
    urllib.request.urlretrieve(data['downloadUrl'], 'tmp/' + data['name'])
    print('Download finished with success. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    # Unzipping the downloaded file
    t = datetime.datetime.now().timestamp()
    print('Starting to unzip : /tmp/' + data['name'] + '...')
    unZip('tmp', data['name'])
    print('Uncompression finished with success. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    # Clearing the useless files from the folder (like .zip, LICENCE, .gitattributes, README.md, etc...) [WE EXCLUDE .JSON FILES FROM DELETION]
    print('Deleting useless files ...')
    clearDirectory('tmp')

    # Creating the .gma archive
    t = datetime.datetime.now().timestamp()
    print('Starting to create the .gma archive...')
    baseName = getBaseDirectory()
    createWorkshopArchive(gmad, baseName)
    gmaName = baseName + '.gma'
    print('The gma archive has been correctly created. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    # Updating the Workshop item
    t = datetime.datetime.now().timestamp()
    print('Starting to update the .gma archive...')
    updateWorkshopItem(gmaName, fileid, data['body'])
    print('The gma archive has been correctly uploaded to the Workshop. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    return 0

Main()