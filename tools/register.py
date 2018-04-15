#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

测试登录接口

"""

import argparse
import getpass
from colorama import Fore, Style
from .utils import HttpUtil


def register(requests, url):
    username = input('用户名:')
    email = input('邮箱:')
    password = getpass.getpass('密码:')
    post_data = {'email': email, 'username': username, 'password': password}
    return requests.post(url, json=post_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Login API')
    parser.add_argument('url', type=str, help='注册链接')
    args = parser.parse_args()
    client = HttpUtil()
    url = args.url
    res = register(client.requests, args.url)
    if res is None:
        print(Fore.RED + 'Network Error')
    else:
        print(Fore.GREEN + str(res.status_code))
        print(res.text)
    print(Style.RESET_ALL)
