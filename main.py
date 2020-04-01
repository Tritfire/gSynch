# File : main.py
# Created by gabys
# Date : 7/09/2018
# License : Apache 2.0

# Importing Python libraries
import sys
import urllib.request

# Importing API classes
from api import *
# Importing GAME classes
from game import *

# CONFIGURATION : Configure your script here
steam_key = ''  # Your Steam API key
github_key = ''  # Your Github API key

# SUPPORTED
# Supported games
supported_games = {
    'gmod': Gmod
}

# Supported hosts
supported_hosts = {
    'github': Github
}


# Main function
def main():
    if len(sys.argv) < 3:
        raise Exception('Missing arguments.')

    app_id = str(sys.argv[1])  # Steam app ID
    file_id = str(sys.argv[2])  # Steam Workshop file ID
    repo_name = str(sys.argv[3])  # Github repository name format : <owner/name>

    host = supported_hosts.get(user_host, helper.launch_exception)()

    steam = Steam(steam_key, app_id, file_id)
    github = Github(github_key, repo_name)

    if helper.check_times(steam, github):
        print('Everything is up to date. Your workshop file has already been synchronized with your Github repository.')
        return 0

    data = github.get_release_data()

    # Checking & creating /tmp/ directory + creating the empty file
    print('Preparing the download...')
    helper.create_directory('tmp')
    helper.create_empty_file(data['name'], 'tmp')

    # Downloading and writing the file into the previously created empty file
    t = datetime.datetime.now().timestamp()
    print('Starting to download the latest release of https://github.com/' + repo_name + ' ... ' + str(
        data['size']) + ' ...')
    urllib.request.urlretrieve(data['downloadUrl'], 'tmp/' + data['name'])
    print('Download finished with success. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    # Unzipping the downloaded file
    t = datetime.datetime.now().timestamp()
    print('Starting to unzip : /tmp/' + data['name'] + '...')
    helper.unzip('tmp', data['name'])
    print('Uncompress finished with success. It took : ' + str(datetime.datetime.now().timestamp() - t) + ' seconds')

    # Clearing the useless files from the folder (like .zip, LICENCE, .gitattributes, README.md, etc...) [WE EXCLUDE
    # .JSON FILES FROM DELETION]
    print('Deleting useless files ...')
    helper.clear_directory('tmp')

    # Creating the .gma archive
    t = datetime.datetime.now().timestamp()
    print('Starting to create the .gma archive...')
    base_name = helper.get_base_directory()
    create_ws_archive(base_name)
    gma_name = base_name + '.gma'
    print('The .gma archive has been correctly created. It took : ' + str(
        datetime.datetime.now().timestamp() - t) + ' seconds')

    # Updating the Workshop item
    t = datetime.datetime.now().timestamp()
    print('Starting to update the .gma archive...')
    update_ws_item(gma_name, steam.file_id, data['body'])
    print('The gma archive has been correctly uploaded to the Workshop. It took : ' + str(
        datetime.datetime.now().timestamp() - t) + ' seconds')

    return 0


# Script entry point
if __name__ == '__main__':
    main()
