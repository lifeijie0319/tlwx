import datetime
import dicttoxml
import xmltodict

from tornado.log import app_log
from tornado.tcpclient import TCPClient

from ..tool import gen_req_token


class TLClient:
    def __init__(self, host, port, header_length=6):
        self.host = host
        self.port = port
        self.header_length = header_length

    def format_xml(self, service_id, request):
        XML_HEADER = '<?xml version="1.0" encoding="UTF-8" ?><SERVICE xmlns="http://www.allinfinance.com/dataspec/">'
        XML_FOOTER = '</SERVICE>'
        ext_attributes = {}
        service_header = {
            'SERVICE_SN': gen_req_token(),
            'SERVICE_ID': service_id,
            'ORG': '000069411200',
            'CHANNEL_ID': '07',
            'OP_ID': '',
            'REQUST_TIME': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            'VERSION_ID': '01',
            'MAC': '',
        }
        service_body = {'EXT_ATTRIBUTES': ext_attributes, 'REQUEST': request}
        main = {'SERVICE_HEADER': service_header, 'SERVICE_BODY': service_body}
        xml = XML_HEADER + (dicttoxml.dicttoxml(main, attr_type=False, root=False)).decode() + XML_FOOTER
        app_log.debug('XML TYPE: %s', type(xml))
        return xml.encode('utf-8')

    async def send_request(self, service_id, request):
        data = self.format_xml(service_id, request)
        ret = await self.send(data)
        return xmltodict.parse(ret)

    def add_prefix(self, data):
        return str(len(data)).zfill(self.header_length).encode('utf-8') + data

    async def send(self, data):
        tl_cli = await TCPClient().connect(self.host, self.port)
        data = self.add_prefix(data)
        app_log.info('[S]: %s', data)
        tl_cli.write(data)
        ret_len = await tl_cli.read_bytes(self.header_length)
        app_log.info('[R]: %s', ret_len)
        ret = await tl_cli.read_bytes(int(ret_len))
        app_log.info('[R]: %s', ret)
        return ret.decode()
