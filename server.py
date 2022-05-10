import asyncio
import subprocess

from motor import Motor

HOST = subprocess.getoutput("hostname -I").strip()

# setup motor pins
motor = Motor(in1=5, in2=6, pwm=26)

async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        if message == "exit":
            break

        msg_mtr_cmd = {
            "stop": (Motor.ZERO, Motor.STOP),
            "half": (Motor.HALF, Motor.CW),
            "full": (Motor.FULL, Motor.CW)
        }

        if message in msg_mtr_cmd:
            speed, dir = msg_mtr_cmd[message]
            motor.SetSpeedAndDir(speed, dir)

        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")
        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, HOST, 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())