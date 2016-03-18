import logging
import asyncio
import random

from ipaddress import ip_address
from collections import namedtuple
from urllib.parse import urlsplit
from struct import Struct

from time import time

try:
    from . import tl
    from . import scheme
    from . connection import MTProtoConnection, TCPConnection
except SystemError:
    import tl
    import scheme
    from connection import MTProtoConnection, TCPConnection

log = logging.getLogger(__name__)

class DCInfo(namedtuple('DCInfo', 'address port connection_type')):

    def __new__(cls, address, port, connection_type):
        return super().__new__(cls, ip_address(address), int(port), MTProtoConnection.ConnectionType(connection_type))

    @classmethod
    def new(cls, url):
        url = urlsplit(url)
        return cls(url.hostname, url.port, url.scheme.upper())

class DataCenter:

    def __init__(self, url):
        self.dc = DCInfo.new(url)
        self.connection = TCPConnection(str(self.dc.address), self.dc.port)
        self.last_msg_id = 0
        self.auth_key = None
        self.random = random.SystemRandom()

    def init(self, loop):
        pass
        # self.conn = MTProtoConnection.new(self.dc_info.connection_type)
        # self.conn_coro = loop.create_connection(lambda: self.conn, str(self.dc_info.address), self.dc_info.port)

        # f1 = asyncio.async(self.conn_coro)
        # asyncio.async(self.run(loop))
        # f1.add_done_callback(lambda x: self.create_auth_key())
        # loop.run_until_complete(asyncio.wait(tasks))

    def send_rpc_message(self, msg):
        pass
        # self.conn.send_message(msg)
    
    def generate_message_id(self):
        msg_id = int(time() * 2**32)
        if self.last_msg_id > msg_id:
            msg_id = self.last_msg_id + 1
        while msg_id % 4 is not 0:
            msg_id += 1

        return msg_id

    @asyncio.coroutine
    def send_insecure_message(self, request):
        yield from self.connection.send_insecure_message(self.generate_message_id(), request)
        # self.conn.send_insecure_message(self.generate_message_id(), request)

    @asyncio.coroutine
    def create_auth_key(self):
        req_pq = scheme.req_pq(tl.int128_c(self.random.getrandbits(128)))
        yield from self.send_insecure_message(req_pq)
        # res_pq = tl.ResPQ.from_stream(BytesIO(self.recv_plaintext_message()))

        # assert nonce == res_pq.nonce

    @asyncio.coroutine
    def run(self, loop):
        asyncio.ensure_future(self.connection.run(loop), loop=loop)
        asyncio.ensure_future(self.create_auth_key(), loop=loop)

        while True:
            print('test')
            yield from asyncio.sleep(10)

if __name__ == '__main__':

    dc = DataCenter('tcp://149.154.167.40:443')

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(dc.run(loop), loop=loop)
    loop.run_forever()
    loop.close()

