#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_bind, need_openid
from ...config import G
from ...db.api import OP_User
from ...tool import Currency, format_date


class LimitHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
        }
        ret = await G.tl_cli.send2tl('15020', data)
        if not ret['success']:
            return self.render('ccrd/limit.html', {'success': False})
        info_keys = ['success', 'ACCT_OTB', 'ACCT_LIMIT', 'ACCT_CASH_OTB']
        context = {key.lower(): value for key, value in ret.items() if key in info_keys}
        return self.render('ccrd/limit.html', **context)
