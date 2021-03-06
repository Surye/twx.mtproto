import random

from collections import namedtuple

from twx.mtproto import tl

__all__ = ('MTProtoSession',)

class MTProtoSession(namedtuple('MTProtoSession', 'id')):

    def __new__(cls, id):
        return super().__new__(cls, tl.int64_c(id))

    @classmethod
    def new(cls):
        return cls(random.SystemRandom().getrandbits(64))
