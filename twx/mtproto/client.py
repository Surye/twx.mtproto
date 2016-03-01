from twx.mtproto.session import MTProtoSession
from twx.mtproto.dc import DataCenter
import asyncio

class MTProtoClient:
    def __init__(self, config, session_id=None):

        self.api_id = config.get('app', 'api_id')
        self.api_hash = config.get('app', 'api_hash')
        self.app_title = config.get('app', 'app_title')
        self.short_name = config.get('app', 'short_name')

        self.public_keys = config.get('servers', 'public_keys')

        self.test_dc = DataCenter(config.get('servers', 'test_dc'))
        self.production_dc = DataCenter(config.get('servers', 'production_dc'))

        # if self.use_test_dc:
        self.datacenter = self.test_dc
        # else:
        #     self.datacenter = self.productinn_dc

        # self.datacenter = dc.DataCenter('tcp://127.0.0.1:8888')

        if session_id is None:
            self.session = MTProtoSession.new()
            print('creating new session: {}'.format(self.session))
        else:
            self.session = MTProtoSession(session_id)
            print('continuing session: {}'.format(self.session))

    @asyncio.coroutine
    def run(self, loop):
        while True:
            # self.get_nearest_dc()
            print("Test")
            yield from asyncio.sleep(1)

    def init(self):
        asyncio.ensure_future(self.run(asyncio.get_event_loop()))