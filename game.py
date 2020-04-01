# File : game.py
# Created by gabys
# Date : 31/03/2020
# License : Apache 2.0

import abc
import os


class GAME(metaclass=abc.ABCMeta):
    app_id = ""

    def __init__(self, app_id):
        self.app_id = app_id

    @abc.abstractmethod
    def create_ws_item(self, base_path) -> None:
        """
        Creates an uploadable file / folder (depending on the game method to handle WS files)
        Args:
            base_path: Base path of the item

        Returns:
            None: Nothing

        """
        pass

    @abc.abstractmethod
    def update_ws_item(self, file_id, changes) -> None:
        """
        Update a workshop item (depending on the game method to handle WS files uploading)
        Args:
            changes (str): What has been changed in the update
            file_id (str): the Workshop file id that has to be updated

        Returns:
            None: Nothing
        """
        pass


class Gmod(GAME):
    gmad: str = ""
    gmpublish: str = ""

    def __init__(self, app_id, gmad, gmpublish):
        super().__init__(app_id)
        self.gmad = gmad
        self.gmpublish = gmpublish

    def create_ws_item(self, base_path):
        """
        Create a workshop archive (.gma file) in the path "base_path"
        Returns:
            None: Nothing
        """
        full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + base_path
        status = os.system(self.gmad + ' create -folder ' + full_path + ' -out ' + full_path)
        if status != 0:
            raise Exception('The GMA process ended with an error.')

    def update_ws_item(self, file_id, changes) -> None:
        """
        Update a workshop item (with id "file_id" using gmpublish.exe
        Returns:
            None: Nothing
        """
        full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + self.gmad
        status = os.system(
            self.gmpublish + ' update -addon "' + full_path + '" -id "' + file_id + '" -changes "' + changes + '"')
        if status != 0:
            raise Exception('The GMPUBLISH process ended with an error.')
