from models import mpu
import asyncio
import subprocess
import websockets
import time
import json

brake = mpu.MPU(0x68)
gas = mpu.MPU(0x69)

HOST = subprocess.getoutput("hostname -I").strip()
PORT = 8888

async def send_controller_measurements(websocket):
    while True:
        bx, by, bz = brake.read_gyro()
        brake_data = {
            "brake": {
                "x": bx,
                "y": by,
                "z": bz,
                "time": time.time()
            },
        }
        await websocket.send(json.dumps(brake_data))
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(send_controller_measurements, HOST, PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())