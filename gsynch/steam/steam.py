# File : steam.py
# Created by gabys
# Date : 10/04/2020
# License : Apache 2.0
import os
import winreg


class Steam:
    steam_path: str
    games_path: str

    def __init__(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steams")
        except FileNotFoundError:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam")
            except FileNotFoundError as e:
                print("gSynch can't find your Steam installation")
                raise e
        self.steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        self.games_path = self.steam_path + "\steamapps"

    def is_installed(self, app_id):
        """
        Check if a game is installed
        Args:
            app_id: Game's steam id

        Returns:
            bool: whether the game is installed or not
        """
        # Get all the application manistests from Steam
        manifests = [file for file in os.listdir(self.games_path) if
                     os.path.isfile(os.path.join(self.games_path, file))]
        # TODO : Check if the app_id is contained in the manifests files
