import socketio
import time

sio = socketio.Client()


def capture_images():
    while True:
        sio.emit('image', "i am raspberry pi")
        sio.sleep(2)


@sio.event
def connect():
    print('connection established')
    sio.start_background_task(capture_images)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://192.168.43.27:5000')
