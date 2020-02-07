# VirtualJudge
[![Build Status](https://travis-ci.org/VirtualJudge/VirtualJudge.svg?branch=master)](https://travis-ci.org/VirtualJudge/VirtualJudge)
[![Coverage Status](https://coveralls.io/repos/github/VirtualJudge/VirtualJudge/badge.svg?branch=master)](https://coveralls.io/github/VirtualJudge/VirtualJudge?branch=master)
[![Python](https://img.shields.io/badge/Python-3.8-blue.svg)](https://img.shields.io/badge/Python-3.8-blue.svg)
[![Django](https://img.shields.io/badge/Django-3.0.3-blue.svg)](https://img.shields.io/badge/Django-3.0.3-blue.svg)
[![djangorestframework](https://img.shields.io/badge/djangorestframework-3.11.0-blue.svg)](https://img.shields.io/badge/djangorestframework-3.11.0-blue.svg)  

Virtual Judge Based on Python


### Test Deploy
#### Test Enviroment
 
 - Python3.8
 - docker latest
 - docker-compose latest
 - Git
 
#### Install Instructions
1. Install Dependencies: `pip3 install -r requirements.txt`.  
2. Install `Redis` and `Postgres`: Change directory to `dockerfiles` and run `docker-compose -f dev.yml`.  
3. Initial Database: Run `python3 ./manage.py init_install`, it will initialize databases and add default administrator account `root/rootroot`.  
4. Run Service: `python3 ./manage.py runserver 127.0.0.1:8000`.  
5. Search Problems: for example,`http://127.0.0.1:8000/api/problem/poj/3223/`. 

### Spider
[https://github.com/VirtualJudge/spider](https://github.com/VirtualJudge/spider)
### FrontEnd
[https://github.com/VirtualJudge/VirtualJudgeFE](https://github.com/VirtualJudge/VirtualJudgeFE) 

