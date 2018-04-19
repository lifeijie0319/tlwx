import json
import xmltodict

from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.log import app_log
from tornado.options import parse_command_line
from tornado.tcpserver import TCPServer


class XMLServer(TCPServer):
    def __init__(self, header_length: int = 6):
        super().__init__()
        self.stream = None
        self.header_length = header_length

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
            with open('./app/tpl/xml/' + service_id + '.xml', 'r') as f:
                xml = f.read()
            return xml.encode('utf-8')
        except Exception as e:
            app_log.exception(e)
            raise


parse_command_line()
loop = IOLoop.current()
server = XMLServer()
server.listen(8001)
loop.start()
