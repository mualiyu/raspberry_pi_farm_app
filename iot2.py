import RPi.GPIO as gpio
from random import randint
from gpiozero import DistanceSensor
from time import sleep

lF= 25
lB = 23
rF = 18
rB = 24
ls = 20
rs= 21
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(lF, gpio.OUT)
gpio.setup(lB, gpio.OUT)
gpio.setup(rF, gpio.OUT)
gpio.setup(rB, gpio.OUT)
gpio.setup(ls, gpio.OUT)
gpio.setup(rs, gpio.OUT)

def stop():
	gpio.output(lF, 0)
	gpio.output(lB, 0)
	gpio.output(rF, 0)
	gpio.output(rB, 0)
	print("Stop")

def moveForward():
	gpio.output(lF, 1)
	gpio.output(lB, 0)
	gpio.output(rF, 1)
	gpio.output(rB, 0)
	print("Moving forward......")

def moveBackward():
	gpio.output(lF, 0)
	gpio.output(lB, 1)
	gpio.output(rF, 0)
	gpio.output(rB, 1)
	sleep(2)
	print("Moving backward......")

def turnLeftForward():
	gpio.output(lF, 1)
	gpio.output(lB, 0)
	gpio.output(rF, 0)
	gpio.output(rB, 0)
	print("Turning left forward......")

def turnRightForward():
	gpio.output(lF, 0)
	gpio.output(lB, 0)
	gpio.output(rF, 1)
	gpio.output(rB, 0)
	print("Turning right forward......")
def turnLeftBackward():
	gpio.output(lF, 0)
	gpio.output(lB, 1)
	gpio.output(rF, 0)
	gpio.output(rB, 0)
	print("Turning left backward......")

def turnRightBackward():
	gpio.output(lF, 0)
	gpio.output(lB, 0)
	gpio.output(rF, 0)
	gpio.output(rB, 1)
	print("Turning right backward......")

sensor = DistanceSensor(echo=16, trigger=12)
dist_thr = 8
while True:
        dis = (sensor.distance * 100)
        sleep(0.15)
        try:                
                if dis < dist_thr :
                        rand = randint(1,4);
                        if rand == 1:
                                turnLeftForward()
                                sleep(2)
                        elif rand == 2:
                                turnRightForward()
                                sleep(2)
                        elif rand == 3:
                                turnLeftBackward()
                                sleep(2)
                        elif rand == 4:
                                turnRightBackward()
                                sleep(2)
                else :
                        moveForward()
        except KeyboardInterrupt:
             stop()
             break
stop()
