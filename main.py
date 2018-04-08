#-*- coding:utf-8 -*-
import redis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from app.config import tornado_settings
from app.tool import init_G
from app.url import url_patterns
from tornado.options import define, options


define('port', default=8002, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        init_G()
        handlers = url_patterns
        tornado.web.Application.__init__(self, handlers, **tornado_settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
