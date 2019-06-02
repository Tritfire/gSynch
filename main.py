#~-~-~-~-~-~-~-~-~-~-~-~-~-#
#          gSync           #
#    Gabriel Santamaria    #
#        Apache 2.0        #
#~-~-~-~-~-~-~-~-~-~-~-~-~-#

#--------------------#
#      IMPORTS       #
#--------------------#
import json
import requests
import datetime
import sys
#--------------------#
#   CONFIGURATION    #
#--------------------#
steam = '' # Your Steam API key
github = '' # Your Github API key

#------------------------------#
#                              #
#       HELPERS FUNCTIONS      #
#                              #
#------------------------------#
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

def getGithubReleaseText(key, repoName):
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

    return {
        'downloadUrl': downloadUrl,
        'body': data['body']
    }

#--------------------#
#        MISC        #
#--------------------#
def checkTimes(steamKey, appid, fileid, githubKey, repoName):
    return getSteamLastUpdateTime(steamKey, appid, fileid) == getGithubLastUpdateTime(githubKey, repoName)

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
        return True