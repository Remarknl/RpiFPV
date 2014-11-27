#!/usr/bin/env python

import socket
import time
import serial

TCP_IP = '127.0.0.1'
TCP_PORT = 61271
BUFFER_SIZE = 1024
SERIAL_CONNECTION = serial.Serial('/dev/ttyUSB0', 9600)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
    for x in range(0, 3000):
        s.send("getInputs")
        data = s.recv(BUFFER_SIZE).split(",", 2)
        SERIAL_CONNECTION.write(data[0])
        SERIAL_CONNECTION.write(',')
        SERIAL_CONNECTION.write(data[1])
        SERIAL_CONNECTION.write(',')
        SERIAL_CONNECTION.write(data[2])
        SERIAL_CONNECTION.write(',')
        SERIAL_CONNECTION.write(data[3])
        SERIAL_CONNECTION.write(';')
        time.sleep(0.03)
s.close()