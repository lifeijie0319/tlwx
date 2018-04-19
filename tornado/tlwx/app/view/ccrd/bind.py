#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ...config import G, BASE_URL
from ...db.api import OP_User
from ...db.model import User


class BindHandler(BaseHandler):
    @need_openid
    async def get(self):
        if OP_User(self.db).check_bind(self.openid):
            return self.redirect(BASE_URL + '/staticfile/done.html?from=binded')
        else:
            self.render('ccrd/bind.html')
    async def post(self):
        app_log.debug('REQ: %s', self.request.body)
        data = json.loads(self.request.body)
        data['openid'] = self.openid
        idno = data.pop('idno')
        vcode = data.pop('vcode')
        res = self.check_vcode(vcode)
        if res['success']:
            user = OP_User(self.db).get(self.openid)
            if user:
                user.binded = True
            else:
                OP_User(self.db).create(data)
            self.db.commit()
            self.write({'success': True})
        else:
            self.write(res)


class UnbindHandler(BaseHandler):
    @need_openid
    async def get(self):
        user = OP_User(self.db).get(self.openid)
        if user and user.binded:
            ccrdno = user.ccrdno
            cus_info = await G.tl_cli.api_11010(ccrdno)
            if not cus_info['success']:
                raise Exception(cus_info['msg'])
            cellphone = cus_info['MOBILE_NO']
            idno = cus_info['ID_NO']
            context = {
                'idtype': '身份证',
                'idno': idno[:4] + '*' * (len(idno) - 8) + idno[-4:],
                'ccrdno': ccrdno[:4] + '*' * (len(ccrdno) - 8) + ccrdno[-4:],
                'name': cus_info['NAME'],
                'cellphone': cellphone[:3] + '****' + cellphone[-4:],
            }
            return self.render('ccrd/unbind.html', **context)
        else:
            return self.redirect(BASE_URL + '/staticfile/done.html?from=unbinded')
    def post(self):
        user = OP_User(self.db).get(self.openid)
        if user and user.binded:
            user.binded = False
            self.db.commit()
            self.write({'success': True})
        else:
            self.write({'success': False, 'msg': '您已经解绑，请不要重复提交'})
