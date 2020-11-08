import asyncio
import json
import os
import random
import websockets


async def play():
    url = 'wss://msoll.de/spe_ed'
    key = 'ZC4R7UH2QKVRQ3VVEQ6WIA4VBHFRVPM4CGEBW7XFYAR6NQZGJVFEFQBT'

    async with websockets.connect(f"{url}?key={key}") as websocket:
        print("Waiting for initial state...", flush=True)
        while True:
            state_json = await websocket.recv()
            state = json.loads(state_json)
            current_field = state['cells']
            print("<", type(state['cells']))
            own_player = state["players"][str(state["you"])]
            if not state["running"] or not own_player["active"]:
                break
            action = 'change_nothing'
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)


asyncio.get_event_loop().run_until_complete(play())