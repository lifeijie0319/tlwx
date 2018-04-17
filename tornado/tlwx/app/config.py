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
class G:pass
