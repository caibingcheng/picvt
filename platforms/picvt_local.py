from .picvt_base import PICVT
import re


class Process(PICVT):
    def __init__(self):
        self.img_pattern = re.compile(r'^!\[.*', re.M)
        self.url_pattern = re.compile(r'((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))|("\2([^%\/\|:\n\"]*)")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)')

    def extract(self, content):
        url_list = []
        result = self.img_pattern.findall(content)
        for url in result:
            url = self.url_pattern.search(url)
            if url:
                url_list.append(url.group())
        return url_list

    def download(self, url):
        return True, url