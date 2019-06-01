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
#--------------------#
#	CONFIGURATION	 #
#--------------------#
steam = '' # Your Steam API key
github = '' # Your Github API key

#--------------------#
#	  STEAM PART  	 #
#--------------------#
def getLastUpdateTime(key, appid, fileid):
    baseUrl = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
    parameters = {
        'key': key,
        'appid': appid,
        'publishedfileids[0]': fileid,
        'itemcount': 1
    }
    r = requests.post(url = baseUrl, data = parameters)
    data = json.loads(r.text)
    time = data['response']['publishedfiledetails'][0]['time_updated']
    if time is None:
        time = 0
    
    return time

#--------------------#
#	 GITHUB  PART  	 #
#--------------------#
