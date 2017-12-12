# coding=utf-8
from src.socket_test.chat.command import Command
from src.socket_test.chat.message import Message


def parse_type(s):
    # type: (str) -> type or None
    known_types = {'int':int,'str':str, 'bool':bool, 'float':float, 'Message':Message, 'Command':Command}
    if s in known_types.keys():
        return known_types.get(s)
    return None