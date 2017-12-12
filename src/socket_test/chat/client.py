# coding=utf-8
# from __future__ import print_function
import socket
import threading

def receive():
    while True:
        print('Receive: ' + s.recv(2048))


def send():
    while True:
        s.send(input('Send: '))

s = socket.socket()
s.connect(('127.0.0.1', 10086))

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()

