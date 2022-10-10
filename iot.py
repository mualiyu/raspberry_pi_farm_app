import RPi.GPIO as gpio
import time

from gpiozero import DistanceSensor
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(23, gpio.OUT)
gpio.setup(25, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(24, gpio.OUT)

def stop():
        gpio.output(25, 0)
        gpio.output(23, 0)
        gpio.output(24, 0)
        gpio.output(18, 0)
        #print("Stop")

def moveFoward():
        gpio.output(25, 1)
        gpio.output(23, 0)
        gpio.output(24, 1)
        gpio.output(18, 0)
        #print("Moving forward......")

def moveBackward():
	gpio.output(25, 0)
	gpio.output(23, 1)
	gpio.output(24, 0)
	gpio.output(18, 1)
	sleep(2)
	#print("Moving backward......")

def turnLeft():
        gpio.output(25, 0)
        gpio.output(23, 0)
        gpio.output(24, 1)
        gpio.output(18, 0)
        #print("Turning left......")



def turnRight():
        gpio.output(25, 1)
        gpio.output(23, 0)
        gpio.output(24, 0)
        gpio.output(18, 0)
        #print("Turning right......")

sensor = DistanceSensor(echo=16, trigger=12)

count = 0
pre_dis = 0
while True:
    dis = (sensor.distance * 100)
    try:    
        '''if(pre_dis == int(dis) and pre_dis < 99):
            if(count > 30):
                moveBackward()
                count = 0
            else:
                count+=1 '''
        if(dis < 25):
            turnLeft()
        else:
            moveFoward()
                        
    except KeyboardInterrupt:
        stop()
        break
    #print(dis, pre_dis)
    #pre_dis = int(dis)

stop()

