#-*- coding:utf8 -*-
import datetime

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
    def ccrd_news(openid, serverid):
        ret = {
            'to_user': openid,
            'from_user': serverid,
            'count': 3,
            'items': [
                {
                    'title': '在线申请信用卡',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply1.jpg',
                    'url': get_oauth_url('/ccrd/online_apply/1'),
                },
                {
                    'title': '在线申请信用卡',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply2.png',
                    'url': get_oauth_url('/ccrd/online_apply/1'),
                },
                {
                    'title': '信用卡申请进度查询',
                    'description': '',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_progress.png',
                    'url': get_oauth_url('/ccrd/online_apply/status/1'),
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
                #'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply1.jpg',
            },
            {
                'title': '自定义测试图文消息',
                'url': get_oauth_url('/staticfile/form.html'),
                'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply2.png',
            },
        ]
        return articles

    def bill_query(curr_symbol, qual_grace_bal, tot_due_amt, billing_date, pmt_due_date):
        today = datetime.date.today().strftime('%m月%d日')
        description = today + '\n账单金额：' + curr_symbol + qual_grace_bal + '\n最低还款额：'\
           + curr_symbol + tot_due_amt + '\n账单日：' + billing_date + '\n最后还款日：' + pmt_due_date\
           + '\n备注' + '\n' + '-' * 30 + '\n<b>阅读全文</b>'
        articles = [
            {
                'title': '我的账单',
                'description': description,
                'url': get_oauth_url('/ccrd/bill'),
                #'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply1.jpg',
            },
        ]
        return articles
