#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ...db.model import User
from ...tool import G
#from ... import config


class ActivateHandler(BaseHandler):
    @need_openid
    async def get(self):
        self.render('ccrd/activate.html')
    def post(self):
        data = json.loads(self.request.body)
        #idno = self.get_argument('idno')
        #ccrdno = self.get_argument('ccrdno')
        #cellphone = self.get_argument('cellphone')
        #vcode = self.get_argument('vcode')
        data['openid'] = self.c_openid
        idno = data.pop('idno')
        vcode = data.pop('vcode')
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.write({'success': True})


class UnbindHandler(BaseHandler):
    @need_openid
    async def get(self):
        idno = '330721197003019372'
        ccrdno = '12345678909876543211'
        telno = '13392749392'
        context = {
            'idtype': '身份证',
            'idno': idno[:4] + '*' * (len(idno) - 8) + idno[-4:],
            'ccrdno': ccrdno[:4] + '*' * (len(ccrdno) - 8) + ccrdno[-4:],
            'name': '张三',
            'telno': telno[:3] + '****' + telno[-4:],
        }
        self.render('ccrd/unbind.html', **context)
    def post(self):
        user = self.db.query(User).filter(User.openid==self.c_openid).one_or_none()
        if user:
            user.binded = False
            self.db.commit()
            self.write({'success': True})
            return
        else:
            self.write({'success': False, 'msg': '您已经解绑，请不要重复提交'})
