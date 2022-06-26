from curses import delay_output
from traceback import print_tb
from leancloud import Object
from .picvt_base import PICVT
import re
import os
import json
import shutil
import requests


class API7BU(Object):
    def __init__(self, usr, passwd):
        self.usr = usr
        self.passwd = passwd
        self.init_token(usr, passwd)

    def __del__(self):
        self.del_token()

    def init_token(self, usr, passwd):
        url_token = 'https://7bu.top/api/v1/tokens'
        params = {'email': usr,
                  'password': passwd}
        response = requests.post(url_token, data=params, headers={
                                 'Accept': 'application/json'})
        # assert ready
        self.token = 'Bearer ' + json.loads(response.text)['data']['token']

    def del_token(self):
        url_token = 'https://7bu.top/api/v1/tokens'
        requests.delete(url_token, headers={'Accept': 'application/json',
                                            'Authorization': self.token})

    def upload(self, files):
        url_upload = 'https://7bu.top/api/v1/upload'
        response = ""
        try:
            response = requests.post(url_upload, files=files, headers={
                'Accept': 'application/json',
                'Authorization': self.token})
        except Exception as e:
            print('get response error {} retrying...'.format(e))
            self.del_token()
            self.init_token(self.usr, self.passwd)
            response = requests.post(url_upload, files=files, headers={
                'Accept': 'application/json',
                'Authorization': self.token})

        # assert data exist
        assert(json.loads(response.text)['data'])
        return json.loads(response.text)['data']


class Process(PICVT):
    def __init__(self, params=None):
        self.img_pattern = re.compile(r'^!\[.*', re.M)
        self.url_pattern = re.compile(
            r'(^//.|^/|^[a-zA-Z])?:?/.+(/$)?')
        self.api7bu = API7BU(params['to']['user'], params['to']['password'])

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
        img_url = response['links']['url']
        return True, img_url
