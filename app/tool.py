# -*- coding: utf-8 -*-
import datetime
import redis

from tornado.log import gen_log
from tornado.httpclient import AsyncHTTPClient, HTTPClient

from .config import APPID, BASE_URL, G, REDIS, URL_PREFIX
from .db.sqlal import get_session


def get_oauth_url(redirect_uri, state='1'):
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=' +\
        BASE_URL + redirect_uri + '&response_type=code&scope=snsapi_base&state=' + state + '#wechat_redirect'


def common_callback(res):
    gen_log.debug(res)
    if res.error:
        res.rethrow()
    gen_log.info('ASYNC HTTP RESPONSE: %s', res.body)


def init_G():
    G.redis_conn = redis.StrictRedis(host=REDIS.get('HOST'), port=REDIS.get('PORT'), db=0)
    G.http_cli = HTTPClient()
    G.async_http_cli = AsyncHTTPClient()
    G.db = get_session()
    #gen_log.info(G)


def get_redis_value(key):
    return G.redis_conn.get(key).decode('utf-8')


def gen_req_token():
    token_id = G.redis_conn.incr('REQ_TOKEN_ID')
    token = datetime.datetime.now().strftime('%Y%m%d%H%m%s') + str(token_id % 1000).zfill(3)
    return token
