import sys
import os
import re

import pandas as pd
from parser import get_params

DB = "picvt.csv"


def endwith(path, formats):
    for format in formats:
        format_ok = os.path.splitext(path)[-1] == ".{}".format(format)
        if format_ok:
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


if __name__ == "__main__":
    params = get_params(sys.argv[1:])

    jobs_cnt = 0
    jobs_ok = 0

    db = []
    for root, _, files in os.walk(params['dir']):
        for filepath in files:
            filepath = os.path.join(root, filepath)
            if not endwith(filepath, params['format']):
                continue

            content = ""
            with open(filepath, 'r') as f:
                content = f.read()
                f.close()

            urls = params['from']['execute'].extract(content)
            if not urls:
                continue

            status = {
                'filepath': filepath,
                'jobs': [
                    {"from": url, "to": None, "ok": False}
                    for url in urls
                ],
            }
            jobs_cnt = jobs_cnt + len(status['jobs'])
            db.append(status)

    jobs_idx = 0
    for i, status in enumerate(db):
        for j, job in enumerate(status['jobs']):
            jobs_idx = jobs_idx + 1

            print("[{}/{}]".format(jobs_idx, jobs_cnt),
                  "fetching", job['from'], end=' ')
            save_ok, filepath = params['from']['execute'].download(job['from'])
            db[i]['jobs'][j]['save'] = filepath
            db[i]['jobs'][j]['ok'] = save_ok
            if not save_ok:
                print("failed")
                continue
            print("ok")
            print("[{}/{}]".format(jobs_idx, jobs_cnt), "saving to", filepath)

            print("[{}/{}]".format(jobs_idx, jobs_cnt), "uploading", end=' ')
            upload_ok, url = params['to']['execute'].upload(
                filepath, params['to'])
            db[i]['jobs'][j]['to'] = url
            db[i]['jobs'][j]['ok'] = upload_ok
            if not upload_ok:
                print("failed")
                continue
            print(url, "ok")

            if upload_ok:
                file_replace(db[i]['filepath'], db[i]['jobs']
                             [j]['from'],  db[i]['jobs'][j]['to'])
                jobs_ok = jobs_ok + 1

    print("success {}/{}".format(jobs_ok, jobs_cnt))

    df = pd.json_normalize(db)
    df.to_csv(DB, index=False,
              sep=",", encoding="utf-8")
