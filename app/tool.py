# -*- coding: utf-8 -*-
import redis

from tornado.log import gen_log
from tornado.web import MissingArgumentError

from .config import APPID, BASE_URL, G, REDIS, URL_PREFIX
from .service.wx import oauth_get_openid


def get_oauth_url(redirect_uri, state='1'):
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=' +\
        BASE_URL + redirect_uri + '&response_type=code&scope=snsapi_base&state=' + state + '#wechat_redirect'


def get_openid(self):
    openid = self.get_cookie('openid')
    if not openid:
        try:
            code = self.get_argument('code')
            openid = oauth_get_openid(code)
            if not openid:
                raise Exception('获取openid失败')
            self.set_cookie('openid', openid)
        except MissingArgumentError:
            gen_log.debug('REQUEST %s', self.request.__dict__)
            current_url = self.request.uri.split(URL_PREFIX)[1]
            self.redirect(get_oauth_url(current_url))
            return
    gen_log.info('FINAL OPENID: %s', openid)
    return openid


def common_callback(res):
    gen_log.debug(res)
    if res.error:
        res.rethrow()
    gen_log.info('ASYNC HTTP RESPONSE: %s', res.body)


def init_G():
    G.redis_conn = redis.StrictRedis(host=REDIS.get('HOST'), port=REDIS.get('PORT'), db=0)
    gen_log.info(G)


def get_redis_value(key):
    return G.redis_conn.get(key).decode('utf-8')
