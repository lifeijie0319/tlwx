#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_bind, need_openid
from ...tool import G
from ...db.api import OP_User


class BillHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156'
        }
        ret = await G.tl_cli.send2tl('13110', data)
        app_log.info('账单可分期金额查询: %s', ret.items())
        info_keys = ['LOAN_INIT_TERM', 'LOAN_AMT']
        items = ret['TERMS']['TERM']
        app_log.info('items: %s', items)
        context = {'items': 
            [{key.lower(): value for key, value in item.items() if key in info_keys} for item in items]
        }
        self.render('ccrd/installment_bill.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.api_14040(data['ccrdno'], data['expire'], data['cvv2'])
        if not ret['success']:
            return self.write(ret)
        else:
            return self.write({'success': True})
