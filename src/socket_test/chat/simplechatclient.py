# coding=utf-8
from __future__ import print_function

import socket
import threading
from ast import literal_eval

from src.socket_test.chat.util import *

COMMAND_MSG_TYPE = 'Cmd'
MESSAGE_MSG_TYPE = 'Msg'

COMMAND_PREFIX = '/'

DEFAULT_RECEIVING_SIZE = 2048

SERVER_UID = 0
GUEST_UID = -1


class SimpleChatClient(object):
    _addr = None  # type:str
    _port = None  # type:int
    _sock = None  # type:socket.socket

    _uid = GUEST_UID  # type:int
    _receivers = []  # type:list[int]

    _is_connected = False  # type:bool

    _send_buffer = []  # type: [Message]
    _recv_msg_buffer = []  # type: [Message]
    _cmd_buffer = []  # type: [Message]

    _unknow_type_msg_storage = {}  # type: {str:[Message]}

    _msg_recv_thread = None  # type: threading.Thread
    _msg_send_thread = None  # type: threading.Thread
    _console_input_thread = None  # type: threading.Thread
    _cmd_exec_thread = None  # type: threading.Thread

    _commands = []  # type: [Command]

    _users = {}

    def __init__(self, server_addr, server_port):
        # type: (str, int) -> None
        self._addr = server_addr
        self._port = server_port
        self._sock = socket.socket()
        self._uid = GUEST_UID
        self._receivers = []
        self._send_buffer = []
        self._recv_msg_buffer = []
        self._cmd_buffer = []  # type: list[Message]
        self._unknow_type_msg_storage = {}
        self._users = {}

        self._msg_recv_thread = threading.Thread(target=self.recv_thread_process,
                                                 name='Message Receiving')
        self._msg_send_thread = threading.Thread(target=self.send_thread_process,
                                                 name='Message Sending')
        self._console_input_thread = threading.Thread(target=self.input_thread_process,
                                                      name='Console Input')
        self._cmd_exec_thread = threading.Thread(target=self.cmd_exec_thread_process,
                                                 name='Command Execution')

        # Initialize commands
        self.add_cmd(Command('getuid', self.get_uid, Command.GUEST))
        self.add_cmd(Command('setuid', self.set_uid, Command.SERVER))
        self.add_cmd(Command('e', exec, Command.LOCAL))
        self.add_cmd(Command('?', self.get_cmd_list, Command.LOCAL))
        self.add_cmd(Command('setusers', self.set_user_nicks, Command.SERVER))
        # TODO self.add_cmd(Command('updateusers'))
    def connect(self):
        # Connect to server
        try:
            self._sock.connect((self._addr, self._port))
        except socket.error as e:
            print('Failed to connect to server (%s:%d):' % (self._addr, self._port))
            print(e)
            return
        print('Connection approved.')
        self._is_connected = True
        self._cmd_exec_thread.start()
        print('%s thread activated.' % self._cmd_exec_thread.name)
        self._console_input_thread.start()
        print('%s thread activated.' % self._console_input_thread.name)
        self._msg_recv_thread.start()
        print('%s thread activated.' % self._msg_recv_thread.name)
        self._msg_send_thread.start()
        print('%s thread activated.' % self._msg_send_thread.name)

    def send_raw(self, str_msg:str):
        try:
            self._sock.sendall(str_msg.encode('utf-8'))
        except socket.error as e:
            print('Error occurred while sending message to server.')

    def send(self, msg:Message):
        self.send_raw(repr(msg))

    def send_thread_process(self):
        while self._is_connected:
            if len(self._send_buffer) > 0:
                msg = self._send_buffer.pop(0)
                # if message receiver is self, not send it to server
                if msg.get_field('Receivers') == [self._uid]:
                    self.distribute_message(msg)
                else:
                    self.send(msg)

    def recv_raw(self, size: int=DEFAULT_RECEIVING_SIZE) -> str or None:
        try:
            return str(self._sock.recv(size), 'utf-8')
        except socket.error as e:
            print('Error occurred while receiving message from server.')
            return None

    def recv(self) -> Message or None:
        data = self.recv_raw()
        try:
            return Message.parse_str(data)
        except SyntaxError as e:
            print('Error occurred while parsing message from server.')
            print('Raw data received: \n%s' % data)
            return None

    def recv_thread_process(self):
        while self._is_connected:
            msg = self.recv()
            if not msg is None:
                self.distribute_message(msg)

    def get_console_input(self):
        return input()

    def process_input(self, s:str):
        # type: (str) -> None
        # if input is a command, execute it
        if s.startswith(COMMAND_PREFIX):
            # Generate a new command message and insert to local buffer
            self._cmd_buffer.insert(0, Message(
                {'Sender': self._uid, 'Receivers': [self._uid], 'Type': COMMAND_MSG_TYPE,
                 'Message': s[1:]}))
        else:
            # if input can be parsed to a Message object, parse and send it
            try:
                self._send_buffer.append(Message.parse_str(s))
            except SyntaxError as e:
                # if cannot be parsed, send it as normal message
                msg = Message(
                    {'Sender': self._uid, 'Receivers': self._receivers, 'Type': MESSAGE_MSG_TYPE,
                     'Message': s})
                self._send_buffer.append(msg)

    def input_thread_process(self):
        while self._is_connected:
            input_str = self.get_console_input()
            self.process_input(input_str)

    def cmd_exec_thread_process(self):
        while self._is_connected:
            if len(self._cmd_buffer) > 0:
                # Get command info
                cmd_msg = self._cmd_buffer.pop(0)
                cmd_text = cmd_msg.get_field('Message')  # type:str
                cmd_text = cmd_text.split(' ', 2)
                cmd_ref = cmd_text[0]
                cmd_args = []
                if len(cmd_text) > 1:
                    cmd_args = cmd_text[1].split(' ')
                # Looking for command
                cmds = self.get_cmd_list()
                if cmd_ref not in cmds.keys():  # if command not found
                    msg = Message({'Sender': self._uid, 'Receivers': [cmd_msg.get_field('Sender')],
                                   'Type': MESSAGE_MSG_TYPE,
                                   'Message': 'Unable to execute command: Command "%s" not found.' % cmd_ref})
                    self._send_buffer.append(msg)
                else:
                    cmd = cmds.get(cmd_ref)
                    # Verify the permission to execute command
                    if self.verify_execution(cmd_msg, cmd):
                        # Execute the command and get the result
                        result = self.execute_cmd(cmd, cmd_args)
                        if not result is None:
                            msg = Message(
                                {'Sender': self._uid, 'Receivers': [cmd_msg.get_field('Sender')],
                                 'Type': MESSAGE_MSG_TYPE,
                                 'Message': result})
                            self._send_buffer.append(msg)

    def verify_execution(self, msg:Message, cmd:Command) -> bool:
        executer = msg.get_field('Sender')
        if executer == SERVER_UID and cmd.level <= Command.SERVER:
            return True
        elif executer == self.get_uid() and cmd.level <= Command.LOCAL:
            return True
        elif cmd.level <= Command.GUEST:
            return True
        return False

    def execute_cmd(self, cmd:Command, params:list=None) -> str:
        try:
            if params is None or type(params) is not list:
                return repr(cmd.execute())
            else:
                return repr(cmd.execute(*params))
        except Exception as e:
            return repr(e)

    def distribute_message(self, msg: Message):
        msg_type = msg.get_field('Type')
        if msg_type == MESSAGE_MSG_TYPE:
            self._recv_msg_buffer.append(msg)
            self.disp_msg(msg)
        elif msg_type == COMMAND_MSG_TYPE:
            self._cmd_buffer.append(msg)
        else:  # Unknown type message
            self._handle_unknow_type_msg(msg)

    def _handle_unknow_type_msg(self, msg:Message):
        if not msg.get_field('Type') in self._unknow_type_msg_storage.keys():
            self._unknow_type_msg_storage[msg.get_field('Type')] = [msg]
        else:
            self._unknow_type_msg_storage.get(msg.get_field('Type')).append(msg)

    def disp_msg(self, msg:Message) -> None:
        sender = self._users.get(msg.get_field('Sender'))
        nick = ''
        if sender is not None and self._users.get(sender) is not None:
            nick = self._users.get(sender)
        print('[%d]%s: %s' % (sender, nick, msg.get_field('Message'))) # Expected

    def set_uid(self, uid:int or str) -> None:
        # (This function was used by a command)
        uid = int(uid)
        if uid == SERVER_UID or uid == GUEST_UID:
            raise ValueError('Cannot use %d as your id.' % uid)
        else:
            self._uid = int(uid)

    def get_uid(self) -> int:
        # (This function was used by a command)
        return self._uid

    def get_cmd_list(self) -> {str:Command}:
        # (This function was used by a command)
        cmds = {}
        for cmd in self._commands:
            cmds[cmd.cmd_ref] = cmd
        return cmds

    def set_user_nicks(self, users:dict or str) -> None:
        # (This function was used by a command)
        if type(users) == str:
            users = literal_eval(users)
        self._users = users

    def get_user_nick(self, uid:int = None) -> str or None:
        if uid == None:
            uid = self.get_uid()
        return self._users.get(uid)

    def add_cmd(self, cmd:Command):
        self._commands.append(cmd)

client = SimpleChatClient('localhost', 10086)
client.connect()
