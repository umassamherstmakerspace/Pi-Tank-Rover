import os
from socket import *
from controls import *
import logging as log
import argparse
import time
import RPi.GPIO as GPIO
import sys
import math

p = argparse.ArgumentParser(description='Process some integers.')
p.add_argument("-v","--verbose", help="increase output verbosity",
                    action="store_true")

args = p.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


####################################################################
####################################################################
####################################################################
####################################################################

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

controls = Controller()
####################################################################
####################################################################
####################################################################
####################################################################

IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

ServoPinCam = 23
ServoPinMount = 26
####################################################################
####################################################################
####################################################################
####################################################################

def motor_init():
    global pwm_ENA
    global pwm_ENB
    global pwm_servoCam
    global pwm_servoMount
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    GPIO.setup(ServoPinCam, GPIO.OUT)
    pwm_servoCam = GPIO.PWM(ServoPinCam, 50)
    pwm_servoCam.start(0)
    GPIO.setup(ServoPinMount, GPIO.OUT)
    pwm_servoMount = GPIO.PWM(ServoPinMount, 50)
    pwm_servoMount.start(0)

max_speed = 100

def run(delaytime, speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(max_speed*speed)
    pwm_ENB.ChangeDutyCycle(max_speed*speed)

def runLeft(delaytime, speed, dir):
    d = math.fabs(dir)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(max_speed*speed)
    pwm_ENB.ChangeDutyCycle(max_speed*speed * (1-d))

def runRight(delaytime, speed, dir):
    d = math.fabs(dir)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(max_speed*speed * (1-d))
    pwm_ENB.ChangeDutyCycle(max_speed*speed)

def backward(delaytime, speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(-1 * max_speed*speed)
    pwm_ENB.ChangeDutyCycle(-1 * max_speed*speed)

def backwardLeft(delaytime, speed,dir):
    d = math.fabs(dir)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(-1 * max_speed*speed * (1-d))
    pwm_ENB.ChangeDutyCycle(-1 * max_speed*speed)

def backwardRight(delaytime, speed, dir):
    d = math.fabs(dir)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(-1 * max_speed*speed)
    pwm_ENB.ChangeDutyCycle(-1 * max_speed*speed * (1-d))

def pivotLeft():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(max_speed)
    pwm_ENB.ChangeDutyCycle(max_speed) 

def pivotRight():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(max_speed)
    pwm_ENB.ChangeDutyCycle(max_speed)



pos = 60
pos2 = 50
def processData(data):
    global pos
    global pos2
    pos += 40 * data[controls.buttonOffset+controls.rightYAxis]
    pwm_servoCam.ChangeDutyCycle(2.5 + 10 * pos/180)	

    pos2 += 40 * data[controls.buttonOffset+controls.rightXAxis]
    pwm_servoMount.ChangeDutyCycle(2.5 + 10 * pos2/180)	


    if (data[controls.left] == 1):
        pivotLeft()
        return
    if (data[controls.right] == 1):
        pivotRight()
        return

    forwardSpeed = -1 * data[controls.buttonOffset+controls.leftYAxis]
    horizontalSpeed = -1 * data[controls.buttonOffset+controls.leftXAxis]
    if forwardSpeed > 0 and math.fabs(horizontalSpeed) < .1:
        run(1, forwardSpeed)
    elif forwardSpeed > 0 and horizontalSpeed > 0:
        runLeft(1, forwardSpeed, horizontalSpeed)
    elif forwardSpeed > 0 and horizontalSpeed < 0:
        runRight(1, forwardSpeed, horizontalSpeed)
    elif forwardSpeed < 0 and  math.fabs(horizontalSpeed) < .1:
        backward(1, forwardSpeed)
    elif forwardSpeed < 0 and horizontalSpeed > 0:
        backwardRight(1, forwardSpeed, horizontalSpeed)
    elif forwardSpeed < 0 and horizontalSpeed < 0:
        backwardLeft(1, forwardSpeed, horizontalSpeed)
    else:
        run(1, forwardSpeed)
    

####################################################################
####################################################################
####################################################################
####################################################################


motor_init()

log.info("Waiting to receive messages...")
while 1:
    (data, addr) = UDPSock.recvfrom(buf)
    log.info(data)

    data = list(data.split(","))
    data = [float(i) for i in data]
    # print(data)
    processData(data)
    if data[controls.select] == 1:
        UDPSock.close()
        log.warning("[    MISSION STATUS     ]: System exit")
        raise SystemExit

UDPSock.close()
os._exit(0)

