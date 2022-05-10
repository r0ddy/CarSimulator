import socketio
import io
import picamera
from threading import Condition
import base64
from models import bot

bot.init()
sio = socketio.Client()
sio.connect('ws://car-simulator-349213.uk.r.appspot.com/')
sio.emit('join',{'device_type': 'bot'})

LOCAL_SERVER_URL = None

@sio.on('server_on')
def server_on(data):
    global LOCAL_SERVER_URL
    LOCAL_SERVER_URL = "ws://{}:3000/".format(data["ip"])
    sio.disconnect()

@sio.on('notif')
def notif(data):
    print(data)
    global start_time
    if data['mode'] == 'D' or data['mode'] == 'R':
        reverse = data['mode'] == 'R'
        bot.accelerate(data['speed'], reverse)
        bot.turn(data['steering'], reverse)
    elif data['mode'] == 'P':
        bot.stop()

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

sio.wait()
sio.connect(LOCAL_SERVER_URL)
sio.emit('join',{'device_type': 'bot'})

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    camera.rotation = 180
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        sio.emit('send_msg', {'msg': str(base64.b64encode(frame)), 'device_type': 'bot'})
