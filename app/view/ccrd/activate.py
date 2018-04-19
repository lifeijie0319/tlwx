#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ...tool import G
from ...db.api import OP_CredentialType


class ActivateHandler(BaseHandler):
    @need_openid
    async def get(self):
        credential_types = OP_CredentialType(self.db).get()
        context = {
            'credential_types': credential_types,
        }
        self.render('ccrd/activate.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        app_log.info('[REQ] %s', data)
        ret = await G.tl_cli.api_14040(data['ccrdno'], data['expire'], data['cvv2'])
        if not ret['success']:
            return self.write(ret)
        else:
            return self.write({'success': True})
