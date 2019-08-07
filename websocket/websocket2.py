#!/bin/env python3

import asyncio
import datetime
import websockets


USERS = set()

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

async def dummy_client():
    url = "ws://127.0.0.1:5678"
    async with websockets.connect(url) as ws:
        while True:
            message = await ws.recv()
            print(message)  


async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, "127.0.0.1", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(dummy_client())