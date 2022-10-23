from .picvt_base import PICVT
import re
import os
import json
import shutil
import requests


class API7BU():
    def __init__(self, token):
        self.token = 'Bearer ' + token

    def upload(self, files):
        url_upload = 'https://7bu.top/api/v1/upload'
        response = ""
        try:
            response = requests.post(url_upload, files=files, headers={
                'Accept': 'application/json',
                'Authorization': self.token})
        except Exception as e:
            print('get response error {} '.format(e))
            return None

        # assert data exist
        assert(json.loads(response.text)['data'])
        return json.loads(response.text)['data']


class Process(PICVT):
    def __init__(self, params=None):
        self.img_pattern = re.compile(r'^!\[.*', re.M)
        self.url_pattern = re.compile(
            r'(^//.|^/|^[a-zA-Z])?:?/.+(/$)?')
        self.api7bu = API7BU(params['to']['token'])

    def extract(self, content, params):
        url_list = []
        result = self.img_pattern.findall(content)
        for url in result:
            url = self.url_pattern.search(url)
            if url:
                url_list.append(url.group())
        return url_list

    def download(self, url, params):
        return True, url

    def upload(self, path, params):
        files = {
            'file': open(path, 'rb'),
        }
        response = self.api7bu.upload(files)
        if response is None:
            return False, None

        img_url = response['links']['url']
        return True, img_url
