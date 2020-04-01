# File : helper.py
# Created by gabys
# Date : 30/03/2020
# License : Apache 2.0
import os
import zipfile


def is_zip(file_type) -> bool:
    """
    Check if the given file is a ZIP
    Returns:
        bool: Whether it's a ZIP file or not
    """
    mimes = {
        'application/zip',
        'application/octet-stream',
        'application/x-zip-compressed',
        'multipart/x-zip'
    }
    for v in mimes:
        if v == file_type:
            return True
    return False


def unzip(path, file_name) -> None:
    """
    Unzip a ZIP file
    Returns:
        None: Nothing
    """
    if not os.path.isfile(path + '/' + file_name):
        raise Exception(
            'A problem occurred while trying to unzip the file archive : file do not exists nor is a valid one.')
    f = zipfile.ZipFile(path + '/' + file_name, 'r')
    f.extractall(path)
    f.close()


def check_times(to_update, reference) -> bool:
    """
    Check if there is a difference between update times
    Returns:
        bool: Whether or not the first
    """
    return to_update.get_last_update() >= reference.get_last_update()


def create_directory(directory_name) -> None:
    """
    Create a directory called "directory_name"
    Returns:
        None: Nothing
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def create_empty_file(file_name, relative_directory) -> None:
    """
    Creates an empty file in the relative directory "relative_directory"
    Returns:
        None: Nothing
    """
    open(relative_directory + '/' + file_name, 'w').close()


# TOOK & ADAPTED FROM THIS POST :
# https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
def clear_directory(folder) -> None:
    """
    Clear a particular directory of his files
    Returns:
        None: Nothing
    """
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            _, ext = os.path.splitext(path)
            if os.path.isfile(path) and ext != '.json':
                os.unlink(path)
        except Exception as e:
            print(e)


def get_base_directory() -> str:
    """
    Gets the base directory of the add-on we work on
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


def launch_exception(message: str) -> None:
    """
    Launch an exception with a message "message"
    Args:
        message: Exception message

    Returns:
        None: Nothing
    """
    raise Exception(message)
