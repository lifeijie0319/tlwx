#-*- coding:utf-8 -*-
import logging
import redis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.httpclient import AsyncHTTPClient, HTTPClient
from tornado.options import define, options
from dicttoxml import LOG

from app.config import G, REDIS, TL_AIC, TL_IMAGE, tornado_settings, URL_PREFIX
from app.service.tl_api import TLClient, TLImageClient
from app.url import url_patterns


define('port', default=8002, help='run on the given port', type=int)
LOG.setLevel(logging.WARNING)


class Application(tornado.web.Application):
    def __init__(self):
        G.redis_conn = redis.StrictRedis(host=REDIS.get('HOST'), port=REDIS.get('PORT'), db=0)
        G.http_cli = HTTPClient()
        G.async_http_cli = AsyncHTTPClient()
        G.tl_cli = TLClient(TL_AIC['HOST'], TL_AIC['PORT'])
        G.tl_image_cli = TLImageClient(G.async_http_cli, TL_IMAGE)
        handlers = url_patterns
        tornado.web.Application.__init__(self, handlers, **tornado_settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
