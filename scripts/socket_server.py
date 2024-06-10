import os
import json
import asyncio
import websockets
import threading

CLIENTS = set()
PORT = 8765

from scripts.worker_strategy_execution import run_testing_strategy
from scripts.emulator import load_emulator

abort_event = threading.Event()

async def message_handler(data):
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return

    if data['type'] == 'loadEmulator':
        emulator_thread = threading.Thread(target=load_emulator)
        emulator_thread.start()
    elif data['type'] == 'runStrategyTests':
        execution_parameters = data['payload']['execution_parameters']
        strategy = data['payload']['strategy']
        abort_event.clear()

        strategy_thread = threading.Thread(target=run_testing_strategy_wrapper, args=(execution_parameters, strategy))
        strategy_thread.start()
    elif data['type'] == 'abortExecution':
        abort_event.set()

async def handler(websocket):
    CLIENTS.add(websocket)

    try:
        while True:
            data = await websocket.recv()
            await message_handler(data)

    except websockets.ConnectionClosed:
        pass
    finally:
        CLIENTS.remove(websocket)

async def broadcast(type, payload):
    for websocket in CLIENTS.copy():
        try:
            await websocket.send(json.dumps({
                'type': type,
                'payload': payload
            }))
        except websockets.ConnectionClosed:
            CLIENTS.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

def socket_server():
    asyncio.run(main())

def run_testing_strategy_wrapper(execution_parameters, strategy):
    global abort_event
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_testing_strategy(execution_parameters, strategy, broadcast, abort_event))

if __name__ == "__main__":
    server_thread = threading.Thread(target=socket_server)
    server_thread.start()
    
    server_thread.join()
