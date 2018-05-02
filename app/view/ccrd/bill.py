#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_bind, need_openid
from ...config import G
from ...db.api import OP_User
from ...tool import Currency, format_date


class BillHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
            'STMT_DATE': '000000',
        }
        ret = await G.tl_cli.send2tl('12010', data)
        if not ret['success']:
            return self.render('ccrd/bill.html', {'success': False})
        info_keys = ['success', 'QUAL_GRACE_BAL', 'TOT_DUE_AMT', 'CTD_PMT_NOT_AMT']
        context = {key.lower(): value for key, value in ret.items() if key in info_keys}
        currency = Currency(ret['CURR_CD'])
        context = dict(context, **{
            'billing_date': format_date(ret['BILLING_DATE']),
            'pmt_due_date': format_date(ret['PMT_DUE_DATE']),
            'curr_symbol': currency.symbol,
            'curr_name': currency.name,
        })
        return self.render('ccrd/bill.html', **context)

    async def post(self):
        req_data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        tl_data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
            'STMT_DATE': '000000',
            'FIRSTROW': req_data['firstrow'],
            'LASTROW': req_data['lastrow']
        }
        ret = await G.tl_cli.send2tl('12011', tl_data)
        app_log.debug('BILL_DETAIL: %s\n%s', ret['TXNS'], type(ret['TXNS']))
        if not ret.get('TXNS'):
            return self.write({'html': '', 'nextpage': False})
        items = ret['TXNS']['TXN']
        if not isinstance(items, list):
            items = [items]
        html = self.render_string('ccrd/bill_detail.html', **{
            'items':[{
                'curr_symbol': Currency(item['TXN_CURR_CD']).symbol,
                'txn_date': format_date(item['TXN_DATE']),
                'ccrdno_tail': item['TXN_CARD_NO'][-4:],
                'txn_amt': item['TXN_AMT'],
                'txn_short_desc': item['TXN_SHORT_DESC']
            } for item in items]
        })
        context = {
            'success': True,
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)


class BillDueHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        return self.render('ccrd/bill_due.html')
    async def post(self):
        req_data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        tl_data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
            'SETT_TXN_TYPE': '',
            'FIRSTROW': req_data['firstrow'],
            'LASTROW': req_data['lastrow']
        }
        ret = await G.tl_cli.send2tl('13060', tl_data)
        if not ret['success']:
            return self.write(ret)
        if not ret.get('TXNS'):
            return self.write({'html': '', 'nextpage': False})
        app_log.debug('BILL_DETAIL: %s\n%s', ret['TXNS']['TXN'], type(ret['TXNS']['TXN']))
        items = ret['TXNS']['TXN']
        if not isinstance(items, list):
            items = [items]
        html = self.render_string('ccrd/bill_due_list.html', **{
            'items':[{
                'curr_symbol': Currency(item['TXN_CURR_CD']).symbol,
                'txn_date': format_date(item['TXN_DATE']),
                'txn_card_no': item['TXN_CARD_NO'][-4:],
                'txn_amt': item['TXN_AMT'],
                'txn_short_desc': item['TXN_SHORT_DESC']
            } for item in items]
        })
        context = {
            'success': True,
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)
