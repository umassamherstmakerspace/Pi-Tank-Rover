# coding: utf-8


import os
from socket import *
from controls import *
import logging as log
import argparse
import time
import RPi.GPIO as GPIO
import sys

p = argparse.ArgumentParser(description='Process some integers.')
p.add_argument("-v","--verbose", help="increase output verbosity",
                    action="store_true")

args = p.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


####################################################################
####################################################################
####################################################################
####################################################################

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

controls = Controller()
####################################################################
####################################################################
####################################################################
####################################################################

IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

####################################################################
####################################################################
####################################################################
####################################################################

def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

max_speed = 100

def run(delaytime, speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(max_speed*speed)
    pwm_ENB.ChangeDutyCycle(max_speed*speed)
    time.sleep(delaytime)


def processData(data):
    forwardSpeed = -1 * data[controls.leftYAxis]
    run(1, forwardSpeed)
    

####################################################################
####################################################################
####################################################################
####################################################################


motor_init()

log.info("Waiting to receive messages...")
while 1:
    (data, addr) = UDPSock.recvfrom(buf)
    log.info("Received message: " + data)

    data = list(data.split(","))
    data = [float(i) for i in data]

    processData(data)
    if data[controls.select] == 1:
        UDPSock.close()
        log.warning("[    MISSION STATUS     ]: System exit")
        raise SystemExit

UDPSock.close()
os._exit(0)

