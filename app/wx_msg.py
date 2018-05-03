#-*- coding:utf8 -*-
import datetime

from tornado.log import app_log

from . import config
from .tool import get_oauth_url
from .service.async_wx import Message


class TPL:
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
        Message.send_template_msg(openid, config.TRADE_TPL_ID, url, content)

    @classmethod
    def send_bill(cls, openid, data):
        url = ''
        content = {
            'first': {
                'value': u'您的' + data['card_type'] + '卡' + data['month'] + '月账单',
                'color': '#000000'
            },
            'keyword1': {
                'value': data.get('date'),
                'color': '#000000'
            },
            'keyword2': {
                'value': data.get('pay_date'),
                'color': '#000000'
            },
            'keyword3': {
                'value': data.get('amt'),
                'color': '#000000'
            },
            'keyword4': {
                'value' : data.get('min_amt'),
                'color' :'#000000'
            },
            'remark': {
                'value': u'点击查看详情',
                'color': '#000000'
            },
        }
        Message.send_template_msg(openid, config.BILL_TPL_ID, url, content)

    @classmethod
    def repay(cls, openid, data):
        url = ''
        content = {
            'first': {
                'value': data['date'],
                'color': '#000000'
            },
            'keyword1': {
                'value': data.get('ccrdno_tail'),
                'color': '#000000'
            },
            'keyword2': {
                'value': data.get('amt'),
                'color': '#000000'
            },
            'remark': {
                'value': u'点击查看详情',
                'color': '#000000'
            },
        }
        Message.send_template_msg(openid, config.REPAY_TPL_ID, url, content)


class XML:
    @staticmethod
    def ccrd_news(openid, serverid):
        ret = {
            'to_user': openid,
            'from_user': serverid,
            'count': 4,
            'items': [
                {
                    'title': '在线申请信用卡',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply1.jpg',
                    'url': get_oauth_url('/ccrd/online_apply/select'),
                },
                {
                    'title': '推荐他人办卡',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply2.png',
                    'url': get_oauth_url('/staticfile/ccrd/online_apply/invitation1.html'),
                },
                {
                    'title': '信用卡申请进度查询',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_progress.png',
                    'url': get_oauth_url('/ccrd/online_apply/status/form'),
                },
                {   
                    'title': '信用卡激活',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_progress.png',
                    'url': get_oauth_url('/ccrd/activate'),
                },
            ],
        }
        return ret

    @staticmethod
    def installment(openid, serverid):
        ret = {
            'to_user': openid,
            'from_user': serverid,
            'count': 4,
            'items': [
                {
                    'title': '账单分期',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply1.jpg',
                    'url': get_oauth_url('/ccrd/installment/bill'),
                },
                {
                    'title': '消费分期',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_apply2.png',
                    'url': get_oauth_url('/ccrd/installment/consumption'),
                },
                {
                    'title': '现金分期',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_progress.png',
                    'url': get_oauth_url('/ccrd/installment/cash'),
                },
                {
                    'title': '大额现金分期',
                    'picurl': config.BASE_URL + '/static/img/ccrd/mes_progress.png',
                    'url': get_oauth_url('/ccrd/installment/lg_cash'),
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
           + curr_symbol + tot_due_amt + '\n账单日：' + billing_date + '\n最后还款日：' + pmt_due_date
        articles = [
            {
                'title': '我的账单',
                'description': description,
                'url': get_oauth_url('/ccrd/bill'),
            },
        ]
        return articles

    def limit_query(curr_symbol, acct_limit, acct_otb, acct_cash_otb):
        today = datetime.date.today().strftime('%m月%d日')
        description = today + '\n信用额度：' + curr_symbol + acct_limit + '\n可用额度：'\
           + curr_symbol + acct_otb + '\n预借现金额度：' + acct_cash_otb
        articles = [
            {
                'title': '我的额度',
                'description': description,
                'url': get_oauth_url('/ccrd/limit'),
            },
        ]
        return articles

    def point_query(point_bal, ctd_earned_points):
        today = datetime.date.today().strftime('%m月%d日')
        description = today + '\n积分余额：' + point_bal + '\n本期新增：' + ctd_earned_points
        articles = [
            {
                'title': '我的积分',
                'description': description,
                'url': get_oauth_url('/ccrd/point'),
            },
        ]
        return articles
