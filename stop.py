import RPi.GPIO as gpio
import time
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
        print("Stop")

stop()
