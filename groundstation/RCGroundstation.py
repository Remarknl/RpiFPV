#!/usr/bin/env python

import socket
import pygame
import os

# trims
trimChannel1 = 0
trimChannel2 = 0
trimChannel3 = 0
trimChannel4 = 0

enable = 0

# headless pygame shit
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
INPUTS = [0, 1, 2, 3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 13:
                trimChannel2 = trimChannel2 + 10
            if event.button == 14:
                trimChannel2 = trimChannel2 - 10
            if event.button == 12:
                trimChannel3 = trimChannel3 + 10
            if event.button == 11:
                trimChannel3 = trimChannel3 - 10
            if event.button == 7:
                enable = 500
    
    chan1 = int(round(_joystick.get_axis(1) * enable + enable + trimChannel1))
    chan2 = int(round(_joystick.get_axis(4) * 500 + 500 + trimChannel2))
    chan3 = int(round(_joystick.get_axis(3) * 500 + 500 + trimChannel3))
    chan4 = int(round(_joystick.get_axis(0) * 500 + 500 + trimChannel4))
    if chan1 > 1000: chan1 = 1000
    if chan1 < 0: chan1 = 0
    if chan2 > 1000: chan2 = 1000
    if chan2 < 0: chan2 = 0
    if chan3 > 1000: chan3 = 1000
    if chan3 < 0: chan3 = 0
    if chan4 > 1000: chan4 = 1000
    if chan4 < 0: chan4 = 0
    
    chan1 = 1000 - chan1
    
    INPUTS[0] = str(chan1)
    INPUTS[1] = str(chan2)
    INPUTS[2] = str(chan3)
    INPUTS[3] = str(chan4)
    
    
    data = conn.recv(BUFFER_SIZE)
    if data:
        #print "received data:", data
        conn.send(','.join(map(str, INPUTS)))
        
    if data == 'exit':
        break
conn.close()
