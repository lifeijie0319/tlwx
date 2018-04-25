#-*- coding:utf-8 -*-
import json

from tornado.log import app_log
from urllib.parse import urlencode

from ..common import BaseHandler, need_bind, need_openid
from ... import config
from ...tool import Currency, G, xml_format
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
        if not ret['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
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
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('12012', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)


class CashHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        self.render('ccrd/installment_cash.html')

    async def post(self):
        data = json.loads(self.request.body)
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('12012', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}


class ConsumptionHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        self.render('ccrd/installment_consumption.html')

    async def post(self):
        req_data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        tl_data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
            'FIRSTROW': req_data['firstrow'],
            'LASTROW': req_data['lastrow']
        }
        ret = await G.tl_cli.send2tl('13081', tl_data)
        html = self.render_string('ccrd/installment_consumption_list.html', **{
            'items':[{
                'txn_curr_cd': Currency(item['TXN_CURR_CD']).symbol,
                'txn_amt': item['TXN_AMT'],
                'txn_date': xml_format(item['TXN_DATE'], 'date'),
                'txn_time': xml_format(item['TXN_TIME'], 'time'),
                'ccrdno_tail': item['TXN_CARD_NO'][-4:],
                'txn_short_desc': item['TXN_SHORT_DESC']
            } for item in ret['TXNS']['TXN']]
        })
        context = {
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)


class ConsumptionFormHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        amount = self.get_argument('amt')
        self.render('ccrd/installment_consumption_form.html', **{'amount': amount})

    async def post(self):
        data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('13082', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)
