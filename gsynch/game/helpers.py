# File : helpers.py
# Created by gabys
# Date : 30/03/2020
# License : Apache 2.0
import os


def gmod_get_base_directory(path: str) -> str:
    """
    Gets the Garry's Mod add-on base directory
    Returns:
        str: Returns the base directory of the add-on
    """
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
    directories = [f.path for f in os.scandir(path) if f.is_dir()]
    for p in directories:
        if os.path.isdir(os.path.join(path, p)):
            i = i + 1
    if i > 1:
        return 'tmp'
    else:
        if directories[0] in blacklist:
            return path
        else:
            return directories[0]
