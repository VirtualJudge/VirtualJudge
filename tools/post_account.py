#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

提交爬虫用的账号到服务器

"""

import argparse
import json
import traceback

from tools.login import login
from tools.utils import HttpUtil


def fresh_account(requests, remote_url):
    remote_url = str(remote_url).rstrip('/') + '/api/language/'
    return requests.post(remote_url)


def post_account(requests, remote_url, account_path):
    if str(remote_url).endswith('/'):
        remote_url += 'api/remote/'
    else:
        remote_url += '/api/remote/'
    try:
        with open(account_path, 'r') as f:
            for account in json.loads(f.read()):
                print(requests.post(remote_url, json=account).text)
            return 'SUCCESS'
    except OSError:
        traceback.print_exc()
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='提交或更新爬虫账号到VJ')
    # parser.add_argument('--remote', type=str, default='http://127.0.0.1:8000/api/remote',
    # help='post remote account url')
    parser.add_argument('--accounts', type=str, default='accounts.json', help='爬虫账号文件')
    parser.add_argument('--config', type=str, default='config.json', help='json config file path')
    # parser.add_argument('--login', type=str, default='http://127.0.0.1:8000/api/login', help='login url')
    args = parser.parse_args()

    client = HttpUtil()
    res = login(client.requests, args.config)
    client.requests.headers.update({'X-CSRFToken': client.requests.cookies.get('csrftoken')})
    print(res.text)
    remote_url = None
    if res is not None:
        with open(args.config, 'r') as f:
            config_json = json.loads(f.read())
            remote_url = config_json.get('base_url')
    pos = post_account(client.requests, remote_url, args.accounts)
    if pos is None:
        print('Network Error')
    else:
        print(str(pos))
    res = fresh_account(client.requests, remote_url)
    if res:
        print(str(res.text))
    else:
        print('fresh account failed')