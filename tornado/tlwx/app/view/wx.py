#-*- coding:utf-8 -*-
import copy
import json
import tornado.web

from tornado.gen import coroutine
from tornado.log import app_log

from .common import BaseHandler
from .. import config
from ..tool import get_oauth_url, get_redis_value, G
from ..service.async_wx import Basic, JSSDK, Material, Menu


class RefreshTokenHandler(BaseHandler):
    @coroutine
    def get(self):
        access_token, expires_in = yield Basic.get_access_token()
        G.redis_conn.set(config.ACCESS_TOKEN_KEY, access_token)
        ticket = yield Basic.get_jsapi_ticket(access_token)
        G.redis_conn.set(config.JSAPI_TICKET_KEY, ticket)
        self.write('success')


class RefreshMenuHandler(BaseHandler):
    def get(self):
        menu = Menu()
        access_token = get_redis_value(config.ACCESS_TOKEN_KEY)
        app_log.info('ACCESS_TOKEN: %s', access_token)
        menu.delete(access_token)
        menu.create(access_token)
        self.write('success')

    def configure(self, origin_menu):
        menu_config = copy.deepcopy(origin_menu)
        for button in menu_config.get('button'):
            for sub_button in button.get('sub_button'):
                if sub_button.get('type') == 'view':
                    sub_button['url'] = get_oauth_url(sub_button['url'])
        app_log.debug('menu_config %s', menu_config)
        return menu_config


class JSSDKHandler(BaseHandler):
    def post(self):
        url = self.get_argument('url')
        result = JSSDK.config(url)
        app_log.debug('%s %s', type(result), result)
        self.write(result)


class UploadImgHandler(BaseHandler):
    @coroutine
    def post(self):
        openid = yield self.get_openid()
        kargs = json.loads(self.request.body)
        app_log.info(kargs)
        for item in kargs.get('imgs'):
            img = yield self.download_file(item['mediaid'], config.MEDIA_PATH + '/' + item['dirname'] + '/', openid)
            if not img.get('success'):
                self.write({'success': False, 'msg': '图片提交失败'})
                return
        self.write({'success': True})

    @coroutine
    def download_file(self, mediaid, path, filename):
        app_log.info('%s, %s, %s', mediaid, path, filename)
        res = yield Material.get_tmp(mediaid)
        if res.get('success'):
            app_log.debug('%s, %s', path, filename)
            with open(path + filename + '.jpg', 'wb') as f:
                f.write(res.get('content'))
            res = {'success': True}
        return res
