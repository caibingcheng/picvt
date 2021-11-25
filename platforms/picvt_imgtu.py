from .picvt_base import PICVT
import re


class Process(PICVT):
    def __init__(self):
        self.img_pattern = re.compile(r'.*ax1x.*', re.M)
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
