#!/usr/bin/env python

import socket
import pygame
import os

# headless shit
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.display.init()
screen = pygame.display.set_mode((1,1))

# joystick shit
pygame.joystick.init()
_joystick = pygame.joystick.Joystick(0)
_joystick.init()

TCP_IP = '0.0.0.0'
TCP_PORT = 61271
BUFFER_SIZE = 20
INPUTS = [2, 3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    pygame.event.get()
    INPUTS[0] = str(int(round(_joystick.get_axis(0)*500+500)))
    INPUTS[1] = str(int(round(_joystick.get_axis(1)*500+500)))
    
    
    data = conn.recv(BUFFER_SIZE)
    if data:
        print "received data:", data
        conn.send(','.join(map(str, INPUTS)))  # echo
        
    if data == 'exit':
        break
conn.close()
