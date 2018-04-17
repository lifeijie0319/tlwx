#-*- coding:utf-8 -*-
import os

from tornado.web import StaticFileHandler

from . import config
from .view import common
from .view import wx
from .view.ccrd import online_apply


url_patterns = [
    (r'/tlwx', common.RootHandler),
    (r'/tlwx/([^/]+\.[^/]+)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/media/(.*)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/staticfile/(.*)', common.StaticTPLHandler),
    #(r'/tlwx/test/(?P<action>\w+)', common.TestHandler),
    (r'/tlwx/common/send_vcode', common.SendVcodeHandler),
    (r'/tlwx/common/refresh_pic_vcode', common.RefreshPicVcodeHandler),
    (r'/tlwx/common/upload_img', common.UploadImgHandler),
    (r'/tlwx/wx/jssdk', wx.JSSDKHandler),
    (r'/tlwx/wx/refresh_token', wx.RefreshTokenHandler),
    (r'/tlwx/wx/refresh_menu', wx.RefreshMenuHandler),
    (r'/tlwx/wx/upload_img', wx.UploadImgHandler),
    (r'/tlwx/ccrd/online_apply/(?P<page>\d?)', online_apply.PageHandler),
    (r'/tlwx/ccrd/online_apply/status/(?P<page>\d?)', online_apply.StatusPageHandler),
    #(r'/tlwx/ccrd/online_apply/upload_idcard', online_apply.UploadIDCardHandler),
]
