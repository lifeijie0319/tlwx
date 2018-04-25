#-*- coding:utf-8 -*-
import logging
import requests

from tornado.log import app_log


api_url = 'https://yun.anytec.cn'


def detect(path):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = {
        'photo': ('face', open(path, 'rb'), 'image/jpeg'),
    }
    r = requests.post(api_url + '/n-tech/v0/detect', files=files)
    app_log.info('REQUEST HEADERS: %s', r.request.headers)
    app_log.info('RESPONSE %s', r)
    app_log.info('CONTENT: %s', r.json())


def identify(path):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = {
        'photo': ('face', open(path, 'rb'), 'image/jpeg'),
    }
    r = requests.post(api_url + '/n-tech/v0/identify', headers=headers, files=files)
    app_log.info('REQUEST HEADERS: %s', r.request.headers)
    app_log.info('RESPONSE %s', r)
    app_log.info('CONTENT: %s', r.json())


def verify(path1, path2):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = { 
        'photo1': open(path1, 'rb'),
        'photo2': open(path2, 'rb'),
    }
    r = requests.post(api_url + '/n-tech/v0/verify', headers=headers, files=files)
    app_log.info('REQUEST HEADERS: %s', r.request.headers)
    app_log.info('RESPONSE %s', r)
    app_log.info('CONTENT: %s', r.json())


def gallery_list():
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    r = requests.post(api_url + '/v0/galleries', headers=headers)
    app_log.info(r)


if __name__ == '__main__':
    path1 = '/home/tonglian/tlwx/app/media/face/oSDTiwq1vFtLARyBeBGhRpNeXczA.jpg'
    path2 = '/home/tonglian/tlwx/app/media/face/oSDTiwjobsmlFZNmNsvqvZsBLXLk.jpg'
    detect(path1)
    #identify(path2)
    #verify(path1, path2)
    #gallery_list()
