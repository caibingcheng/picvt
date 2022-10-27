from .picvt_base import PICVT
import re
import os
import shutil


class Process(PICVT):
    def __init__(self, params=None):
        self.img_pattern = re.compile(r'^!\[.*', re.M)
        self.url_pattern = re.compile(
            r'((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))|("\2([^%\/\|:\n\"]*)")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^( |\))\b%\|:\n\"\\\/])+)+\/?)')

    def extract(self, content, params):
        url_list = []
        result = self.img_pattern.findall(content)
        for url in result:
            url = self.url_pattern.search(url)
            if url:
                url_list.append(url.group())
        return url_list

    def download(self, url, params):
        if ('config' in params.keys()) and ('path' in params['config'].keys()):
            url = '{}{}'.format(os.path.abspath(params['config']['path']), url)
        return True, url

    def upload(self, path, params):
        dst = shutil.copy(path, params['config']['path'])
        prelink = params['config']['link']
        prelink = '/statics/' if prelink == "" else prelink
        return True, prelink + dst.split('/')[-1]
