#-*- coding:utf-8 -*-
import os

from tornado.web import StaticFileHandler

from . import config
from .view import common
from .view import root
from .view import wx
from .view.ccrd import activate
from .view.ccrd import bill
from .view.ccrd import bind
from .view.ccrd import installment
from .view.ccrd import limit
from .view.ccrd import online_apply
from .view.ccrd import point


url_patterns = [
    (r'/tlwx', root.RootHandler),
    (r'/tlwx/([^/]+\.[^/]+)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/media/(.*)', StaticFileHandler, {'path': config.MEDIA_PATH}),
    (r'/tlwx/staticfile/(.*)', common.StaticTPLHandler),
    (r'/tlwx/test/(?P<action>\w+)', common.TestHandler),
    (r'/tlwx/common/send_vcode', common.SendVcodeHandler),
    (r'/tlwx/common/refresh_pic_vcode', common.RefreshPicVcodeHandler),
    (r'/tlwx/common/upload_img', common.UploadImgHandler),
    (r'/tlwx/common/info_check', common.InfoCheckHandler),
    (r'/tlwx/wx/jssdk', wx.JSSDKHandler),
    (r'/tlwx/wx/refresh_token', wx.RefreshTokenHandler),
    (r'/tlwx/wx/refresh_menu', wx.RefreshMenuHandler),
    (r'/tlwx/wx/upload_img', wx.UploadImgHandler),
    (r'/tlwx/ccrd/online_apply/(?P<page>\d?)', online_apply.PageHandler),
    (r'/tlwx/ccrd/online_apply/status/(?P<page>\d?)', online_apply.StatusPageHandler),
    (r'/tlwx/ccrd/bind', bind.BindHandler),
    (r'/tlwx/ccrd/unbind', bind.UnbindHandler),
    (r'/tlwx/ccrd/activate', activate.ActivateHandler),
    (r'/tlwx/ccrd/bill', bill.BillHandler),
    (r'/tlwx/ccrd/bill_due', bill.BillDueHandler),
    (r'/tlwx/ccrd/limit', limit.LimitHandler),
    (r'/tlwx/ccrd/point', point.PointHandler),
    (r'/tlwx/ccrd/point/detail', point.DetailHandler),
    (r'/tlwx/ccrd/installment/bill', installment.BillHandler),
    (r'/tlwx/ccrd/installment/cash', installment.CashHandler),
    (r'/tlwx/ccrd/installment/consumption', installment.ConsumptionHandler),
    (r'/tlwx/ccrd/installment/consumption/form', installment.ConsumptionFormHandler),
    #(r'/tlwx/ccrd/online_apply/upload_idcard', online_apply.UploadIDCardHandler),
]
