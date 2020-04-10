# File : steam.py
# Created by gabys
# Date : 10/04/2020
# License : Apache 2.0
import os

if not os.name == "posix":
    import winreg # assure portability


class Steam:
    steam_path: str
    games_path: list

    def __init__(self, steam_path=""):
        if not os.name == "posix":
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
            self.steam_path = steam_path
        self.games_path = [
            self.steam_path + "\\steamapps"
        ]
        # Check if there is other library directories
        # TODO : parse libraryfolders.vdf with steamfiles lib (but we need to wait the maintener to accept the pull request)

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
        :param app_id:
        :return:
        """
        for path in self.games_path:
            for file in os.listdir(path):
                if os.path.isfile((os.path.join(path, file))):
                    if app_id in file:
                        if os.path.splitext(file)[1] == ".acf":
                            pass # parse .acf file to find the
        return path