from configparser import ConfigParser

from twx.mtproto import client
import asyncio

asyncio.get_event_loop().set_debug(True)

config = ConfigParser()
config.read_file(open('mtproto.conf'))

client = client.MTProtoClient(config)
client.init()

