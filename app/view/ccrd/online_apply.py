#-*- coding:utf-8 -*-
import tornado.web

from tornado.log import app_log

from ..common import BaseHandler, need_openid
from ... import config


class PageHandler(BaseHandler):
    @need_openid
    def get(self, page=1):
        app_log.debug('%s %s', page, type(page))
        return self.render('ccrd/online_apply' + page + '.html')


class StatusPageHandler(BaseHandler):
    def get(self, page=1):
        app_log.debug('%s %s', page, type(page))
        return self.render('ccrd/online_apply_status' + page + '.html')


#class UploadIDCardHandler(BaseHandler):
#    def post(self):
#        openid = get_openid(self)
#        front_id = self.get_argument('front_id')
#        back_id = self.get_argument('back_id')
#        res1 = self.download_file(front_id, config.MEDIA_PATH + '/front_id/', openid)
#        if not res1.get('success'):
#            return self.write({'success': False, 'msg': '身份证前面影像提交失败'})
#        res2 = self.download_file(back_id, config.MEDIA_PATH + '/back_id/', openid)
#        if not res2.get('success'):
#            return self.write({'success': False, 'msg': '身份证后面影像提交失败'})
#        return self.write({'success': True})
#
#    def download_file(self, mediaid, path, filename):
#        res = get_tmp_media(mediaid)
#        if res.get('success'):
#            with open(path + filename + '.jpg', 'wb') as f:
#                f.write(res.get('content'))
#            res = {'success': True}
#        return res
