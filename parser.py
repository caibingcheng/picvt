import json
import sys
import os
import argparse
import importlib


PARAMS = {}
CONFIG = {}
PLATFORMS = []
CONFIG_PATH = "platforms/picvt_config.json"


def get_config():
    global CONFIG
    global CONFIG_PATH
    if CONFIG:
        return CONFIG
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
        f.close()
    return CONFIG


def get_platforms():
    global PLATFORMS
    if PLATFORMS:
        return PLATFORMS
    config = get_config()
    for conf in config:
        PLATFORMS.append(conf['platform'])
    return PLATFORMS


def get_params(args):
    global PARAMS
    if PARAMS:
        return PARAMS

    parser = argparse.ArgumentParser()
    # access
    parser.add_argument('-u', '--user', dest='user',
                        type=str, help='target user', default=None)
    parser.add_argument('-p', '--password', dest='password',
                        type=str, help='target password', default=None)
    parser.add_argument('-t', '--token', dest='token',
                        type=str, help='target token', default=None)

    parser.add_argument('-f', '--format', dest='format',
                        nargs='+', help='file format', default=["md"])
    parser.add_argument('-r', '--retry', dest='retry',
                        type=int, help='retry times', default=1)
    parser.add_argument('-e', '--except', dest='except',
                        nargs='+', help='except path', default=[])

    parser.add_argument('--repo', dest='repo',
                        type=str, help='repo name', default=None)
    parser.add_argument('--branch', dest='branch',
                        type=str, help='branch name', default=None)
    parser.add_argument('--path', dest='path',
                        type=str, help='content path', default=None)
    parser.add_argument('--link', dest='link',
                        type=str, help='content link', default=None)

    parser.add_argument('-D', '--dir', dest='dir', required=True,
                        type=str, help='target dir')
    parser.add_argument('-F', '--from', dest='from', choices=get_platforms(), required=True,
                        type=str, help='from')
    parser.add_argument('-T', '--to', dest='to', choices=get_platforms(), required=True,
                        type=str, help='to')

    params = parser.parse_args(args).__dict__

    def get_platfrom_config(platform):
        config = get_config()
        for conf in config:
            if conf['platform'] == platform:
                return conf
        return None

    config = {
        'repo': params['repo'],
        'branch': params['branch'],
        'path': params['path'],
        'link': params['link'],
    }
    PARAMS = {
        'from': {
            'platform': params['from'],
            'execute': get_platfrom_config(params['from'])['execute'],
            'config': config,
        },

        'to': {
            'platform': params['to'],
            'execute': get_platfrom_config(params['to'])['execute'],
            'user': params['user'],
            'password': params['password'],
            'token': params['token'],
            'config': config,
        },

        'dir': params['dir'],
        'format': params['format'],
        'retry': params['retry'],
        'except': params['except'],
    }

    PARAMS['from']['execute'] = importlib.import_module(
        'platforms.' + PARAMS['from']['execute']).Process()
    PARAMS['to']['execute'] = importlib.import_module(
        'platforms.' + PARAMS['to']['execute']).Process()

    return PARAMS


if __name__ == "__main__":
    print(get_config())
    print(get_platforms())
    print(get_params(sys.argv[1:]))
