import pygame
import sys
import time
import socket

pygame.init()
 
pygame.joystick.init()
 
print(pygame.joystick.get_count())
_joystick = pygame.joystick.Joystick(0)
_joystick.init()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            print(event)
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0: # this is the x axis
                print(event.value)
            if event.axis == 5: # right trigger
                print(event.value)
    xdir = _joystick.get_axis(0)
    rtrigger = _joystick.get_axis(5)
	#deadzone
    if abs(xdir) < 0.2:
        xdir = 0.0
    if rtrigger < -0.9:
        rtrigger = -1.0