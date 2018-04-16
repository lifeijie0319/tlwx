#-*- coding:utf8 -*-
from tornado.log import app_log

from . import config
from .tool import get_oauth_url
from .service.async_wx import Message


class TPL:
    TRADE_DETAAIL_TPL_ID = 'dIKccSFgM7gi7zwzd2t960_4Akm-JORICZNwZCAoS1s'

    @classmethod
    def send_trade_detail(cls, openid, data):
        app_log.info('send_trade_detail')
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
        Message.send_template_msg(openid, cls.TRADE_DETAAIL_TPL_ID, url, content)


class XML:
    @staticmethod
    def example_news(openid, serverid):
        ret = {
            'to_user': openid,
            'from_user': serverid,
            'count': 3,
            'items': [
                {
                    'title': '表单',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/credit_card/mes_apply1.jpg',
                    'url': get_oauth_url('/staticfile/form.html'),
                },
                {
                    'title': 'jssdk',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/credit_card/mes_apply2.png',
                    'url': get_oauth_url('/staticfile/jssdk/index.html'),
                },
                {
                    'title': '图片上传',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/credit_card/mes_progress.png',
                    'url': get_oauth_url('/staticfile/img_upload.html'),
                },
            ],
        }
        return ret


class Custom:
    def example_articles():
        description = '账单金额 : ￥1000\n' + '最低还款额 : ￥100\n' +\
            '账单日 : 2018-01-01\n' + '最后还款日 : 2015-12-05'
        articles = [
            {
                'title': '自定义测试图文消息',
                'description': description,
                'url': get_oauth_url('/staticfile/form.html'),
                #'picurl': config.BASE_URL + '/static/img/credit_card/mes_apply1.jpg',
            },
            {
                'title': '自定义测试图文消息',
                'url': get_oauth_url('/staticfile/form.html'),
                'picurl': config.BASE_URL + '/static/img/credit_card/mes_apply2.png',
            },
        ]
        return articles
