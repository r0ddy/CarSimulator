from gcp_server import send_server
from models import mpu
import time

brake = mpu.MPU(0x68, 1)
gas = mpu.MPU(0x69, 1)
steering = mpu.MPU(0x68, 0)

def notify_bot(action):
    send_server('/notify_bot', {'action': action})

def action_loop():
    while True:
        action = {
            "brake": brake.read_x_angle(),
            "gas": gas.read_y_angle(),
            "steering": steering.read_x_angle(),
        }
        notify_bot(action)
        time.sleep(0.5)
