# coding=utf-8
from __future__ import print_function

import socket
import threading

from src.socket_test.chat.util import *

COMMAND_MSG_TYPE = 'Cmd'
MESSAGE_MSG_TYPE = 'Msg'
DEFAULT_RECEIVING_SIZE = 2048

COMMAND_PREFIX = '/'

DEFAULT_USER_LIMIT = 2
SERVER_UID = 0
GUEST_UID = -1

DEFAULT_ADDR = 'localhost'
DEFAULT_PORT = 10086


class SimpleChatServer(object):
    _is_active = False
    _sock = None  # type: socket.socket
    _uid = SERVER_UID

    _conn_handle_thread = None  # type:threading.Thread
    _msg_sending_thread = None  # type: threading.Thread
    _recv_msg_handle_thread = None  # type: threading.Thread
    _console_input_thread = None  # type: threading.Thread
    _cmd_exec_thread = None  # type: threading.Thread

    _avaliable_uids = []

    _users = []  # type: [SimpleChatServer.User]
    _send_buffer = []  # type: [Message]
    _cmd_buffer = []  # type: [Message]

    _unknow_type_msg_storage = {}  # type: {str:[Message]}

    _commands = []  # type: [Command]

    def __init__(self, address=DEFAULT_ADDR, port=DEFAULT_PORT, max_user=DEFAULT_USER_LIMIT,
                 uid=SERVER_UID):
        # Initialize variables
        self._uid = uid
        self._is_active = False
        self._avaliable_uids = []
        self._users = []  # type: [SimpleChatServer.User]
        self._send_buffer = []  # type: [Message]
        self._cmd_buffer = []  # type: [Message]
        self._unknow_type_msg_storage = {}  # type: {str:[Message]}

        # Initialize socket and bind to the port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket initialized.')
        self._sock.bind((address, port))
        print('Socket binded on %s.' % str(self._sock.getsockname()))
        self._avaliable_uids = list(range(1, max_user + 1))
        print('Connection limit: %d users' % max_user)

        # Initialize threads
        self._console_input_thread = threading.Thread(target=self.input_thread_process,
                                                      name='Console Input')
        self._cmd_exec_thread = threading.Thread(target=self.cmd_exec_thread_process,
                                                 name='Command Execution')
        self._conn_handle_thread = threading.Thread(
            target=self._conn_handle_thread_process,
            name='Connection Handle')
        self._recv_msg_handle_thread = threading.Thread(
            target=self._recv_msg_handle_thread_process,
            name='Message Collecting'
        )
        self._msg_sending_thread = threading.Thread(
            target=self._msg_send_thread_process,
            name='Message Sending')

        # Initialize commands
        self.add_cmd(Command('listu', self.get_user_names, Command.GUEST))

    def start(self):
        print('Starting the server!')
        # Set active statues
        self._is_active = True
        # Start port listening
        self._sock.listen(2)
        # Start threads
        self._cmd_exec_thread.start()
        print('%s thread activated.' % self._cmd_exec_thread.name)
        self._conn_handle_thread.start()
        print('%s thread activated.' % self._conn_handle_thread.name)
        self._recv_msg_handle_thread.start()
        print('%s thread activated.' % self._recv_msg_handle_thread.name)
        self._msg_sending_thread.start()
        print('%s thread activated.' % self._msg_sending_thread.name)
        self._console_input_thread.start()
        print('%s thread activated.' % self._console_input_thread.name)
        print('Server is now online!')

    def _conn_handle_thread_process(self):
        while self._is_active:
            # Accept new connection
            connection, address = self._sock.accept()
            print('Received connection request from %s' % str(address))
            uid = self.assign_uid()
            if uid is None:
                print('Connection refused, server is currently full.')
                msg = repr(Message(
                    {'Sender': SERVER_UID, 'Receivers': [GUEST_UID], 'Type': MESSAGE_MSG_TYPE,
                     'Message': 'Server is currently full.'}))
                connection.sendall(msg.encode('utf-8'))
                connection.close()
                continue
            print('Connection approved, assigned uid: [%d]' % uid)
            # Send welcome information
            msg_str = repr(Message(
                {'Sender': SERVER_UID, 'Receivers': [uid], 'Type': MESSAGE_MSG_TYPE,
                 'Message': 'Welcome, you are now connected.'}))
            connection.sendall(msg_str.encode('utf-8'))
            self._add_user(uid, connection)

    def _msg_send_thread_process(self):
        while self._is_active:
            if len(self._send_buffer) > 0:
                # pop a message from buffer
                msg = self._send_buffer.pop(0)
                receivers = msg.get_field('Receivers')
                if len(receivers) == 0:  # if receiver not given, send to everyone
                    for u in self._users:
                        # if user is not the sender of this message
                        if not u.get_uid() == msg.get_field('Sender'):
                            u.send(msg)
                else:  # send to the user in the receivers list
                    # TODO: Notify sender the receiver is not found
                    not_exist_receiver = []
                    for uid in receivers:  # Expected
                        receiver = self.get_user_by_id(uid)
                        if not receiver is None:
                            receiver.send(msg)
                        else:
                            not_exist_receiver.append(uid)

    def _recv_msg_handle_thread_process(self):
        while self._is_active:
            msgs = self._collect_recv_msg()
            for msg in msgs:
                self._distribute_message(msg)

    def _collect_recv_msg(self, del_msg=True):
        # Get one message from each users' message buffer
        # type: (bool) -> list[Message]
        msgs = []  # type: list[Message]
        for u in self._users:
            msg = u.get_recv_msg(del_msg=del_msg)
            if not msg is None:
                msgs.append(msg)
        return msgs

    def _distribute_message(self, msg):
        # type: (Message) -> None
        # Distribute messages by their 'type' field
        if msg.get_field('Type') == COMMAND_MSG_TYPE:
            self._cmd_buffer.append(msg)
        elif msg.get_field('Type') == MESSAGE_MSG_TYPE:
            self._send_buffer.append(msg)
        else:  # Unknow type message
            self._handle_unknow_type_msg(msg)

    def _handle_unknow_type_msg(self, msg):
        # type: (Message) -> None
        if not msg.get_field('Type') in self._unknow_type_msg_storage.keys():
            self._unknow_type_msg_storage[msg.get_field('Type')] = [msg]
        else:
            self._unknow_type_msg_storage.get(msg.get_field('Type')).append(msg)

    def get_console_input(self):
        return input()

    def process_input(self, s: str):
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
                    {'Sender': self._uid, 'Receivers': [], 'Type': MESSAGE_MSG_TYPE,
                     'Message': s})
                self._send_buffer.append(msg)

    def input_thread_process(self):
        while self._is_active:
            input_str = self.get_console_input()
            self.process_input(input_str)

    def cmd_exec_thread_process(self):
        while self._is_active:
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

    def verify_execution(self, msg: Message, cmd: Command) -> bool:
        executer = msg.get_field('Sender')
        if executer == SERVER_UID and cmd.level <= Command.SERVER:
            return True
        elif executer == self.get_uid() and cmd.level <= Command.LOCAL:
            return True
        elif cmd.level <= Command.GUEST:
            return True
        return False

    def execute_cmd(self, cmd: Command, params: list = None) -> str:
        try:
            if params is None or type(params) is not list:
                return repr(cmd.execute())
            else:
                return repr(cmd.execute(*params))
        except Exception as e:
            return repr(e)

    def _add_user(self, uid, connection, nick=None):
        # type: (int, socket._socketobject, str) -> bool
        # check if user already exist
        for u in self._users:
            if u.get_addr() == connection.getpeername():
                return False
        user = SimpleChatServer.User(self, uid, connection, nick)
        self._users.append(user)
        print('Added user %s[%d]' % (user.get_nick(), user.get_uid()))
        self.announce_user_list()
        return True

    def remove_user(self, user):
        # type: (SimpleChatServer.User) -> bool
        user.destory()
        try:
            self._users.remove(user)
        except SyntaxError:
            return False
        # Return the uid to the available uid list
        self._avaliable_uids.append(user.get_uid())
        print('Removed user %s[%d]' % (user.get_nick(), user.get_uid()))
        self.announce_user_list()
        return True

    def get_user_by_id(self, uid):
        # type: (int) -> SimpleChatServer.User or None
        for u in self._users:
            if u.get_uid() == uid:
                return u
        return None

    def get_user_names(self) -> dict:
        user_list = {}
        for u in self._users:
            user_list[u.get_uid()] = u.get_nick()
        return user_list

    def announce_user_list(self):
        u_list = self.get_user_names()
        msg = {'Sender': self._uid, 'Receivers': [], 'Type': COMMAND_MSG_TYPE,
               'Message': 'setusers %s' % repr(self.get_user_names())}
        self._send_buffer.append(msg)

    def get_uid(self) -> int:
        return self._uid

    def change_nick(self, uid, nick):
        # type: (int, str) -> bool
        u = self.get_user_by_id(uid)
        if u is None:
            return False
        u.set_nick(nick)
        return True

    def assign_uid(self):
        # type: () -> int or None
        if len(self._avaliable_uids) > 0:
            return self._avaliable_uids.pop(0)
        return None

    def is_active(self):
        # type: () -> bool
        return self._is_active

    def add_cmd(self, cmd: Command):
        self._commands.append(cmd)

    def get_cmd_list(self) -> {str: Command}:
        cmds = {}
        for cmd in self._commands:
            cmds[cmd.cmd_ref] = cmd
        return cmds

    class User(object):
        _uid = 0
        _nick = ''
        _server = None  # type: SimpleChatServer
        _conn = None  # type: socket._socketobject

        _isConnected = False

        _recv_msg_buffer = []  # type: list[Message]

        _msg_recv_thread = None  # type: threading.Thread

        def __init__(self, server, uid, connection, nick=None):
            # type: (SimpleChatServer, int, socket._socketobject, str) -> None
            # Initialize variables
            self._isConnected = False
            self._recv_msg_buffer = []  # type: list[Message]
            # If nickname is not given, use uid as the nick.
            if nick is None:
                nick = str(uid)
            self._server = server
            self._conn = connection
            self.set_nick(nick)
            self._isConnected = True
            self.set_uid(uid)
            self._msg_recv_thread = threading.Thread(target=self.recv_thread_process,
                                                     name='Message Receiving (%s[%d])' % (
                                                         self.get_nick(), self.get_uid()))
            self._msg_recv_thread.start()

        def set_nick(self, nick):
            # type: (str) -> None
            self._nick = nick

        def get_recv_msg(self, index=0, del_msg=True):
            # type: (int, bool) -> Message or None
            if len(self._recv_msg_buffer) > index:
                if del_msg:
                    return self._recv_msg_buffer.pop(index)
                else:
                    return self._recv_msg_buffer[index]
            return None

        def send(self, msg):
            # type: (Message) -> None
            self.send_raw(repr(msg))

        def send_raw(self, str_msg):
            # type: (str) -> None
            try:
                self._conn.sendall(str_msg.encode('utf-8'))
            except socket.error as e:
                print('Error occured while sending message to user %s[%d]' % (
                    self.get_nick(), self.get_uid()))
                # TODO: Only remove user if error happened many times
                (self._server.remove_user(self))

        def recv_raw(self, size=DEFAULT_RECEIVING_SIZE):
            # type: (int) -> str or None
            try:
                return str(self._conn.recv(size), 'utf-8')
            except socket.error as e:
                print('Error occurred while receiving message from user %s[%d]' % (
                    self.get_nick(), self.get_uid()))
                # TODO: Only remove user if error happened many times
                (self._server.remove_user(self))
                return None

        def recv(self):
            # type: ()-> Message or None
            data = self.recv_raw()
            try:
                msg = Message.parse_str(data)
            except SyntaxError as e:
                if self.is_connected():  # Ignore the error if user is not connected
                    print('Error occurred while parsing received data from user %s[%d]' % (
                        self.get_nick(), self.get_uid()))
                    print('Raw data received:\n%s' % str(data))
                return None
            if not msg.get_field('Sender') == self.get_uid():
                print(
                    'Error occurred while verifying message from user %s[%d]: Illegal Sender' % (
                        self.get_nick(), self.get_uid()))
                # Send notice to user
                self.send(
                    Message({'Sender': self._server.get_uid(), 'Receivers': [self.get_uid()],
                             'Type': MESSAGE_MSG_TYPE,
                             'Message': 'Error occurred while verifying your message: Sender is not you'}))
                return None
            else:
                return msg

        def recv_thread_process(self, size=DEFAULT_RECEIVING_SIZE):
            while self.is_connected():
                msg = self.recv()
                if not msg == None:
                    self._recv_msg_buffer.append(msg)

        def destory(self):
            self._isConnected = False
            self._recv_msg_buffer = []
            self._conn.close()

        def __del__(self):
            self.destory()

        def is_connected(self):
            return self._isConnected

        def set_uid(self, uid):
            # (This function was used by a command)
            uid = int(uid)
            if uid == SERVER_UID or uid == GUEST_UID:
                raise ValueError('Cannot use %d as user\'s id.' % uid)
            else:
                self._uid = int(uid)
                msg = Message(
                    {'Sender': self._server.get_uid(), 'Receivers': [self._uid],
                     'Type': COMMAND_MSG_TYPE,
                     'Message': 'setuid %d' % self._uid})
                self.send(msg)

        def get_uid(self):
            return self._uid

        def get_nick(self):
            return self._nick

        def get_addr(self):
            return self._conn.getpeername()


server = SimpleChatServer()
server.start()
