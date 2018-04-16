#-*- coding:utf-8 -*-
import os

from tornado.web import StaticFileHandler

from . import config
from .view import common
from .view import wx
from .view.credit_card import online_apply


url_patterns = [
    (r'/tlwx', common.RootHandler),
    (r'/wxdemo/([^/]+\.[^/]+)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/media/(.*)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/staticfile/(.*)', common.StaticTPLHandler),
    (r'/tlwx/test/(?P<action>\w+)', common.TestHandler),
    (r'/tlwx/common/send_vcode', common.SendVcodeHandler),
    (r'/tlwx/common/refresh_pic_vcode', common.RefreshPicVcodeHandler),
    (r'/tlwx/common/upload_img', common.UploadImgHandler),
    (r'/tlwx/wx/jssdk', wx.JSSDKHandler),
    (r'/wxdemo/wx/refresh_token', wx.RefreshTokenHandler),
    (r'/tlwx/wx/refresh_menu', wx.RefreshMenuHandler),
    (r'/tlwx/wx/upload_img', wx.UploadImgHandler),
    (r'/tlwx/credit_card/online_apply/page/(?P<page>\d?)', online_apply.PageHandler),
    (r'/tlwx/credit_card/online_apply/status/page/(?P<page>\d?)', online_apply.StatusPageHandler),
    (r'/tlwx/credit_card/online_apply/upload_idcard', online_apply.UploadIDCardHandler),
]
