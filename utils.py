import os
import re
import hashlib

DB = "picvt.csv"


def endwith(path, formats):
    for format in formats:
        format_ok = os.path.splitext(path)[-1] == ".{}".format(format)
        if format_ok:
            return True
    return False


def contenwith(path, patterns):
    for pattern in patterns:
        if pattern in path:
            return True
    return False


def file_replace(filename, pattern, repl):
    data = ""
    with open(filename, 'r') as f:
        data = f.read()
        f.close()
        data = re.sub(pattern, repl, data)
    with open(filename, 'w') as f:
        f.write(data)
        f.close()


def content_md5(content):
    md5 = None
    md5 = hashlib.md5()
    md5.update(content)
    md5 = md5.hexdigest()
    return md5
