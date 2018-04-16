#-*- coding:utf-8 -*-
import os

tornado_settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'tpl'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'static_url_prefix': '/tlwx/static/',
    'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
    'xsrf_cookies': True,
    'debug': True,
}
BASE_URL = 'https://hz.wx.yinsho.com/tlwx'
URL_PREFIX = '/tlwx'
TOKEN = 'yinshowxtoken'
APPID = 'wx6290daffb81416ac'
APPSECRET = 'f3bc7bb9c6dca40dd1bbe9b69fdf6ea0'
ACCESS_TOKEN_KEY = 'tl_access_token'
JSAPI_TICKET_KEY = 'tl_jsapi_ticket'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = BASE_URL + '/media'
MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'media')
REDIS = {
    'HOST': 'localhost',
    'PORT': '6379',
}
MENU={
    'button': [
        {
            'name': '优惠活动',
            'sub_button': [
                {
                    'type': 'click',
                    'name': '首刷礼兑换',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '周周惠生活',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '网上商城',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '汽车分期',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '财富管理',
                    'key': '1',
                },
            ]
        },
        {
            'name': '我要',
            'sub_button':[
                {
                    'type': 'click',
                    'name': '我要办卡',
                    'key': 'credit_card',
                },
                {
                    'type': 'view',
                    'name': '我要推荐办卡',
                    'url': '/staticfile/credit_card/online_apply_invitation1.html',
                },
                {
                    'type': 'view',
                    'name': '我要查申请进度',
                    'url': '/credit_card/online_apply/status/page/1',
                },
                {
                    'type': 'click',
                    'name': '我要开卡激活',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '我要分期',
                    'key': '1',
                },
            ]
        },
        {
            'name': '我的',
            'sub_button':[
                {
                    'type': 'click',
                    'name': '我的账户',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '我的账单',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '我的额度',
                    'key': '1',
                },
                {
                    'type': 'click',
                    'name': '我的积分',
                    'key': '1',
                },
                {
                    'type': 'view',
                    'name': '我的客户经理',
                    'url': '/staticfile/findface.html',
                },
            ]
        },
    ]
}


class G:pass
