# File : main.py
# Created by gabys
# Date : 7/09/2018
# License : Apache 2.0

# Importing Python libraries
import os
import sys
import urllib.request

# Importing API classes
from api import *

# CONFIGURATION : Configure your script here
steam_key = ''  # Your Steam API key
github_key = ''  # Your Github API key
gmad = ''  # Your path to gmad.exe
gmpublish = ''  # Your path to gmpublish.exe


def create_ws_archive(base_path) -> None:
    """
    Create a workshop archive (.gma file) in the path "base_path"
    Returns:
        None: Nothing
    """
    full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + base_path
    status = os.system(gmad + ' create -folder ' + full_path + ' -out ' + full_path)
    if status != 0:
        raise Exception('The GMA process ended with an error.')


def update_ws_item(gma_path, file_id, changes) -> None:
    """
    Update a workshop item (with id "file_id" using gmpublish.exe
    Returns:
        None: Nothing
    """
    full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + gma_path
    status = os.system(
        gmpublish + ' update -addon "' + full_path + '" -id "' + file_id + '" -changes "' + changes + '"')
    if status != 0:
        raise Exception('The GMPUBLISH process ended with an error.')


# Main function
def main():
    if len(sys.argv) < 3:
        raise Exception('Missing arguments.')

    app_id = str(sys.argv[1])  # Steam app ID
    file_id = str(sys.argv[2])  # Steam Workshop file ID
    repo_name = str(sys.argv[3])  # Github repository name format : <owner/name>

    # Since we're just supporting Github and Steam, don't need to do any check on which to use
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
