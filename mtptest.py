from configparser import ConfigParser

from twx.mtproto import client


config = ConfigParser()
config.read_file(open('mtproto.conf'))

client = client.MTProtoClient(config)
client.init()

