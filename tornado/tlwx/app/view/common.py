#-*- coding:utf-8 -*-
import hashlib
import json
import random
import time
import urllib.parse as urlparse
import xml.etree.ElementTree as ET

from tornado.gen import coroutine
from tornado.log import app_log
from tornado.web import MissingArgumentError, RequestHandler

from .. import config
from ..db.model import User
from ..service.async_wx import CustomMessage, Material, WXUser
from ..service.pic_vcode import VerifyCode
from ..tool import get_oauth_url, G
from ..wx_msg import Custom, TPL, XML


def need_openid(func):
    @coroutine
    def wrapper(self, *args, **kwargs):
        openid = self.get_cookie('openid')
        if not openid:
            try:
                code = self.get_argument('code')
                openid = yield WXUser.oauth_get_openid(code)
                if not openid:
                    raise Exception('获取openid失败')
            except MissingArgumentError:
                app_log.debug('REQUEST %s', self.request.__dict__)
                current_url = self.request.uri.split(config.URL_PREFIX)[1]
                self.redirect(get_oauth_url(current_url))
                return
        self.set_cookie('openid', openid)
        self.openid = openid
        app_log.debug('FUNC: %s', func)
        yield func(self, *args, **kwargs)
    return wrapper


def need_reg(func):
    @coroutine
    def wrapper(self, *args, **kwargs):
        user = G.db.query(User).filter(User.openid==self.openid).one_or_none()
        if not user:
            if self.request.method in ("GET", "HEAD"):
                url = config.REG_URL
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlparse.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        self.user = user
        yield func(self, *args, **kwargs)
    return wrapper


class BaseHandler(RequestHandler):
    def prepare(self, *args, **kargs):
        self.xsrf_token

    @coroutine
    def get_openid(self):
        openid = self.get_cookie('openid')
        if not openid:
            try:
                code = self.get_argument('code')
                openid = yield WXUser.oauth_get_openid(code)
                if not openid:
                    raise Exception('获取openid失败')
                self.set_cookie('openid', openid)
            except MissingArgumentError:
                app_log.debug('REQUEST %s', self.request.__dict__)
                current_url = self.request.uri.split(config.URL_PREFIX)[1]
                self.redirect(get_oauth_url(current_url))
                return
        app_log.info('FINAL OPENID: %s', openid)
        return openid


class RootHandler(BaseHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        l = sorted([timestamp, nonce, config.TOKEN])
        s = hashlib.sha1()
        for t in l:
            s.update(t.encode('utf-8'))
        dig = s.hexdigest()
        if signature == dig:
            return self.write(echostr)
        else:
            app_log.debug(u'check signature fail: %s vs %s' %(signature, dig))
            return self.write('')

    @coroutine
    def post(self):
        root = ET.fromstring(self.request.body)
        xml_type = root.find('MsgType').text
        if xml_type == 'text':
            yield self.text_handler(root)
        elif xml_type == 'event':
            return self.event_handler(root)
        else:
            return self.write('')

    @coroutine
    def text_handler(self, root):
        openid = root.find('FromUserName').text
        serverid = root.find('ToUserName').text
        send_text = root.find('Content').text
        if send_text == '图片':
            mediaid = yield Material.get()
            app_log.info('mediaid %s', mediaid)
            ret = {'to_user': openid, 'from_user': serverid, 'media_id': mediaid}
            app_log.debug(ret)
            return self.render('xml/img.xml', **ret)
        else:
            reply_text = '''1、输入“图片”返回默认图片。\n2、这是一个<a href="http://www.baidu.com/">百度链接</a>。'''
            ret = {'to_user': openid, 'from_user': serverid, 'content': reply_text}
            return self.render('xml/text.xml', **ret)


    def event_handler(self, root):
        app_log.info('EVENT')
        openid = root.find('FromUserName').text
        serverid = root.find('ToUserName').text
        event = root.find('Event').text
        if event == 'subscribe':
            reply_text = '欢迎关注上海鹏弈程信息科技有限公司'
            ret = {'to_user': openid, 'from_user': serverid, 'content': reply_text}
            return self.render('xml/text.xml', **ret)
        elif event == 'CLICK':
            key = root.find('EventKey').text
            if key == 'reply_news':
                ret = XML.example_news(openid, serverid)
                #app_log.info(self.render_string('xml/news.xml', **ret))
                return self.render('xml/news.xml', **ret)
            elif key == 'reply_tpl':
                data = {
                    'date': '2015年6月16日 10:20',
                    'type': '收入/支出500元',
                    'balance': '300元',
                    'summary': '手机银行',
                }
                TPL.send_trade_detail(openid, data)
                return self.write('')
            elif key == 'custom_msg':
                articles = Custom.example_articles()
                CustomMessage.news(openid, articles)
        else:
            return self.write('')


class StaticTPLHandler(BaseHandler):
    #@coroutine
    def get(self, path):
        #openid = yield self.get_openid()
        #app_log.debug('OPENID %s', openid)
        self.render(path)

    def post(self):
        app_log.info('enter this')


class SendVcodeHandler(BaseHandler):
    def post(self):
        cellphone_number = self.get_argument('cellphone')
        client_now = self.get_argument('now')
        app_log.info('params: %s', self.request.body)
        vcode = str(random.randint(100000, 999999))
        app_log.info('VCODE %s', vcode)
        self.set_secure_cookie('vcode', vcode, expires=int(client_now) / 1000 + 120)
        self.write({'success': True})


class RefreshPicVcodeHandler(BaseHandler):
    @coroutine
    def get(self):
        openid = yield self.get_openid()
        generator = VerifyCode()
        img, code = generator.createCodeImage()
        img.save(config.MEDIA_PATH + '/pic_vcode/' + openid + '.jpg','JPEG')
        self.write({'success': True, 'url': config.MEDIA_URL + '/pic_vcode/' + openid + '.jpg'})


class UploadImgHandler(BaseHandler):
    @coroutine
    def post(self):
        openid = yield self.get_openid()
        imgs = self.request.files.get('photo', None)
        if not imgs:
            return self.write({'success': False})
        img = imgs[0]
        app_log.debug(img.keys())
        dirname = self.get_argument('dirname')
        path = config.MEDIA_PATH + '/' + dirname + '/'
        with open(path + openid + '.jpg', 'wb') as f:
            f.write(img['body'])
        self.write({'success': True})


#from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine
class TestHandler(BaseHandler):
    @coroutine
    def get(self, action):
        if action == 'tpl_msg':
            openid = 'oSDTiwq1vFtLARyBeBGhRpNeXczA'
            data = {
                'date': '2015年6月16日 10:20',
                'type': '收入/支出500元',
                'balance': '300元',
                'summary': '手机银行',
            }
            TPL.send_trade_detail(openid, data)
