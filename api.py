# File : api.py
# Created by gabys
# Date : 30/03/2020
# License :

import abc
import datetime
import json

import requests

import helper as helper


class API(metaclass=abc.ABCMeta):
    api_key: str = ""

    def __init__(self, api_key):
        self.api_key = api_key

    @abc.abstractmethod
    def get_last_update(self) -> int:
        """ Gets the last update time

        Returns:
            int: Date in timestamp format
        """
        pass


class Steam(API):
    app_id: str = ""
    file_id: str = ""

    def __init__(self, api_key, app_id, file_id):
        super().__init__(api_key)

    def get_last_update(self):
        base_url = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
        parameters = {
            'key': self.api_key,
            'app_id': self.app_id,
            'publishedfileids[0]': self.file_id,
            'itemcount': 1
        }
        r = requests.post(url=base_url, data=parameters)
        data = json.loads(r.text)
        try:
            data['response']['publishedfiledetails'][0]['time_updated']
        except NameError:
            raise Exception('Can\'t get the latest update time of the following WS item ' + self.file_id)

        time = data['response']['publishedfiledetails'][0]['time_updated']
        return time


class Github(API):
    repository_name: str = ""
    base_url: str = ""

    def __init__(self, api_key, repository_name):
        super().__init__(api_key)
        self.repository_name = repository_name
        self.base_url = 'https://api.github.com/repos/' + self.repository_name + '/releases/latest?access_token=' + self.api_key

    def get_last_update(self):
        r = requests.get(self.base_url)
        data = json.loads(r.text)

        try:
            iso = datetime.datetime.strptime(data['published_at'], "%Y-%m-%dT%H:%M:%S%z")
        except NameError:
            raise Exception('Can\'t fetch any attached asset to the latest release of ' + self.repository_name)

        return iso.timestamp()

    def get_release_data(self):
        """
        Gets the latest release data from the Github website

        Returns:
            list:  A list containing the useful data

        """
        r = requests.get(self.base_url)
        data = json.loads(r.text)

        try:
            download_url = data['assets'][0]['browser_download_url']
        except NameError:
            raise Exception('Can\'t fetch any attached asset to the latest release of ' + self.repository_name)
        try:
            data['body']
        except NameError:
            raise Exception('An error occurred while trying to access to the latest release of ' + self.repository_name)

        if not helper.is_zip(data['assets'][0]['content_type']):
            raise Exception('The latest update asset isn\'t a valid ZIP file')

        return {
            'downloadUrl': download_url,
            'body': data['body'],
            'name': data['assets'][0]['name'],
            'size': data['assets'][0]['size']
        }
