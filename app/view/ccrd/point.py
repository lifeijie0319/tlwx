#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_bind, need_openid
from ...config import G
from ...db.api import OP_User
from ...tool import Currency, format_date


class PointHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
        }
        ret = await G.tl_cli.send2tl('17010', data)
        if not ret['success']:
            return self.render('ccrd/point.html', {'success': False})
        info_keys = ['success', 'POINT_BAL', 'CTD_EARNED_POINTS']
        context = {key.lower(): value for key, value in ret.items() if key in info_keys}
        return self.render('ccrd/point.html', **context)


class DetailHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        return self.render('ccrd/point_detail.html')

    async def post(self):
        req_data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        tl_data = {
            'CARD_NO': user.ccrdno,
            'START_DATE': req_data.get('START_DATE'),
            'END_DATE': req_data.get('END_DATE'),
            'FIRSTROW': req_data['firstrow'],
            'LASTROW': req_data['lastrow']
        }
        ret = await G.tl_cli.send2tl('17011', tl_data)
        info_keys = ['success', 'ACQ_NAME_ADDR', 'SETT_TXN_TYPE', 'TXN_AMT', 'POINT']
        context = {key.lower(): value for key, value in ret.items() if key in info_keys}
        currency = Currency(ret['CURR_CD'])
        context = dict(context, txn_date=format_date(ret['TXN_DATE']))
        context = {
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)
