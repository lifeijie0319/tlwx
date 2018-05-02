#-*- coding:utf-8 -*-
import base64
import json

from tornado.log import app_log
from tornado.web import MissingArgumentError

from ..common import BaseHandler, need_openid
from ... import config
from ...db.api import OP_CCRDOnlineApply
from ...tool import G


def check_apply(func):
    async def wrapper(self, *args, **kwargs):
        items = OP_CCRDOnlineApply(self.db).get(self.openid)
        if len(items) >= 1:
            product_cd = self.get_cookie('product_cd')
            if not product_cd:
                return self.redirect(config.BASE_URL + '/ccrd/online_apply/select')
            step = 'choice'
            for item in items:
                app_log.info('product_cd: %s %s', item.product_cd, product_cd)
                if item.product_cd == product_cd:
                    step = item.step
                    break
            tail = self.request.path.split('/')[-1]
            if tail == step:
                return await func(self, *args, **kwargs)
            else:
                return self.redirect(config.BASE_URL + '/ccrd/online_apply/' + step)
        else:
            return self.redirect(config.BASE_URL + '/ccrd/online_apply/choice')
    return wrapper


class PageHandler(BaseHandler):
    def get(self, page=1):
        return self.render('ccrd/online_apply' + page + '.html')


class SelectHandler(BaseHandler):
    @need_openid
    async def get(self):
        items = OP_CCRDOnlineApply(self.db).get(self.openid)
        app_log.info('items: %s', items)
        if not items:
            return self.redirect(config.BASE_URL + '/ccrd/online_apply/choice')
        mapper = {
            'base_info': '基本信息',
            'id_card': '身份证上传',
            'profile': '概况',
            'job_info': '工作信息',
            'house_info': '住宅信息',
            'other_info': '其他信息',
            'face_check': '人脸识别'
        }
        return self.render('ccrd/online_apply/main_select.html', items=items, mapper=mapper)


class ChoiceHandler(BaseHandler):
    @need_openid
    async def get(self):
        return self.render('ccrd/online_apply/main_choice.html')

    def post(self):
        data = json.loads(self.request.body)
        data['openid'] = self.openid
        app_log.info('REQ: %s', data)
        OP_CCRDOnlineApply(self.db).create(data)
        self.db.commit()
        return self.write({'success': True})


class BaseInfoHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        return self.render('ccrd/online_apply/main_base_info.html', id_types=config.ID_TYPE)

    async def post(self):
        data = json.loads(self.request.body)
        vcode = data.pop('vcode')
        res = self.check_vcode(vcode)
        if not res['success']:
            return self.write(res)
        OP_CCRDOnlineApply(self.db).get(self.openid)
        product_cd = self.get_cookie('product_cd')
        app_log.info('PRODUCT_TYPE: %s', product_cd)
        data['step'] = 'id_card'
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class IDCardHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        return self.render('ccrd/online_apply/main_id_card.html')

    def post(self):
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, {'step': 'profile'})
        self.db.commit()
        return self.write({'success': True})


class ProfileHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        product_cd = self.get_cookie('product_cd')
        item = OP_CCRDOnlineApply(self.db).get(self.openid, product_cd=product_cd)[0]
        context = {
            'name': item.name,
            'id_no': item.id_no,
            'cellphone': item.cellphone,
        }
        return self.render('ccrd/online_apply/main_profile.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        data['if_serve_ever'] = 'Y' if data.get('if_serve_ever') else 'N'
        data['id_start_date'] = data['id_start_date'].replace('-', '')
        data['id_last_date'] = data['id_last_date'].replace('-', '')
        data['step'] = 'job_info'
        app_log.info('REQ: %s', data)
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class JobInfoHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        context = {
            'emp_structures': config.EMP_STRUCTURE,
            'emp_types': config.EMP_TYPE,
            'emp_posts': config.EMP_POST,
            'title_of_technicals': config.TITLE_OF_TECHNICAL,
        }
        return self.render('ccrd/online_apply/main_job_info.html', **context)

    def post(self):
        data = json.loads(self.request.body)
        ssx = data.pop('ssx')
        data['emp_province'], data['emp_city'], data['emp_zone'] = ssx.split(' ')
        data['step'] = 'house_info'
        app_log.info('REQ: %s', data)
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class HouseInfoHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        context = {
            'house_ownerships': config.HOUSE_OWNERSHIP,
            'contact_relations': config.CONTACT_RELATION,
        }
        return self.render('ccrd/online_apply/main_house_info.html', **context)

    def post(self):
        data = json.loads(self.request.body)
        ssx = data.pop('ssx')
        data['home_state'], data['home_city'], data['home_zone'] = ssx.split(' ')
        data['step'] = 'other_info'
        app_log.info('REQ: %s', data)
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class OtherInfoHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        context = {
            'marital_statuses': config.MARITAL_STATUS,
            'qualifications': config.QUALIFICATION,
            'stmt_media_types': config.STMT_MEDIA_TYPE,
            'card_fetch_methods': config.CARD_FETCH_METHOD,
            'card_mailer_inds': config.CARD_MAILER_IND,
        }
        return self.render('ccrd/online_apply/main_other_info.html', **context)

    def post(self):
        data = json.loads(self.request.body)
        data['step'] = 'face_check'
        data['sm_amt_verify_ind'] = 'Y' if data.get('sm_amt_verify_ind') else 'N'
        app_log.info('REQ: %s', data)
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class FaceCheckHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        return self.render('ccrd/online_apply/main_face_check.html')

    def post(self):
        data = json.loads(self.request.body)
        ssx = data.pop('ssx')
        data['home_state'], data['home_city'], data['home_zone'] = ssx.split(' ')
        data['step'] = 'other_info'
        app_log.info('REQ: %s', data)
        product_cd = self.get_cookie('product_cd')
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class StatusHandler(BaseHandler):
    def get(self, action):
        if action == 'form':
            return self.render('ccrd/online_apply/status.html', id_types=config.ID_TYPE)
        elif action == 'list':
            data = self.get_cookie('ccrd_online_apply_status')
            data = base64.b64decode(data)
            data = json.loads(data)
            app_log.info('DATA: %s', data)
            return self.render('ccrd/online_apply/status_list.html', items=data)
        elif action == 'detail':
            app_no = self.get_argument('app_no')
            data = self.get_cookie('ccrd_online_apply_status')
            data = base64.b64decode(data)
            data = json.loads(data)
            for item in data:
                if item['APP_NO'] == app_no:
                    context = item
                    break
            app_log.info('DETAIL: %s', context)
            return self.render('ccrd/online_apply/status_detail.html', **context)

    async def post(self, action):
        data = json.loads(self.request.body)
        pic_vcode = data.pop('pic_vcode')
        real_pic_vcode = self.get_secure_cookie('pic_vcode').decode()
        app_log.debug('PIC_VCODE_COMPARE: %s %s', pic_vcode, real_pic_vcode)
        if pic_vcode != real_pic_vcode:
            return self.write({'success': False, 'msg': '图片验证码错误'})
        ret = await G.tl_cli.send2tl('11000', data)
        if not ret.get('APPLYS'):
            return self.write({'success': False, 'msg': '没有数据'})
        items = ret['APPLYS']['APPLY']
        if not isinstance(items, list):
            items = [items]
        mapper = {
            'APPLY10': '申请已受理',
            'L05': '成功申请',
            'M05': '失败申请'
        }
        for item in items:
            item['STATUS'] = mapper[item['RTF_STATE']]
        data = json.dumps(items, ensure_ascii=False).encode('utf-8')
        app_log.info('DATA: %s', type(data))
        data = base64.b64encode(data)
        self.set_cookie('ccrd_online_apply_status', data)
        return self.write({'success': True})
