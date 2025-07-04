#!/usr/bin/env python3

import socket

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( ("localhost", 8000) )
    # Happens with HTTP/1.1 as well
    s.send(b"GET / HTTP/1.0\r\n\r\n")
    s.recv(255)
    s.close()

