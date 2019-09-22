import pygame
import sys
import time
import socket
import os
from socket import *
import logging as log
import argparse
from controls import *

p = argparse.ArgumentParser(description='Process some integers.')
p.add_argument("-v","--verbose", help="increase output verbosity",
                    action="store_true")

args = p.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


pygame.init()
pygame.joystick.init()
if (pygame.joystick.get_count() == 0):
    log.error("No Device Connected")
    raise SystemExit

_joystick = pygame.joystick.Joystick(0)
log.info("[    XBOX STATUS     ]: Controller Init")
_joystick.init()
log.info("[    XBOX STATUS     ]: Init Successful")

####################################################################
####################################################################
####################################################################
####################################################################

host = "172.20.10.12" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

####################################################################
####################################################################
####################################################################
####################################################################

buttons_packet = [0] * 15
triggers_packet = [0] * 6
controls = Controller()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            b = event.dict['button']
            log.info("[    XBOX STATUS     ]: Joystick button pressed - {}".format(b))
            buttons_packet[b] = 1
        elif event.type == pygame.JOYBUTTONUP:
            b = event.dict['button']
            log.info("[    XBOX STATUS     ]: Joystick button released - {}".format(b))
            buttons_packet[b] = 0

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 4: 
                triggers_packet[controls.leftTrigger] = round(event.value,1)
            if event.axis == 5: 
                triggers_packet[controls.rightTrigger] = round(event.value,1)
            if event.axis == 0:
                triggers_packet[controls.leftXAxis] = round(event.value,1)
            if event.axis == 1:
                triggers_packet[controls.leftYAxis] = round(event.value,1)
            if event.axis == 2:
                triggers_packet[controls.rightXAxis] = round(event.value,1)
            if event.axis == 3:
                triggers_packet[controls.rightYAxis] = round(event.value,1)

    s = ""
    for i in buttons_packet:
        s += str(i) + ","
    for i in triggers_packet:
        s += str(i) + ","
    
    s = s[:-1]
    log.info("[     MISSION SEND    ]: " + s)
    s = s.encode()
    UDPSock.sendto(s, addr)

    if buttons_packet[controls.select] == 1:
        UDPSock.close()
        log.warning("[    MISSION STATUS     ]: System exit")
        raise SystemExit

