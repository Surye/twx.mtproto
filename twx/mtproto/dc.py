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
    from . connection import MTProtoConnection, MTProtoTCPConnection
except SystemError:
    import tl
    import scheme
    from connection import MTProtoConnection, MTProtoTCPConnection

log = logging.getLogger(__name__)

class DCInfo(namedtuple('DCInfo', 'address, port, connection_type')):

    def __new__(cls, address, port, connection_type):
        return super().__new__(cls, ip_address(address), int(port), MTProtoConnection.ConnectionType(connection_type))

    @classmethod
    def new(cls, url):
        url = urlsplit(url)
        return cls(url.hostname, url.port, url.scheme.upper())

class DataCenter:
    def __init__(self, url):
        self.dc = DCInfo.new(url)
        self.conn = MTProtoConnection.new(self.dc.connection_type, self.dc.address, self.dc.port)
        self.last_msg_id = 0
        self.auth_key = None
        self.random = random.SystemRandom()

    def send_rpc_message(self, msg):
        self.conn.send_message(msg)
    
    def generate_message_id(self):
        msg_id = int(time() * 2**32)
        if self.last_msg_id > msg_id:
            msg_id = self.last_msg_id + 1
        while msg_id % 4 is not 0:
            msg_id += 1

        return msg_id

    @asyncio.coroutine
    def send_insecure_message(self, request):
        yield from self.conn.send_insecure_message(self.generate_message_id(), request)

    @asyncio.coroutine
    def create_auth_key(self):
        req_pq = scheme.req_pq(tl.int128_c(self.random.getrandbits(128)))
        yield from self.send_insecure_message(req_pq)

    @asyncio.coroutine
    def run(self, loop):
        asyncio.ensure_future(self.conn.run(loop), loop=loop)
        asyncio.ensure_future(self.create_auth_key(), loop=loop)

        while True:
            print('test')
            yield from asyncio.sleep(10)

