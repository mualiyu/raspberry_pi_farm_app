from flask import Flask
import serial
import json
from time import sleep
from gpiozero import LED
import threading
payload = '{}'

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
        data = gps.readline().decode('utf-8').strip()
        message = data[0:6]
        if (message == "$GPRMC"):
            # GPRMC = Recommended minimum specific GPS/Transit data
            # Reading the GPS fix data is an alternative approach that also works
            parts = data.split(",")
            if parts[2] == 'V':
                # V = Warning, most likely, there are no satellites in view...
                #print ("GPS receiver warning")
                return "{'gps':{}}"
            else:
                # Get the position data that was transmitted with the GPRMC message
                # In this example, I'm only interested in the longitude and latitude
                # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
                longitude = formatDegreesMinutes(parts[5], 3)
                latitude = formatDegreesMinutes(parts[3], 2)
                #print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
                return "{'gps':{'longitude':"+longitude+", 'latitude':"+latitude+"}}"
        else:
            # Handle other NMEA messages and unsupported strings
            pass

class BackgroundThread(object):
    
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
    def run(self):
        """ Method that runs forever """
        #define usb connection for gps and lora reciver
        loraModule = serial.Serial('/dev/ttyACM0', 9600)
        gpsModule = serial.Serial ("/dev/ttyUSB0", 9600)


        valveA = LED(23)
        valveB = LED(24)
        valveA.active_high = True
        valveB.active_high = True

        # In the NMEA message, the position gets transmitted as:
        # DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
        # the minutes. However, I want to convert this format to the following:
        # DD.MMMM. This method converts a transmitted string to the desired format
        running = True
        while running:
            try:
                gps = getPositionData(gpsModule)
                nodeA = loraModule.readline().decode('ascii').strip()
                nodeB = loraModule.readline().decode('ascii').strip()            
                try:
                    nodex = json.loads(nodeA)
                    nodexId = nodex['nodeId']
                    nodexTemp = nodex['temperature']
                    nodexHum = nodex['humidity']
                    nodexMois = nodex['moisture']
                    nodey = json.loads(nodeB)
                    nodeyId = nodey['nodeId']
                    nodeyTemp = nodey['temperature']
                    nodeyHum = nodey['humidity']
                    nodeyMois = nodey['moisture']
                    
                    if nodex['nodeId'] == 1 and nodex['moisture'] < 0:
                        print("turning off valveA")
                        valveA.on()
                    else:
                        print("turning on valveA")
                        valveA.off()
                    if nodey['nodeId'] == 2 and nodey['moisture'] < 0:
                        print("turning off valveB")
                        valveB.on()
                    else:
                        print("turning on valveB")
                        valveB.off()
                except:
                    print("Error Json")
                valves = "{'valves':{'node1':"+str(not valveA.is_active)+", 'node2':"+str(not valveB.is_active)+"}}"
                payload = "["+nodeA+","+nodeB+","+gps+", "+valves+"]"
                print(payload)
            except KeyboardInterrupt:
                running = False
                gpsModule.close()
                print ("Application closed!")
            
            
                

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>'+payload+'</h1>'
if __name__ == '__main__':
    readSensors = BackgroundThread()
    print (readSensors)
    #app.run(debug=True, host='0.0.0.0')
    
        
