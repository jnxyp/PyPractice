# coding=utf-8
import socket

s = socket.socket()
s.connect(('127.0.0.1', 10086))

while True:
    print 'Receive: ' + s.recv(1024)
    s.send(raw_input('Send: '))