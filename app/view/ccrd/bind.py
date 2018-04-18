#-*- coding:utf-8 -*-
import json

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ...db.model import User
from ...tool import G
#from ... import config


class BindHandler(BaseHandler):
    @need_openid
    async def get(self):
        self.render('ccrd/bind.html')
    async def post(self):
        app_log.debug('REQ: %s', self.request.body)
        data = json.loads(self.request.body)
        action = data.pop('action')
        if action == 'info_check':
            service_id = '11010'
            request = {
                'CARD_NO': data['ccrdno'],
                'OPT': 0,
            }
            ret = await G.tl_cli.send_request(service_id, request)
            app_log.debug('[R] %s', ret)
            status = ret['SERVICE']['SERVICE_HEADER']['SERV_RESPONSE']['STATUS']
            if status != 'S':
                return self.write({'success': False, 'msg': '客户信息不存在，请确定卡是否已激活'})
            response = ret['SERVICE']['SERVICE_BODY']['RESPONSE']
            if response['ID_NO'] != data['idno']:
                return self.write({'success': False, 'msg': '卡号对应的证件号与输入的证件号不匹配'})
            if not response['MOBILE_NO']:
                return self.write({'success': False, 'msg': '获取不到手机号'})
            return self.write({'success': True, 'cellphone': response['MOBILE_NO']})
        elif data.get('action') == 'submit':
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
