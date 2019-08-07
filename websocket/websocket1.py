#!/bin/env python3

import websockets
import asyncio



async def hello_from_client():
    url = "ws://localhost:4321"
    async with websockets.connect(url) as ws:
        name = input("what is your name: ")
        await ws.send(f"hello, my name is {name}")
        greeting = await ws.recv()
        print(f"< recv: {greeting}")

async def hello_from_server(websocket, path):
    name = await websocket.recv()
    name = name.split()[-1]
    greeting = f"nice to meet you, {name}"
    await websocket.send(greeting)

if __name__ == "__main__":
    server = websockets.serve(hello_from_server, "localhost", 4321)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_until_complete(hello_from_client())


