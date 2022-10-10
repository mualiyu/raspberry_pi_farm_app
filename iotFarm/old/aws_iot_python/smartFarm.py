from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from gpiozero import LED
import logging
import time
import argparse
import json
import serial
import sqlite3

loraModule = serial.Serial('/dev/ttyACM0', 9600)
gpsModule = serial.Serial ("/dev/ttyUSB0", 9600)

valve = LED(23)
AUTOMATIC_MODE = True

#connect to database file
dbconnect = sqlite3.connect("smartFarmDB");
#If we want to access columns by name we need to set
#row_factory to sqlite3.Row class
dbconnect.row_factory = sqlite3.Row;
#now we create a cursor to work with db
cursor = dbconnect.cursor();

def formatDegreesMinutes(coordinates, digits):
    
    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = left[:digits]
    minutes = right[:3]

    return degrees + "." + minutes

# This method reads the data from the serial port, the GPS dongle is attached to,
# and then parses the NMEA messages it transmits.
# gps is the serial port, that's used to communicate with the GPS adapter

def getPositionData(gps):
    run = True
    while run:
        #print("acquiring GPS data")
        data = gps.readline().decode('utf-8').strip()
        #print (data)
        message = data[0:6]
        if (message == "$GPRMC"):
            # GPRMC = Recommended minimum specific GPS/Transit data
            # Reading the GPS fix data is an alternative approach that also works
            parts = data.split(",")
            if parts[2] == 'V':
                # V = Warning, most likely, there are no satellites in view...
                #print ("GPS receiver warning")
                return '"null"'
            else:
                # Get the position data that was transmitted with the GPRMC message
                # In this example, I'm only interested in the longitude and latitude
                # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
                longitude = formatDegreesMinutes(parts[5], 3)
                latitude = formatDegreesMinutes(parts[3], 2)
                #print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
                return "{\"longitude\":\""+longitude+"\", \"latitude\":\""+latitude+"\"}"
        else:
            # Handle other NMEA messages and unsupported strings
            pass
def sensorRead():
    # In the NMEA message, the position gets transmitted as:
    # DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
    # the minutes. However, I want to convert this format to the following:
    # DD.MMMM. This method converts a transmitted string to the desired format
    #print("starting sensor read")
    try:
        #print("starting GPS")
        gps = getPositionData(gpsModule)
        #print("starting Lora")
        nodeA = loraModule.readline().decode('ascii').strip()
        nodeB = loraModule.readline().decode('ascii').strip()
        payload = {}
        try:
            nodex = json.loads(nodeA)
            nodey = json.loads(nodeB)
            payload['nodeA'] = nodex
            payload['nodeB'] = nodey
            payload['gps'] = json.loads(gps)
            payload['pump'] = str(valve.value)
            payload['automode'] = str(AUTOMATIC_MODE)
            if AUTOMATIC_MODE:
                if nodex['moisture'] > 0 :
                    print("turning on valve")
                    valve.on()
                elif nodey['moisture'] > 0:
                    print("turning on valve")
                    valve.on()
                else:
                    print("turning off valve")
                    valve.off()
            # store to local db
            #execute insetr statement
            cursor.execute('''insert into sensor values (?, ?, ?, ?)''',
                           (nodex['nodeId'], nodex['temperature'], nodex['humidity'],
                            nodex['moisture']));
            cursor.execute('''insert into sensor values (?, ?, ?, ?)''',
                           (nodey['nodeId'], nodey['temperature'], nodey['humidity'],
                            nodey['moisture']));
            dbconnect.commit();
        except:
            print("Error Json")
            pass
            
        return json.dumps(payload)        
    except :
        #running = False
        #gpsModule.close()
        #loraModule.close()
        #print ("Sensor read Fails!")
        return False
# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    payload = json.loads(message.payload.decode('ascii').strip())
    pump = payload['pump']
    automode = payload['automode']
    global AUTOMATIC_MODE
    AUTOMATIC_MODE = automode
    valve.value = pump
    print(pump, automode, AUTOMATIC_MODE)

host = 'a2x4ipi3mptttw-ats.iot.us-east-2.amazonaws.com'
rootCAPath = 'credentials/root-CA.crt'
certificatePath = 'credentials/certificate.pem.crt'
privateKeyPath = 'credentials/private.pem.key'


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient("SmartFarm")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
try:
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe("smartfarm/command", 1, customCallback)
    time.sleep(2)
except:
    pass
# Publish to the same topic in a loop forever
while True:
    dataset = sensorRead()
    if dataset:
        try:
            myAWSIoTMQTTClient.publish("smartfarm/dataset", dataset, 1)
            #print('Published topic %s: %s\n' % ("smartfarm/dataset", dataset))
            time.sleep(1)
        except:
            pass
