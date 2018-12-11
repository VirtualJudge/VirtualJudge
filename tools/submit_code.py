import time
import traceback
import json
import requests
import argparse


class HttpUtil(object):
    def __init__(self):
        self._req = requests.session()

    @property
    def requests(self):
        return self._req


def login(requests, base_url):
    try:
        if str(base_url).endswith('/') is False:
            base_url += '/'
        account = config_json.get('user')
        if account and account.get('username') and account.get('password'):
            post_data = {'username': account.get('username'), 'password': account.get('password')}
            return requests.post(base_url + 'api/auth/', json=post_data)
        return None
    except OSError:
        traceback.print_exc()
        return None


def post_code(requests, base_url, json_str):
    if str(base_url).endswith('/') is False:
        base_url += '/'
    try:
        res = requests.post(base_url + 'api/submission/', json=json_str)
        print(res.text)
        return 'SUCCESS'
    except OSError:
        traceback.print_exc()
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='提交或更新爬虫账号到VJ')
    parser.add_argument('--config', type=str, default='config.json', help='json config file path')
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config_json = json.loads(f.read())
        base_url = config_json.get('base_url')

        client = HttpUtil()
        res = login(client.requests, base_url)
        client.requests.headers.update({'X-CSRFToken': client.requests.cookies.get('csrftoken')})
        json_str = {
            'code': """
        #include <iostream>
        using namespace std;
        int main(){
            int a, b;
            while(cin >> a >> b){
                cout << a + b << endl;
            }
        }
            """,
            'language': '1',
            'remote_id': 1000,
            'remote_oj': 'WUST'
        }
        for i in range(5):
            pos = post_code(client.requests, base_url, json_str)
            time.sleep(5)
        exit(0)
    exit(1)
