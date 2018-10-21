# VirtualJudge
[![Build Status](https://travis-ci.org/VirtualJudge/VirtualJudge.svg?branch=master)](https://travis-ci.org/VirtualJudge/VirtualJudge)
[![Coverage Status](https://coveralls.io/repos/github/VirtualJudge/VirtualJudge/badge.svg?branch=master)](https://coveralls.io/github/VirtualJudge/VirtualJudge?branch=master)
[![Python](https://img.shields.io/badge/Python-3.6.5-blue.svg)](https://img.shields.io/badge/Python-3.6.5-blue.svg)
[![Django](https://img.shields.io/badge/Django-2.0.4-blue.svg)](https://img.shields.io/badge/Django-2.0.4-blue.svg)
[![djangorestframework](https://img.shields.io/badge/djangorestframework-3.8.2-blue.svg)](https://img.shields.io/badge/djangorestframework-3.8.2-blue.svg)  
基于Python爬虫的虚拟评测系统  

### 测试部署
#### 测试环境
 
 - python3.6
 - docker latest
 - docker-compose latest
 - git
 
#### 安装过程
1. 安装Python依赖: `pip3 install -r requirements.txt`  
2. 安装Redis和Postgres数据库: 如果没有安装redis和postgres的情况下,在 `dockerfiles` 目录下运行 `docker-compose -f dev.yml`，安装了就跳过这一步
3. 初始化数据库: `python3 ./manage.py init_install` 初始化数据库和admin账号，默认admin账号是`root`，密码是`rootroot`
4. 运行服务: `python3 ./manage.py runserver 127.0.0.1:8000`
5. 初始化爬虫账号: 在`tools`目录下有个`accounts-sample.json`，拷贝一份命名为`accounts.json`，按照格式填入账号密码，另外`config-sample.json`放的是初始化爬虫账号的时候的服务器配置文件,拷贝一份`config.json`放到当前目录下，然后修改里面的配置,之后执行`python3 post_accounts.py`就可以了
6. 查看题目: 浏览器打开`http://127.0.0.1:8000/api/problem/poj/3223/`

### 爬虫地址
[https://github.com/VirtualJudge/spider](https://github.com/VirtualJudge/spider)
### 前端地址
[https://github.com/VirtualJudge/VirtualJudgeFE](https://github.com/VirtualJudge/VirtualJudgeFE)

### demo
[https://vj.prefixai.com/](https://vj.prefixai.com/)


