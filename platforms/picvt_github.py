from .picvt_base import PICVT
from github import Github
import os
import re


class Process(PICVT):
    def __init__(self):
        self.img_pattern = re.compile(r'https://cdn.jsdelivr.net/gh/.*', re.M)
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[a-zA-Z]|[0-9]')

    def extract(self, content):
        url_list = []
        result = self.img_pattern.findall(content)
        for url in result:
            url = self.url_pattern.search(url)
            if url:
                url_list.append(url.group())
        return url_list

    def upload(self, filepath, params):
        g = Github(params['token'])
        repo = g.get_repo(
            "{}/{}".format(g.get_user().login, params['config']['repo']))

        path = self._get_dict_value(params['config'], 'path', 'pictures')
        path = os.path.join(path, "{}".format(
            self._get_file_purename(filepath)))

        message = self._get_dict_value(
            params['config'], 'message', 'upload pictures by picvt')
        content = self._get_file_content(filepath)
        branch = self._get_dict_value(params['config'], 'branch', 'master')

        try:
            IDX = 0
            while True:
                repo.get_contents(path, ref=branch)
                path = self._get_dict_value(
                    params['config'], 'path', 'pictures')
                path = os.path.join(path, "{}{}".format(
                    IDX, self._get_file_purename(filepath)))
                IDX += 1
        except Exception as e:
            pass

        try:
            repo.create_file(
                path=path,
                message=message,
                branch=branch,
                content=content)
        except Exception as e:
            return False, None

        url = "https://cdn.jsdelivr.net/gh/{}/{}@{}/{}".format(
            g.get_user().login, params['config']['repo'], params['config']['branch'], path)
        return True, url

    def download(self, url):
        if "cdn.jsdelivr.net" in url:
            header = "https://raw.githubusercontent.com"
            imgpath = url.split("gh")[1]
            imgpath = '/'.join(imgpath.split('@'))
            url = header + imgpath
        return super().download(url)
