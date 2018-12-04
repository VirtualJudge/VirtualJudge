#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

提交爬虫用的账号到服务器

"""

import argparse
import json
import traceback
import requests


class HttpUtil(object):
    def __init__(self):
        self._req = requests.session()

    @property
    def requests(self):
        return self._req


def login(requests, config_path):
    try:
        with open(config_path, 'r') as f:
            config_json = json.loads(f.read())
            print(config_json)
            remote_url = config_json.get('base_url')
            if str(remote_url).endswith('/'):
                remote_url += 'api/auth/'
            else:
                remote_url += '/api/auth/'
            account = config_json.get('account')
            if account and account.get('username') and account.get('password'):
                post_data = {'username': account.get('username'), 'password': account.get('password')}
                return requests.post(remote_url, json=post_data)
            return None
    except OSError:
        traceback.print_exc()
        return None


def fresh_account(requests, remote_url):
    remote_url = str(remote_url).rstrip('/') + '/api/language/'
    return requests.post(remote_url)


def post_account(requests, remote_url, account_path):
    if str(remote_url).endswith('/'):
        remote_url += 'api/account/'
    else:
        remote_url += '/api/account/'
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
    # parser.add_argument('--support', type=str, default='http://127.0.0.1:8000/api/remote',
    # help='post support user url')
    parser.add_argument('--accounts', type=str, default='accounts.json', help='爬虫账号文件')
    parser.add_argument('--config', type=str, default='config.json', help='json config file path')
    # parser.add_argument('--login', type=str, default='http://127.0.0.1:8000/api/login', help='login url')
    args = parser.parse_args()

    client = HttpUtil()
    res = login(client.requests, args.config)
    client.requests.headers.update({'X-CSRFToken': client.requests.cookies.get('csrftoken')})
    print(res)
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
    import time

    print('3秒后刷新账号数据')
    time.sleep(3)
    res = fresh_account(client.requests, remote_url)
    if res:
        print(str(res.text))
    else:
        print('fresh user failed')
