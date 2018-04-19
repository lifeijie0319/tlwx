#-*- coding:utf-8 -*-
import hashlib
import xml.etree.ElementTree as ET

from tornado.log import app_log

from .common import BaseHandler
from .. import config
from ..service.async_wx import CustomMessage
from ..tool import get_oauth_url
from ..wx_msg import Custom, TPL, XML


class RootHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.exempt_csrf = True

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

    async def post(self):
        root = ET.fromstring(self.request.body)
        xml_type = root.find('MsgType').text
        if xml_type == 'text':
            await self.text_handler(root)
        elif xml_type == 'event':
            return self.event_handler(root)
        else:
            return self.write('')

    async def text_handler(self, root):
        openid = root.find('FromUserName').text
        serverid = root.find('ToUserName').text
        send_text = root.find('Content').text
        binded = self.check_bind(openid)
        if send_text in ('jcbd'):
            if binded:
                url = get_oauth_url('/ccrd/unbind')
                reply_text = '解绑信用卡，<a href="' + url + '">点击这里</a>。'
            else:
                reply_text = '您当前未绑定信用卡'
            ret = {'to_user': openid, 'from_user': serverid, 'content': reply_text}
            self.render('xml/text.xml', **ret)
            return
        if not binded:
            url = get_oauth_url('/ccrd/bind')
            reply_text = '尚未绑定信用卡，绑定<a href="' + url + '">点击这里</a>。'
            ret = {'to_user': openid, 'from_user': serverid, 'content': reply_text}
            self.render('xml/text.xml', **ret)
            return
        elif send_text in ('账单', 'ZD', 'zd'):
            return
        elif send_text in ('额度', 'ED', 'ed'):
            return
        elif send_text in ('积分', 'JF', 'jf'):
            return
        elif send_text in ('活动', 'HD', 'hd'):
            return
        elif send_text in ('优惠', 'yh', 'YH'):
            return
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
            if key == 'ccrd':
                ret = XML.ccrd_news(openid, serverid)
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
