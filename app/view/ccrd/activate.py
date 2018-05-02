#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ...db.api import OP_CredentialType
from ...tool import get_doc, G
from ...service.rsa import rsa_decrypt


class ActivateHandler(BaseHandler):
    @need_openid
    async def get(self):
        credential_types = OP_CredentialType(self.db).get()
        context = {
            'credential_types': credential_types,
            'protocol': get_doc('protocol.txt')
        }
        self.render('ccrd/activate.html', **context)

    async def post(self):
        app_log.debug('REQ: %s', self.request.body)
        data = rsa_decrypt(self.request.body)
        data = json.loads(data)
        vcode = data.pop('vcode')
        res = self.check_vcode(vcode)
        if not res['success']:
            return self.write(res)
        req = {
            'CARD_NO': data['ccrdno'],
            'EXPIRE_DATE': data['expire'],
            'CVV2': data['cvv2'],
        }
        app_log.info('[REQ] %s', req)
        ret = await G.tl_cli.send2tl('14040', req)
        if not ret['success']:
            return self.write(ret)
        else:
            return self.write({'success': True})
