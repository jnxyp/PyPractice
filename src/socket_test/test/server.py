# coding=utf-8
import socket
import threading
import time


def echo(sock, addr):
    # type: (socket, str) -> None
    buffer = []
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        if data == 'exit' or not data:
            break
        buffer.append(data)
        sock.send(str(buffer))
    sock.close()
    print 'Connection from ' + str(addr) + ' closed.'


DEFAULT_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 10086
DEFAULT_PROCESS = echo


class Server(object):
    socket = None

    def __init__(self, connection_process=DEFAULT_PROCESS, address=DEFAULT_ADDRESS, port=DEFAULT_PORT,
                 max_connection=1):
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((address, port))
        print 'Socket binded on ' + address + ':' + str(port)

        self.socket = s

    def start(self, backlog=1):
        self.socket.listen(backlog)
        print 'Waiting for connection...'

        while True:
            sock, addr = self.socket.accept()
            print type(sock)
            print type(self.socket)
            print 'Accepted connection from' + str(addr)
            t = threading.Thread(target=DEFAULT_PROCESS, args=(sock, addr))
            t.start()


server = Server()
server.start()
