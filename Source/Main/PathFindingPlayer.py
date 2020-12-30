import json
import random
import numpy as np
from Source.Utility.Pathfinding.Graph import Graph
import Source.Utility.GameMetrics as GameMetrics

from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class PathFindingPlayer(PlayerInterface):

    def __init__(self, game_state):
        if game_state != None:
            x = game_state[str(game_state["you"])]["x"]
            y = game_state[str(game_state["you"])]["y"]
            self.graph = Graph(game_state["cells"], x, y, game_state["width"], game_state["height"])
        else:
            self.graph = None

    def get_command(self, game_state):
        game_state = json.loads(game_state)
        #destination = self.get_destination(game_state)

        x = game_state["players"][str(game_state["you"])]["x"]
        y = game_state["players"][str(game_state["you"])]["y"]
        print("game state: " + str((x,y)) + str(game_state["cells"][x][y]))
        self.graph = Graph(game_state["cells"], x, y, game_state["width"], game_state["height"])
        return "turn_right"

    def get_destination(self, game_state):
        current_x = game_state["players"][str(game_state["you"])]["x"]
        current_y = game_state["players"][str(game_state["you"])]["y"]
        width = game_state["width"]
        height = game_state["height"]
        max_value = 0
        max_position = None
        for i in range(-4, 5):
            for j in range(-4, 5):
                x = current_x + i
                y = current_y + j
                if x >= 0 and x < width and y >= 0 and y < height:
                    game_state["players"][str(game_state["you"])]["x"] = x
                    game_state["players"][str(game_state["you"])]["y"] = y
                    if GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + min(GameMetrics.get_distances_to_borders(game_state, game_state["you"] - 1)) > max_value:
                        max_position = (x,y)
                        max_value = GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + min(GameMetrics.get_distances_to_borders(game_state, game_state["you"]-1))
        return max_position