#-*- coding:utf8 -*-
from .config import BASE_URL
from .tool import get_oauth_url


def xml_credit_card(openid, serverid):
    ret = {
        'to_user': openid,
        'from_user': serverid,
        'count': 3,
        'items': [
            {
                'title': '在线申请信用卡',
                'description': '',
                'picurl': BASE_URL + '/static/img/credit_card/mes_apply1.jpg',
                'url': get_oauth_url('/credit_card/online_apply/page/0'),
            },
            {
                'title': '在线申请信用卡',
                'description': '',
                'picurl': BASE_URL + '/static/img/credit_card/mes_apply2.png',
                'url': get_oauth_url('/credit_card/online_apply/page/0'),
            },
            {
                'title': '信用卡申请进度查询',
                'description': '',
                'picurl': BASE_URL + '/static/img/credit_card/mes_progress.png',
                'url': get_oauth_url('/credit_card/online_apply/status/page/1'),
            },
        ],
    }
    return ret
