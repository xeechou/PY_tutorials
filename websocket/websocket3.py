#!/bin/env python3

import asyncio
import datetime
import websockets
import json
import logging

logging.basicConfig()

BOOKS = 0
USERS = set()
#we have a global lock here
LOCK = asyncio.Lock()

async def produce_book():
    global BOOKS
    BOOKS += 1
    print(f"we have {BOOKS} books now")

async def consume_book():
    global BOOKS
    BOOKS -= 1
    BOOKS = max(BOOKS, 0)
    print(f"we left with {BOOKS} books now")

    #BOOKS = max(0, BOOKS-1)

async def producer():
    while True:
        await produce_book()
        await notify_state()
        await asyncio.sleep(1)

def get_state():
    return json.dumps({"type": "state", "count" : BOOKS})

def get_users():
    return len(USERS)

async def notify_users():
    if USERS:
        message = json.dumps({"type" : "users", "count" : len(USERS)})
        #this may not work, object has to have __anext__
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_state():
    if USERS:
        message = get_state()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(ws):
    USERS.add(ws)
    await notify_users()

async def unregister(ws):
    USERS.remove(ws)
    await notify_users()

async def client_handler(ws, path):
    #this is why we are using set, so we don't need to create multiple clients
    await register(ws)
    try:
        await notify_state()
        #here we have async for
        async for message in ws:
            data = json.loads(message)
            if data["action"] == "buy":
                print("user is buying")
                await consume_book()
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)

    finally:
        await unregister(ws)



if __name__ == "__main__":
    start_sever = websockets.serve(client_handler, "localhost", 5678)
    asyncio.get_event_loop().run_until_complete(start_sever)
    asyncio.get_event_loop().run_until_complete(producer())
    asyncio.get_event_loop().run_forever()

