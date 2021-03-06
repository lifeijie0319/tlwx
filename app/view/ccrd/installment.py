#-*- coding:utf-8 -*-
import json

from tornado.log import app_log
from urllib.parse import urlencode

from ..common import BaseHandler, need_bind, need_openid
from ... import config
from ...tool import Currency, get_doc, G, xml_format
from ...db.api import OP_User


class BillHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data1 = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156',
            'STMT_DATE': '000000',
        }
        ret1 = await G.tl_cli.send2tl('12010', data1)
        if not ret1['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret1['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
        data2 = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156'
        }
        ret2 = await G.tl_cli.send2tl('13110', data2)
        if not ret2['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret2['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
        info_keys = ['LOAN_INIT_TERM', 'LOAN_AMT']
        items = ret2['TERMS']['TERM']
        app_log.info('items: %s', items)
        context = {
            'qual_grace_bal': ret1['QUAL_GRACE_BAL'],
            'items': [{key.lower(): value for key, value in item.items() if key in info_keys} for item in items],
            'protocol': get_doc('protocol.txt')
        }
        self.render('ccrd/installment/bill.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('12012', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN', 'LOAN_FIXED_FEE1']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)


class CashHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
            'CURR_CD': '156'
        }
        ret = await G.tl_cli.send2tl('13140', data)
        if not ret['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
        info_keys = ['LOAN_INIT_TERM', 'LOAN_AMT']
        items = ret['TERMS']['TERM']
        app_log.info('items: %s', items)
        context = {
            'items': [{key.lower(): value for key, value in item.items() if key in info_keys} for item in items],
            'protocol': get_doc('protocol.txt')
        }
        self.render('ccrd/installment/cash.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('13084', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN', 'LOAN_FIXED_FEE1']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)


class LGCashHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        data = {
            'LOAN_CODE': '2005',
        }
        ret = await G.tl_cli.send2tl('13004', data)
        if not ret['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
        info_keys = ['LOAN_INIT_TERM', 'MAX_AMOUNT']
        items = ret['LOANFEEDEFS']['LOANFEEDEF']
        context = {
            'items': [{key.lower(): value for key, value in item.items() if key in info_keys} for item in items],
            'protocol': get_doc('protocol.txt')
        }
        self.render('ccrd/installment/lg_cash.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('13160', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN', 'LOAN_FIXED_FEE1']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)


class ConsumptionHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        self.render('ccrd/installment/consumption.html')

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
        if not ret['success']:
            return self.write(ret)
        if not ret.get('TXNS'):
            return self.write({'success': True, 'html': '', 'nextpage': False})
        html = self.render_string('ccrd/installment/consumption_list.html', **{
            'items':[{
                'txn_curr_cd': Currency(item['TXN_CURR_CD']).symbol,
                'txn_amt': item['TXN_AMT'],
                'ref_nbr': item['REF_NBR'],
                'txn_date': xml_format(item['TXN_DATE'], 'date'),
                'txn_time': xml_format(item['TXN_TIME'], 'time'),
                'ccrdno_tail': item['TXN_CARD_NO'][-4:],
                'txn_short_desc': item['TXN_SHORT_DESC']
            } for item in ret['TXNS']['TXN']]
        })
        context = {
            'success': True,
            'html': html.decode(),
            'nextpage': True if ret['NEXTPAGE_FLG'] == 'Y' else False
        }
        return self.write(context)


class ConsumptionFormHandler(BaseHandler):
    @need_openid
    @need_bind
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        data = {
            'CARD_NO': user.ccrdno,
        }
        ret = await G.tl_cli.send2tl('13000', data)
        if not ret['success']:
            url = config.BASE_URL + '/staticfile/done.html?from=error'
            url += '&' + urlencode({'error_msg': ret['msg']})
            app_log.debug('URL: %s', url)
            return self.redirect(url)
        info_keys = ['LOAN_INIT_TERM', 'MIN_AMOUNT', 'MAX_AMOUNT']
        items = ret['LOANFEEDEFS']['LOANFEEDEF']
        context = {
            'items': [{key.lower(): value for key, value in item.items() if key in info_keys} for item in items],
            'protocol': get_doc('protocol.txt'),
            'txn_amt': self.get_argument('txn_amt')
        }
        self.render('ccrd/installment/consumption_form.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        user = OP_User(self.db).get(self.openid)
        data['CARD_NO'] = user.ccrdno
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.send2tl('13082', data)
        if not ret['success']:
            return self.write(ret)
        else:
            info_keys = ['success', 'LOAN_INIT_FEE1', 'LOAN_FIXED_PMT_PRIN', 'LOAN_FIXED_FEE1']
            context = {key.lower(): value for key, value in ret.items() if key in info_keys}
            return self.write(context)
