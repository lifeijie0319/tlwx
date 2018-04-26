# -*- coding: utf-8 -*-
import datetime
import redis

from tornado.log import app_log

from .config import APPID, BASE_DIR, BASE_URL, G


def get_oauth_url(redirect_uri, state='1'):
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=' +\
        BASE_URL + redirect_uri + '&response_type=code&scope=snsapi_base&state=' + state + '#wechat_redirect'


def common_callback(res):
    app_log.debug(res)
    if res.error:
        res.rethrow()
    app_log.info('ASYNC HTTP RESPONSE: %s', res.body)


def get_redis_value(key):
    return G.redis_conn.get(key).decode('utf-8')


def gen_req_token():
    token_id = G.redis_conn.incr('REQ_TOKEN_ID')
    token = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(token_id % 1000).zfill(3)
    return token


def format_date(s):
    t = s[:4] + '-' + s[4:6] + '-' + s[6:]
    return t


def xml_format(s, type):
    if type == 'date':
        t = s[:4] + '-' + s[4:6] + '-' + s[6:]
    elif type == 'time':
        t = s[:2] + ':' + s[2:4] + ':' + s[4:]
    return t


def get_doc(name):
    with open(BASE_DIR + '/app/static/doc/ccrd/' + name) as f:
        doc = f.read()
    return doc


class Currency:
    def __init__(self, code='156'):
        self.code = code
        self.symbol = '$' if code == '840' else '￥'
        self.name = '美元' if code == '840' else '人民币'
