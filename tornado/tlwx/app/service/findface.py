#-*- coding:utf-8 -*-
import logging
import requests


api_url = 'http://jswj888.f3322.net:8889'
def detect(path):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = {
        'photo': ('face', open(path, 'rb'), 'image/jpeg'),
    }
    r = requests.post(api_url + '/n-tech/v0/detect', headers=headers, files=files)
    print('REQUEST HEADERS:', r.request.headers)
    print('RESPONSE', r)
    print('CONTENT:', r.json())


def identify(path):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = {
        'photo': ('face', open(path, 'rb'), 'image/jpeg'),
    }
    r = requests.post(api_url + '/n-tech/v0/identify', headers=headers, files=files)
    print('REQUEST HEADERS:', r.request.headers)
    print('RESPONSE', r)
    print('CONTENT:', r.json())


def verify(path1, path2):
    headers = {
        'Authorization': 'Token tGd3-nXYt',
    }
    files = { 
        'photo1': open(path1, 'rb'),
        'photo2': open(path2, 'rb'),
    }
    r = requests.post(api_url + '/n-tech/v0/verify', headers=headers, files=files)
    print('REQUEST HEADERS:', r.request.headers)
    print('RESPONSE', r)
    print('CONTENT:', r.json())


if __name__ == '__main__':
    path1 = '/home/tonglian/tlwx/app/media/face/oSDTiwq1vFtLARyBeBGhRpNeXczA.jpg'
    path2 = '/home/tonglian/tlwx/app/media/face/oSDTiwjobsmlFZNmNsvqvZsBLXLk.jpg'
    #detect(path1)
    #identify(path2)
    verify(path1, path2)
