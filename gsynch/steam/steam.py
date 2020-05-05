# File : steam.py
# Created by gabys
# Date : 10/04/2020
# License : Apache 2.0
import os
import subprocess
import sys
# steamfiles library, made by @leovp https://github.com/leovp/steamfiles
from steamfiles import acf

if os.name != "posix":
    import winreg  # assure portability


class NotFound(Exception):
    """
    This is raised when a required data isn't found by the system
    """
    pass


class Steam:
    steam_path: str
    games_path: list

    def __init__(self, steam_path=""):
        if os.name != "posix":
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steams")
            except FileNotFoundError:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam")
                except FileNotFoundError as e:
                    print("gSynch can't find your Steam installation")
                    raise e
            self.steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        else:
            whereis = subprocess.run(['whereis', 'steam'], stdout=subprocess.PIPE)
            self.steam_path = whereis.stdout.decode('utf-8')[7:]  # we get rid of "steam: " (which is 7 char long)
        self.games_path = [
            self.steam_path + "\\steamapps"
        ]
        # Check if there is other library directories (see "libraryfolders.vdf analysis.txt")
        try:
            with open(self.steam_path + "\\libraryfolders.vdf") as foldersfile:
                data = acf.load(foldersfile)
        except OSError as e:
            print("We can't figure out where the fuck is your libraryfolders.vdf file !"
                  f"Full error :\n {e}")
            sys.exit(-1)  # this is a fatal error
        except TypeError or ValueError as e:
            print(
                f"An error occurred while trying to parse {self.steam_path}\\libraryfolders.vdf. Please open an Issue "
                f"at https://github.com/Gabyfle/gSynch with your libraryfolders.vdf file !")
            sys.exit(-1)  # this is a fatal error
        finally:
            if foldersfile is not None:
                foldersfile.close()
        # Now check if the libraryfolders.vdf file is correct, and if he follow "libraryfolders.vdf analysis.txt" (if
        # not, abort)
        if not data["LibraryFolders"]:
            print(f"An error occurred while trying to use data from your libraryfolders.vdf file. Please report this "
                  f"to https://github.com/Gabyfle/gSynch in the Issue section, attaching your libraryfolders.vdf file.")
            sys.exit(-1)  # this is a fatal error
        else:
            for key in data["LibraryFolders"]:
                if key.isdigit():  # if the key is a digit, it's a path to a library folder
                    self.games_path.append(data["LibraryFolders"][key])
        # now we should have all the library path from the user's Steam installation

    def is_installed(self, app_id):
        """
        Check if a game is installed
        Args:
            app_id: Game's steam id

        Returns:
            bool: whether the game is installed or not
        """
        # Get all the application manifests from Steam and check if app_id is in the name of one file
        for path in self.games_path:
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    if app_id in file:
                        return True
        return False  # there is no file that contains app_id, the app isn't installed

    def get_install_path(self, app_id):
        """
        Get the installation path of the application "app_id"
        Args:
            app_id: Game's steam id

        Returns:
            str: path to the game
        """
        data = dict  # contains parsed data from appmanifest_id.acf files

        for path in self.games_path:
            for file in os.listdir(path):
                if os.path.isfile((os.path.join(path, file))):  # make sure this is a file and not a directory
                    if app_id in file:  # this file contains the application id of the requested app
                        if os.path.splitext(file)[1] == ".acf":  # make sure this is a manifest file
                            try:
                                with open(os.path.join(path, file)) as acf_file:
                                    data = acf.load(acf_file)
                            except OSError as e:
                                print(f"A problem occurred while trying to open {os.path.join(path, file)}. Make sure "
                                      f"gSynch has the permission to read this path!")
                                sys.exit(-1)  # this is a fatal error
                            except TypeError or ValueError as e:
                                print(
                                    f"An error occurred while trying to parse {os.path.join(path, file)}. Please open "
                                    f"an Issue "
                                    f"at https://github.com/Gabyfle/gSynch with {os.path.join(path, file)} attached!")
                                sys.exit(-1)  # this is a fatal error
                            finally:
                                if acf_file is not None:
                                    acf_file.close()
        if data is not None and data["installDir"] is not None:
            directory = data["installDir"]
        else:
            raise NotFound(f"Sorry, but gSynch can't find the app : {app_id}... Are you sure it's installed ?")
        return directory
