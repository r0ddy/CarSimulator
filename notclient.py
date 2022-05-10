# echo-client.py

import asyncio

SERVER_HOST = '192.168.0.108'

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        SERVER_HOST, 8888)

    try:
        while True:
            message = input()
            print(f'Send: {message!r}')
            writer.write(message.encode())
            await writer.drain()
            data = await reader.read(100)
            print(f'Received: {data.decode()!r}')
            if message == "exit":
                break
    except KeyboardInterrupt:
        message = "exit"
        writer.write(message.encode())
        await writer.drain()
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client())