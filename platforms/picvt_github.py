from .picvt_base import PICVT
from github import Github
import os


class Process(PICVT):
    def __init__(self):
        pass

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
                path = self._get_dict_value(params['config'], 'path', 'pictures')
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
