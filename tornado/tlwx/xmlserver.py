import datetime
import dicttoxml
import json
import redis
import xmltodict

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.log import app_log
from tornado.options import parse_command_line
from tornado.tcpserver import TCPServer

from app import config
from app.tool import gen_req_token, G
from app.db.api import OP_User
from app.db.sqlal import Session
from app.service.tl_api import TLClient
from app.wx_msg import TPL


class XMLServer(TCPServer):
    def __init__(self, header_length: int = 6):
        super().__init__()
        self.stream = None
        self.header_length = header_length
        G.redis_conn = redis.StrictRedis(host=config.REDIS.get('HOST'), port=config.REDIS.get('PORT'), db=0)
        G.async_http_cli = AsyncHTTPClient()

    async def handle_stream(self, stream, address):
        app_log.info('Connection from peer: {}'.format(address))
        self.stream = stream
        try:
            while True:
                length = await stream.read_bytes(self.header_length)
                app_log.info(length)
                msg = await stream.read_bytes(int(length))
                app_log.info('[R] %s', msg)
                data = await self.process_data(msg.decode())
                data = str(len(data)).zfill(self.header_length).encode('utf-8') + data
                app_log.info('[S] %s', data)
                await stream.write(data)
                del msg  # Dereference msg in case it's big.
        except StreamClosedError:
            app_log.info('{} disconnected'.format(address))

    async def process_data(self, data):
        data = xmltodict.parse(data)
        app_log.info(data)
        try:
            service_id = data['SERVICE']['SERVICE_HEADER']['SERVICE_ID']
            app_log.debug('service_id %s', service_id)
            if service_id == '91000':
                req = data['SERVICE']['SERVICE_BODY']['REQUEST']
                app_log.info('91000 REQ: %s', req)
                ret = self.process_trade_detail(req)
                service_header = {
                    'SERVICE_SN': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                    'SERVICE_ID': '91000',
                    'ORG': '000069411200',
                    'SERVICE_TIME': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                    'SERV_RESPONSE': ret
                }
                XML_HEADER = '<?xml version="1.0" encoding="UTF-8" ?><SERVICE xmlns="http://www.allinfinance.com/dataspec/">'
                XML_FOOTER = '</SERVICE>'
                main = {'SERVICE_HEADER': service_header, 'SERVICE_BODY': None}
                app_log.debug('main: %s', main)
                xml = XML_HEADER + (dicttoxml.dicttoxml(main, attr_type=False, root=False)).decode() + XML_FOOTER
            else:
                with open('./app/tpl/xml/' + service_id + '.xml', 'r') as f:
                    xml = f.read()
            return xml.encode('utf-8')
        except Exception as e:
            app_log.exception(e)
            raise

    def process_trade_detail(self, req):
        session = Session()
        app_log.debug('CARD_NO: %s', req['CARD_NO'])
        user = OP_User(session).get_by_ccrdno(req['CARD_NO'])
        app_log.debug('USER: %s', user)
        openid = None
        if user and user.binded:
            openid = user.openid
            date = datetime.datetime.strptime(req['TRANS_TIME'], '%m%d%H%M%S').strftime('%m月%d日 %H:%M:%S')
            data = {
                'date': date,
                'type': config.TRADE_TYPE[req['TRANS_TYPE']],
                'balance': '￥ ' + req['TRANS_AMT'],
                'summary': config.TRADE_TYPE[req['TRANS_TYPE']],
            }
            TPL.send_trade_detail(openid, data)
            ret = {
                'STATUS': 'S',
                'CODE': '00',
                'DESC': '',
            }
        else:
            ret = {
                'STATUS': 'F',
                'CODE': '14',
                'DESC': '卡号未绑定',
            }
        session.close()
        return ret


parse_command_line()
loop = IOLoop.current()
server = XMLServer()
server.listen(8001)
loop.start()
