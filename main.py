#~-~-~-~-~-~-~-~-~-~-~-~-~-#
#          gSync           #
#    Gabriel Santamaria    #
#        Apache 2.0        #
#~-~-~-~-~-~-~-~-~-~-~-~-~-#

#--------------------#
#      IMPORTS       #
#--------------------#
import json, requests
import sys, os
import urllib.request
import datetime
#--------------------#
#   CONFIGURATION    #
#--------------------#
steam = '13C34ABF0073127B1904B632B7391356' # Your Steam API key
github = 'e932228baa42d68c35368dfa7a24fecd8a0b4095' # Your Github API key

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

def createDirectory(dname):
    if not os.path.exists(dname):
        os.makedirs(dname)

def createEmptyFile(fname, relativeDir):
    open(relativeDir + '/' + fname, 'w').close()

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

    print('Preparing the download...')
    createDirectory('tmp')
    createEmptyFile(data['name'], 'tmp')

    t = datetime.datetime.now().timestamp()
    print('Starting to download the latest release of https://github.com/' + repoName + ' ... ...')
    urllib.request.urlretrieve(data['downloadUrl'], 'tmp/' + data['name'])
    print('Download finished with success. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')



Main()