#-*- coding:utf-8 -*-
from tornado.log import gen_log

from .tool import get_oauth_url
from .service.async_wx import send_template_msg


TRADE_DETAAIL_TPL_ID = '79SB1YCP7Ts06IkJKY_PfhtVzwTSg2H9jrZBL1DgXIY'


def send_trade_detail(openid, data):
    gen_log.info('send_trade_detail')
    url = ''
    content = {
        'first': {
            'value': u'您的账户发起了一笔新的交易',
            'color': '#000000'
        },
        'keyword1': {
            'value': data.get('date'),
            'color': '#000000'
        },
        'keyword2': {
            'value': data.get('type'),
            'color': '#000000'
        },
        'keyword3': {
            'value': data.get('balance'),
            'color': '#000000'
        },
        'keyword4': {
            'value' : data.get('summary'),
            'color' :'#000000'
        },
        'remark': {
            'value': u'点击查看详情',
            'color': '#000000'
        },
    }
    send_template_msg(openid, TRADE_DETAAIL_TPL_ID, url, content)
