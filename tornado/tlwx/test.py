#-*- coding:utf-8 -*-
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line

from app.tool import init_G
from app.wx_tpl_msg import send_trade_detail


@coroutine
def main():
    openid = 'oSDTiwq1vFtLARyBeBGhRpNeXczA'
    data = {
        'date': '2015年6月16日 10:20',
        'type': '收入/支出500元',
        'balance': '300元',
        'summary': '手机银行',
    }
    yield send_trade_detail(openid, data)


if __name__ == '__main__':
    parse_command_line()
    init_G()
    IOLoop.current().run_sync(main)
