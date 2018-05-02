#-*- coding:utf-8 -*-
import json
import random
import urllib.parse as urlparse

from tornado.log import app_log
from tornado.web import MissingArgumentError, RequestHandler

from .. import config
from ..db.api import OP_User
from ..db.sqlal import Session
from ..service.async_wx import WXUser
from ..service.pic_vcode import VerifyCode
from ..service.rsa import rsa_decrypt
from ..tool import get_oauth_url, G
from ..wx_msg import TPL


def need_openid(func):
    async def wrapper(self, *args, **kwargs):
        openid = self.get_cookie('openid')
        openid = 'oSDTiwq1vFtLARyBeBGhRpNeXczA'
        if not openid:
            try:
                code = self.get_argument('code')
                openid = await WXUser.oauth_get_openid(code)
                if not openid:
                    raise Exception('获取openid失败')
            except MissingArgumentError:
                app_log.debug('REQUEST %s', self.request.__dict__)
                current_url = self.request.uri.split(config.URL_PREFIX)[1]
                self.redirect(get_oauth_url(current_url))
                return
        self.set_cookie('openid', openid)
        self._openid = openid
        app_log.debug('FUNC: %s', func)
        await func(self, *args, **kwargs)
    return wrapper


def need_bind(func):
    async def wrapper(self, *args, **kwargs):
        if not OP_User(self.db).check_bind(self.openid):
            if self.request.method in ("GET", "HEAD"):
                url = config.BASE_URL + '/ccrd/bind'
                #if "?" not in url:
                #    if urlparse.urlsplit(url).scheme:
                #        next_url = self.request.full_url()
                #    else:
                #        next_url = self.request.uri
                #    url += "?" + urlparse.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        await func(self, *args, **kwargs)
    return wrapper


class BaseHandler(RequestHandler):
    def prepare(self):
        self.xsrf_token
        self.db = Session()

    def on_finish(self):
        #app_log.debug('%' * 10 + 'FINISHED' + '%' * 10)
        self.db.close()

    def check_xsrf_cookie(self):
        if not hasattr(self, 'exempt_csrf'):
            super().check_xsrf_cookie()

    def check_vcode(self, vcode):
        real_vcode = self.get_secure_cookie('vcode')
        app_log.info('VCODE:REAL_VCODE %s:%s', vcode, real_vcode)
        if not real_vcode:
            return {'success': False, 'msg': '验证码过期'}
        if vcode != real_vcode.decode():
            return {'success': False, 'msg': '验证码错误'}
        return {'success': True}

    @property
    def openid(self):
        if hasattr(self, '_openid'):
            return self._openid
        return self.get_cookie('openid')


class StaticTPLHandler(BaseHandler):
    def get(self, path):
        self.render(path)

    def post(self):
        app_log.info('enter this')


class SendVcodeHandler(BaseHandler):
    async def post(self):
        cellphone = self.get_argument('cellphone')
        client_now = self.get_argument('now')
        app_log.info('params: %s', self.request.body)
        vcode = str(random.randint(1000, 9999))
        app_log.info('VCODE %s', vcode)
        self.set_secure_cookie('vcode', vcode, expires=int(client_now) / 1000 + 120)
        message = '来自通联金融的验证码，%s' % vcode
        req = {
            'MOBILE_NO': cellphone,
            'MESSAGE': message,
        }
        ret = await G.tl_cli.send2tl('12105', req)
        if not ret['success']:
            return self.write(ret)
        self.write({'success': True})


class RefreshPicVcodeHandler(BaseHandler):
    @need_openid
    async def get(self):
        generator = VerifyCode()
        img, code = generator.createCodeImage()
        app_log.info('PIC_VCODE: %s', code)
        img.save(config.MEDIA_PATH + '/pic_vcode/' + self.openid + '.jpg','JPEG')
        self.set_secure_cookie('pic_vcode', code)
        self.write({'success': True, 'url': config.MEDIA_URL + '/pic_vcode/' + self.openid + '.jpg'})


class UploadImgHandler(BaseHandler):
    @need_openid
    async def post(self):
        imgs = self.request.files.get('photo', None)
        if not imgs:
            return self.write({'success': False})
        img = imgs[0]
        app_log.debug(img.keys())
        dirname = self.get_argument('dirname')
        path = config.MEDIA_PATH + '/' + dirname + '/'
        with open(path + self.openid + '.jpg', 'wb') as f:
            f.write(img['body'])
        self.write({'success': True})


class InfoCheckHandler(BaseHandler):
    async def post(self):
        app_log.debug('REQ: %s', self.request.body)
        data = json.loads(rsa_decrypt(self.request.body))
        req = {
            'CARD_NO': data['ccrdno'],
            'OPT': 0,
        }
        ret = await G.tl_cli.send2tl('11010', req)
        if not ret['success']:
            return self.write(ret)
        elif not ret['MOBILE_NO']:
            return self.write({'success': False, 'msg': '获取不到手机号'})
        elif ret['ID_NO'] != data['idno']:
            return self.write({'success': False, 'msg': '卡号对应的证件号与输入的证件号不匹配'})
        return self.write({'success': True, 'cellphone': ret['MOBILE_NO']})


class TestHandler(BaseHandler):
    async def get(self, action):
        with open(config.BASE_DIR + '/app/tpl/xml/91000_REQ.xml') as f:
            xml = f.read()
        app_log.debug('%s %s', xml, type(xml))
        ret = await G.tl_cli.send(xml.encode('utf-8'))
        app_log.debug(ret)
        return self.write(ret)
