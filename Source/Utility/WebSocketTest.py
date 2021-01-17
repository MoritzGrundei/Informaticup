import asyncio
import json
import os
import random
import websockets
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from Source.Main.HeuristicPlayer import HeuristicPlayer
from Source.Main.SimplePlayer import SimplePlayer

def plot_field(board):
    bounds = [0, 1, 2, 3, 4, 5, 6]
    cmap = mpl.colors.ListedColormap(['white', 'purple', 'red', 'green', 'blue', 'brown', 'orange'])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    plt.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), ticks=bounds)
    plt.imshow(board, cmap=cmap)
    plt.show()

async def play():
    url = os.environ["URL"]
    key = os.environ["KEY"]


    async with websockets.connect(f"{url}?key={key}") as websocket:
        print("Waiting for initial state...", flush=True)
        state_json = await websocket.recv()
        print("Started Game")
        state = json.loads(state_json)
        own_player = state["players"][str(state["you"])]
        player = SimplePlayer(49)
        action = player.get_command(state_json)
        action_json = json.dumps({"action": action})
        await websocket.send(action_json)
        while True:
            state_json = await websocket.recv()
            state = json.loads(state_json)
            own_player = state["players"][str(state["you"])]
            if not state["running"] or not own_player["active"]:
                break
            action = player.get_command(state_json)
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)
        print(state)
        print(own_player)
        plot_field(np.array(state["cells"]))

asyncio.get_event_loop().run_until_complete(play())



