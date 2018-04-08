#-*- coding:utf-8 -*-
import hashlib
import json
import random
import tornado.web
import xml.etree.ElementTree as ET

from tornado.log import app_log

from .. import config
from ..service.pic_vcode import VerifyCode
from ..tool import get_oauth_url, get_openid
from ..xml_msg import xml_credit_card


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie('openid')


class RootHandler(BaseHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        l = sorted([timestamp, nonce, config.TOKEN])
        s = hashlib.sha1()
        for t in l:
            s.update(t)
        dig = s.digest().encode('hex')
        if signature == dig:
            return self.write(echostr)
        else:
            #logger.debug(u'check signature fail: %s vs %s' %(signature, dig))
            return self.write('')

    def post(self):
        root = ET.fromstring(self.request.body)
        xml_type = root.find('MsgType').text
        if xml_type == 'text':
            return self.text_handler(root)
        elif xml_type == 'event':
            return self.event_handler(root)
        else:
            return self.write('')

    def text_handler(self, root):
        openid = root.find('FromUserName').text
        serverid = root.find('ToUserName').text
        send_text = root.find('Content').text
        ret = {'to_user': openid, 'from_user': serverid, 'content': send_text}
        return self.render('xml/text.xml', **ret)

    def event_handler(self, root):
        app_log.info('EVENT')
        openid = root.find('FromUserName').text
        serverid = root.find('ToUserName').text
        event = root.find('Event').text
        if event == 'CLICK':
            key = root.find('EventKey').text
            if key == 'credit_card':
                ret = xml_credit_card(openid, serverid)
                #app_log.info(self.render_string('xml/news.xml', **ret))
                return self.render('xml/news.xml', **ret)
            elif key == 'test':
                ret = {'to_user': openid, 'from_user': serverid, 'content': '<a href="https://www.baidu.com">百度</a>'}
                return self.render('xml/text.xml', **ret)
        else:
            return self.write('')


class StaticTPLHandler(BaseHandler):
    def get(self, path):
        openid = get_openid(self)
        app_log.debug('OPENID %s', openid)
        return self.render(path)


class SendVcodeHandler(BaseHandler):
    def post(self):
        cellphone_number = self.request.body
        vcode = random.randint(100000, 999999)
        return self.write({'success': True})


class RefreshPicVcodeHandler(BaseHandler):
    def get(self):
        openid = get_openid(self)
        generator = VerifyCode()
        img, code = generator.createCodeImage()
        img.save(config.MEDIA_PATH + '/pic_vcode/' + openid + '.jpg','JPEG')
        return self.write({'success': True, 'url': config.MEDIA_URL + '/pic_vcode/' + openid + '.jpg'})


class UploadImgHandler(BaseHandler):
    def post(self):
        openid = get_openid(self)
        imgs = self.request.files.get('photo', None)
        if not imgs:
            return self.write({'success': False})
        img = imgs[0]
        app_log.debug(img.keys())
        dirname = self.get_argument('dirname')
        path = config.MEDIA_PATH + '/' + dirname + '/'
        with open(path + openid + '.jpg', 'wb') as f:
            f.write(img['body'])
        return self.write({'success': True})


#from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine
from ..service.async_wx import get_tmp_media
class TestHandler(BaseHandler):
    @coroutine
    def get(self, action):
        if action == 'tpl_msg':
            from ..wx_tpl_msg import send_trade_detail
            openid = 'oSDTiwq1vFtLARyBeBGhRpNeXczA'
            data = {
                'date': '2015年6月16日 10:20',
                'type': '收入/支出500元',
                'balance': '300元',
                'summary': '手机银行',
            }
            send_trade_detail(openid, data)
        else:
            mediaid = 'dewdwe'
            response = yield get_tmp_media(mediaid)
            app_log.debug(response)
