#-*- coding:utf-8 -*-
import json
import tornado.web

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ... import config
from ...db.api import OP_CCRDOnlineApply


def check_apply(func):
    async def wrapper(self, *args, **kwargs):
        items = OP_CCRDOnlineApply(self.db).get(self.openid)
        if len(items) > 1:
            return self.redirect(config.BASE_URL + '/select')
        elif len(items) == 1:
            status = items[0].status
            mapper = {
                '基本信息': 'base_info',
                '身份证': 'id_card',
                '概述': 'profile',
                '工作信息': 'job_info',
                '住宅信息': 'house_info',
                '其他信息': 'other_info',
                '人脸识别': 'face_check',
            }
            tail = mapper[status]
            self.set_secure_cookie('product_cd', items[0].product_cd)
            current = self.request.path.split('/')[-1]
            if current == tail:
                await func(self, *args, **kwargs)
            else:
                return self.redirect(config.BASE_URL + '/ccrd/online_apply/' + tail)
        else:
            current = self.request.path.split('/')[-1]
            if current == 'choice':
                await func(self, *args, **kwargs)
            else:
                return self.redirect(config.BASE_URL + '/ccrd/choice')
    return wrapper


class PageHandler(BaseHandler):
    def get(self, page=1):
        return self.render('ccrd/online_apply' + page + '.html')


class ChoiceHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        return self.render('ccrd/online_apply/main_choice.html')

    def post(self):
        data = json.loads(self.request.body)
        data['openid'] = self.openid
        app_log.info('REQ: %s', data)
        self.set_secure_cookie('product_cd', data['product_cd'])
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
        product_cd = self.get_secure_cookie('product_cd').decode()
        app_log.info('PRODUCT_TYPE: %s', product_cd)
        data['status'] = '身份证'
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class IDCardHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        return self.render('ccrd/online_apply/main_id_card.html')

    def post(self):
        product_cd = self.get_secure_cookie('product_cd').decode()
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, {'status': '概述'})
        self.db.commit()
        return self.write({'success': True})


class ProfileHandler(BaseHandler):
    @need_openid
    @check_apply
    async def get(self):
        product_cd = self.get_secure_cookie('product_cd').decode()
        item = OP_CCRDOnlineApply(self.db).get(self.openid, product_cd=product_cd)
        context = {
            'name': item.name,
            'id_no': item.id_no,
            'cellphone': item.cellphone,
        }
        return self.render('ccrd/online_apply/main_profile.html', **context)

    async def post(self):
        data = json.loads(self.request.body)
        data.pop('if_serve_ever')
        data['id_start_date'] = data['id_start_date'].replace('-', '')
        data['id_last_date'] = data['id_last_date'].replace('-', '')
        data['status'] = '工作信息'
        app_log.info('REQ: %s', data)
        product_cd = self.get_secure_cookie('product_cd').decode()
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
        data['status'] = '住宅信息'
        app_log.info('REQ: %s', data)
        product_cd = self.get_secure_cookie('product_cd').decode()
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
        data['status'] = '其他信息'
        app_log.info('REQ: %s', data)
        product_cd = self.get_secure_cookie('product_cd').decode()
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
        data['status'] = '人脸识别'
        data['sm_amt_verify_ind'] = 'Y' if data.get('sm_amt_verify_ind') else 'N'
        app_log.info('REQ: %s', data)
        product_cd = self.get_secure_cookie('product_cd').decode()
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
        data['status'] = '其他信息'
        app_log.info('REQ: %s', data)
        product_cd = self.get_secure_cookie('product_cd').decode()
        OP_CCRDOnlineApply(self.db).update(self.openid, product_cd, data)
        self.db.commit()
        return self.write({'success': True})


class StatusPageHandler(BaseHandler):
    def get(self, page=1):
        app_log.debug('%s %s', page, type(page))
        return self.render('ccrd/online_apply_status' + page + '.html')
