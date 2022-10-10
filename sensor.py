import RPi.GPIO as gpio
import time
from gpiozero import DistanceSensor
from time import sleep
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
sensor = DistanceSensor(echo=16, trigger=12)
while True:
    print('Distance: ', sensor.distance * 100)
