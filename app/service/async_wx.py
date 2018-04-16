#-*- coding:utf-8 -*-
import hashlib
import json
import random
import string
import time

from datetime import datetime
from tornado.gen import coroutine
from tornado.httpclient import HTTPRequest
from tornado.log import gen_log

from ..config import APPID, APPSECRET, JSAPI_TICKET_KEY, TOKEN, ACCESS_TOKEN_KEY
from ..db.model.admin import WXMenu
from ..tool import common_callback, get_oauth_url, get_redis_value, G


class Basic:
    @staticmethod
    @coroutine
    def get_access_token():
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)
        res = yield G.async_http_cli.fetch(url)
        res = json.loads(res.body)
        gen_log.info('get_access_token %s', res)
        return res['access_token'], res['expires_in']

    @staticmethod
    @coroutine
    def get_jsapi_ticket(access_token):
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type={type}'
        params = {'access_token': access_token, 'type': 'jsapi'}
        res = yield G.async_http_cli.fetch(url.format(**params))
        res = json.loads(res.body)
        gen_log.info('get_jsapi_ticket %s', res)
        return res['ticket']


class WXUser:
    def __init__(self):
        pass

    @staticmethod
    @coroutine
    def oauth_get_openid(code, state='1'):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID, APPSECRET, code)
        res = yield G.async_http_cli.fetch(url)
        res = json.loads(res.body)
        gen_log.info('OAUTH_GET_OPENID RES: %s', res)
        openid = res['openid']
        return openid

    @staticmethod
    @coroutine
    def check_user_subscribed(openid):
        access_token = get_redis_value(ACCESS_TOKEN_KEY)
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
        res = yield G.async_http_cli.fetch(url)
        res = json.loads(res.body)
        #gen_log.debug(res)
        if res.get('errcode'):
            return res.get('errmsg')
        else:
            return res.get('subscribe')

class Message:
    @staticmethod
    def send_template_msg(openid, template_id, url, content):
        access_token = get_redis_value(ACCESS_TOKEN_KEY)
        gen_log.info('OPENID: %s, %s', openid, type(openid))
        post_data = {
            "touser": openid,
            "template_id": template_id,
            "url": url,
            "data": content,
        }
        post_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
        post_data = json.dumps(post_data).encode('utf-8')
        gen_log.info('POST: %s', post_data)
        req = HTTPRequest(post_url, method='POST', body=post_data)
        G.async_http_cli.fetch(req, common_callback)


class CustomMessage:
    @classmethod
    def send(cls, openid, data):
        data = json.dumps(data, ensure_ascii=False)
        gen_log.info('POST: %s', data)
        access_token = get_redis_value(ACCESS_TOKEN_KEY)
        post_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
        G.async_http_cli.fetch(post_url, common_callback, method='POST', body=data)

    @classmethod
    def text(cls, openid, content):
        data = {
            'touser': openid,
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
        cls.send(openid, data)

    @classmethod
    def news(cls, openid, articles):
        data = {
            'touser': openid,
            'msgtype': 'news',
            'news': {
                'articles': articles
            }
        }
        cls.send(openid, data)


class Menu:
    def __init__(self, menu=None):
        if menu:
            self.menu = menu
        else:
            self.menu = self.construct()
        gen_log.info('menu: %s', self.menu)

    def construct(self):
        menus = G.db.query(WXMenu).filter(WXMenu.level==1)
        gen_log.info('count: %s', menus.count())
        root = {
            'button': []
        }
        l1_count = menus.count()
        if l1_count > 3 or l1_count == 0:
            raise Exception('一级菜单的数量不对')
        for l1 in menus:
            if l1.children:
                if len(l1.children) > 5:
                    raise Exception(l1.name + '的子菜单的数量超过五个')
                sub_buttons = [self.construct_unit(l2) for l2 in l1.children]
                root['button'].append({
                    'name': l1.name,
                    'sub_button': sub_buttons
                })
            else:
                unit = self.construct_unit(l1)
                root['button'].append(unit)
        return root

    def construct_unit(self, menu):
        unit = {
            'type': menu.type,
            'name': menu.name
        }
        if menu.type == 'click':
            unit['key'] = menu.key
        elif menu.type == 'view':
            unit['url'] = get_oauth_url(menu.url)
        else:
            raise Exception('未知的按钮类型')
        return unit

    def create(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        data = json.dumps(self.menu, ensure_ascii=False)
        if isinstance(data, str):
            data = data.encode('utf-8')
        G.async_http_cli.fetch(post_url, common_callback, method='POST', body=data)

    @staticmethod
    def query(access_token):
        url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % access_token
        G.async_http_cli.fetch(url, common_callback)

    @staticmethod
    def delete(access_token):
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % access_token
        #url = 'http://192.168.10.210:8888'
        G.async_http_cli.fetch(url, common_callback)


class JSSDK:
    @classmethod
    def sign(cls, jsapi_ticket, url):
        """jssdk签名函数"""
        #gen_log.debug('ENTER SIGN')
        nonceStr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        timestamp = int(time.time())
        ret = {
            'nonceStr': nonceStr,
            'jsapi_ticket': jsapi_ticket,
            'timestamp': timestamp,
            'url': url
        }
        secret_str = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
        ret['signature'] = hashlib.sha1(secret_str.encode('utf-8')).hexdigest()
        for key in ret.keys():
            gen_log.debug('%s\n', type(ret[key]))
        return ret

    @classmethod
    def config(cls, url):
        #gen_log.debug('START: %s', datetime.now())
        jsapi_ticket = get_redis_value(JSAPI_TICKET_KEY)
        #gen_log.debug('TIMETAG1: %s', datetime.now())
        if jsapi_ticket == None:
            return {'success': False, 'msg': 'failed to get jsapi_ticket'}
        ret = cls.sign(jsapi_ticket, url)
        #gen_log.debug('TIMETAG2: %s', datetime.now())
        gen_log.info('RETURN: %s %s', ret, type(ret))
        if ret == None:
            return {'success': False, 'msg': 'failed to sign'}
        #gen_log.debug('END: %s', datetime.now())
        return {'success': True, 'config': ret}


class Material:
    @staticmethod
    @coroutine
    def get(type='image', offset=0, count=1):
        access_token = get_redis_value(ACCESS_TOKEN_KEY)
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % access_token
        post_data = {
            'type': 'image',
            'offset': 0,
            'count': 1,
        }
        post_data = json.dumps(post_data)
        res = yield G.async_http_cli.fetch(url, method='POST', body=post_data)
        res = json.loads(res.body)
        gen_log.info('RETURN: %s', res)
        return res['item'][0]['media_id']

    @staticmethod
    @coroutine
    def get_tmp(mediaid):
        access_token = get_redis_value(ACCESS_TOKEN_KEY)
        #gen_log.debug(mediaid)
        gen_log.debug('access_token %s', access_token)
        url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' %(access_token, mediaid)
        res = yield G.async_http_cli.fetch(url)
        #gen_log.debug(res.headers)
        content_type = res.headers.get('Content-Type')
        res = res.body
        if content_type == 'image/jpeg':
            res = {'success': True, 'content': res}
        else:
            res = json.loads(res)
            res['success'] = False
            gen_log.debug(res)
        return res
