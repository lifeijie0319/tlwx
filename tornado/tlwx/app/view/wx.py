#-*- coding:utf-8 -*-
import copy
import json
import tornado.web

from tornado.gen import coroutine
from tornado.log import app_log

from .common import BaseHandler
from .. import config
from ..tool import get_oauth_url, get_openid, get_redis_value
from ..service.wx import weixin_jssdk
from ..service.async_wx import get_tmp_media, Menu


class RefreshMenuHandler(BaseHandler):
    def get(self):
        access_token = get_redis_value(config.ACCESS_TOKEN_KEY)
        app_log.info('ACCESS_TOKEN: %s', access_token)
        menu = Menu()
        app_log.debug(config.MENU)
        menu_json = json.dumps(self.configure(config.MENU), ensure_ascii=False)
        menu.delete(access_token)
        menu.create(menu_json, access_token)
        return self.write('success')

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
        result = weixin_jssdk(url)
        import json
        app_log.debug('%s %s', type(result), result)
        return self.finish(result)


class UploadImgHandler(BaseHandler):
    #@coroutine
    def post(self):
        openid = get_openid(self)
        kargs = json.loads(self.request.body)
        app_log.info(kargs)
        for item in kargs.get('imgs'):
            img = self.download_file(item['mediaid'], config.MEDIA_PATH + '/' + item['dirname'] + '/', openid)
            if not img.get('success'):
                return self.write({'success': False, 'msg': '图片提交失败'})
        return self.write({'success': True})

    #@coroutine
    def download_file(self, mediaid, path, filename):
        app_log.info('%s, %s, %s', mediaid, path, filename)
        res = get_tmp_media(mediaid)
        if res.get('success'):
            with open(path + filename + '.jpg', 'wb') as f:
                f.write(res.get('content'))
            res = {'success': True}
        return res
