# File : main.py
# Created by gabys
# Date : 7/09/2018
# License : Apache 2.0

# Importing Python libraries
import argparse

# Importing API classes
from api import *
# Importing GAME classes
from game import *

# CONFIGURATION : Configure your script here
steam_key = ''  # Your Steam API key

# SUPPORTED
# Supported games
supported_games = {
    'gmod': Gmod
}

# Supported hosts
supported_hosts = {
    'github': Github
}


def get_arguments():
    """
    Creates a new ArgumentParser and returns the given arguments in a Namespace
    Returns:
        Namespace: arguments
    """
    parser = argparse.ArgumentParser(prog="gSynch",
                                     description="gSynch allow you to synchronise your Git code with the Steam Workshop")

    # Action group : what the user wants to do ?
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--build', action="store", metavar="<executable>",
                         help="Builds the workshop item with the given executable")
    actions.add_argument('--update', action="store", metavar="<item>",
                         help="Update the given workshop item to the Workshop")
    actions.add_argument('--synch', action="store", nargs=2, metavar=("<executable>", "<item>"),
                         help="Builds the workshop item with the given executable and push "
                              "it to the workshop")
    # Steam related things
    steam = parser.add_argument_group(title="Steam Workshop file and application IDs")
    steam.add_argument('--file', help="Workshop file unique identifier.", required=True)
    steam.add_argument('--app', help="Steam Application unique identifier.", required=True)

    parser.add_argument("--host", action="store", help="Link to your repository", required=True)

    # TODO : Add an argument for directly supported games such as Garry's Mod

    return parser.parse_args()


# Main function
def main():
    arguments = get_arguments()

    host = supported_hosts.get(arguments.host, helper.launch_exception("The specified host isn't supported"))()

    # TODO : Refactor this code and make it compatible with the new classes

    """    
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
    """


# Script entry point
if __name__ == '__main__':
    main()
