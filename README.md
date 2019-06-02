# gSynch
A Git / Steam Workshop addon synchronizer in Python

## Informations

This little Python script allows you to synchronize your addons quickly and easily. Based on the Git version manager, you just need to update your addon with Git to be updated on the Steam Workshop.

## How to use
To use this script, you must have a proper installation of Python 3.x on your system. Then, download the latest release (located in the releases tab of this repository) and put it in a random folder.

Before launching the script, you MUST configure it with your :
- **Steam API key** : https://steamcommunity.com/dev/apikey
- **A Github access token** : https://github.com/settings/tokens

Then, launch a command prompt inside this folder and launch this command : 
```sys
python main.py <appid> <fileid> <repoName>
```
