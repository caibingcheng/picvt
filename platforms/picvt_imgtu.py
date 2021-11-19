from .picvt_base import PICVT
import re


class Process(PICVT):
    def __init__(self):
        self.img_pattern = re.compile('!\[.*\]\(.*ax1x.*\)', re.M)
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def extract(self, content):
        result = self.img_pattern.findall(content)
        return [self.url_pattern.search(url).group() for url in result]
