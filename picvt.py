import sys
import os

import pandas as pd
from parser import get_params
from utils import *


if __name__ == "__main__":
    params = get_params(sys.argv[1:])

    jobs_cnt = 0
    jobs_ok = 0

    db = []
    dbq = {}
    for root, _, files in os.walk(params['dir']):
        for filepath in files:
            filepath = os.path.join(root, filepath)
            if contenwith(filepath, [".git/", ".repo/"] + params['except']):
                continue
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

    for i, status in enumerate(db):
        for j, job in enumerate(status['jobs']):
            print(status['filepath'], job['from'])

    is_continue = input("Continue: [Y/n]")
    if is_continue == 'n':
        exit()

    jobs_idx = 0
    for i, status in enumerate(db):
        for j, job in enumerate(status['jobs']):
            jobs_idx = jobs_idx + 1

            from_md5 = content_md5(job['from'].encode('utf-8'))
            if from_md5 in dbq.keys():
                db[i]['jobs'][j]['to'] = dbq[from_md5][0]
                db[i]['jobs'][j]['save'] = dbq[from_md5][1]
                db[i]['jobs'][j]['ok'] = True
                print("[{}/{}]".format(jobs_idx, jobs_cnt),
                    "repeating", job['from'], "done")

                file_replace(db[i]['filepath'], db[i]['jobs']
                             [j]['from'],  db[i]['jobs'][j]['to'])
                jobs_ok = jobs_ok + 1
                continue

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
                dbq[from_md5] = (db[i]['jobs'][j]['to'], db[i]['jobs'][j]['save'])

    print("success {}/{}".format(jobs_ok, jobs_cnt))

    df = pd.json_normalize(db)
    df.to_csv(DB, index=False,
              sep=",", encoding="utf-8")
