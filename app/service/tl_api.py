import datetime
import dicttoxml
import json
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

    async def send2tl(self, service_id, data):
        data = self.format_xml(service_id, data)
        ret = await self.send(data)
        ret = xmltodict.parse(ret)
        serv_response = ret['SERVICE']['SERVICE_HEADER']['SERV_RESPONSE']
        if serv_response['STATUS'] == 'F':
            return {'success': False, 'msg': serv_response['DESC']}
        response = ret['SERVICE']['SERVICE_BODY']['RESPONSE']
        if response:
            response['success'] = True
        else:
            response = {'success': True}
        return response

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
        app_log.info('[R]: %s', ret.decode())
        return ret.decode()


class TLImageClient:
    def __init__(self, cli, config):
        self.cli = cli
        self.org = config['ORG']
        self.sys_id = config['SYS_ID']
        self.operator_id = config['OPERATOR_ID']
        self.url = 'http://' + config['HOST'] + ':' + config['PORT']

    async def send(self, data, url, method='POST'):
        #app_log.info('[S] %s', data)
        data = json.dumps(data, ensure_ascii=False)
        headers = {'Content-Type': 'application/json'}
        res = await self.cli.fetch(self.url + url, method=method, body=data, headers=headers)
        if res.error:
            res.rethrow()
        app_log.info('[R] %s', res.body)
        return res.body
        
    async def get_image_no(self, name, id_no, id_type):
        data = {
            'ORG': self.org,
            'ID_TYPE': id_type,
            'ID_NO': id_no,
            'NAME': name,
            'SYS_ID': self.sys_id,
            'OPERATOR_ID': self.operator_id
        }
        #return {'RET_CODE': 'F', 'RET_MSG': '获取影像批次号失败'}
        return {"IMAGE_NO":"aps.2018050811215607164dc9zS00000","RET_CODE":"S"}
        #return await self.send(data, '/api/v1/img/id')

    async def add(self, name, id_no, id_type, image_no, images):
        data = {
            'ORG': self.org,
            'ID_TYPE': id_type,
            'ID_NO': id_no,
            'NAME': name,
            'SYS_ID': self.sys_id,
            'IMAGE_NO': image_no,
            'OPERATOR_ID': self.operator_id,
            'images': images
        }
        #return {'RET_CODE': 'F', 'RET_MSG': '新增影像失败'}
        return {"IMAGE_NO":"aps.2018050715580502264dc9zS00000","RET_CODE":"S"}
        #return await self.send(data, '/api/v1/img/org1/' + image_no)

    async def query(self, image_no):
        data = {
            'IMAGE_NO': image_no,
            'ORG': self.org,
            'SYS_ID': self.sys_id,
            'OPERATOR_ID': self.operator_id,
        }
        app_log.info('DATA: %s', data)
        ret = await self.send(data, '/api/v1/img/info')
        return ret
