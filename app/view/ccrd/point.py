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
        app_log.debug('\nREQ: %s\n', req_data)
        user = OP_User(self.db).get(self.openid)
        start = req_data.get('start')
        start = start.replace('-', '') if start else None
        end = req_data.get('end')
        end = end.replace('-', '') if end else None
        tl_data = {
            'CARD_NO': user.ccrdno,
            'START_DATE': start,
            'END_DATE': end,
            'FIRSTROW': req_data['firstrow'],
            'LASTROW': req_data['lastrow']
        }
        ret = await G.tl_cli.send2tl('17011', tl_data)
        if not ret.get('TXN_POINTS'):
            return self.write({'html': '', 'nextpage': False})
        items = ret['TXN_POINTS']['TXN_POINT']
        if not isinstance(items, list):
            items = [items]
        html = self.render_string('ccrd/point_detail_list.html', **{
            'items':[{
                'txn_date': format_date(item['TXN_DATE']),
                'acq_name_addr': item['ACQ_NAME_ADDR'],
                'sett_txn_type': item['SETT_TXN_TYPE'],
                'txn_amt': item['TXN_AMT'],
                'point': item['POINT']
            } for item in items]
        })
        context = {
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)
