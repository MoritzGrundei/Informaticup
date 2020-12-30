import json
import random
import numpy as np
from Source.Utility.Pathfinding.Graph import Graph
import Source.Utility.GameMetrics as GameMetrics

from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class PathFindingPlayer(PlayerInterface):

    def __init__(self):
        self.graph = None

    def get_command(self, game_state):
        game_state = json.loads(game_state)
        x = game_state["players"][str(game_state["you"])]["x"]
        y = game_state["players"][str(game_state["you"])]["y"]
        self.graph = Graph(game_state["cells"], x, y, game_state["width"], game_state["height"])
        destination = self.get_destination(self.graph.get_connected_components(), game_state)
        print(str(destination))
        return "turn_right"

    def get_destination(self, nodes, game_state):
        width = game_state["width"]
        height = game_state["height"]
        max_value = 0
        max_position = None
        for node in nodes:
            x = node.get_x()
            y = node.get_y()
            if x >= 0 and x < width and y >= 0 and y < height:
                game_state["players"][str(game_state["you"])]["x"] = x
                game_state["players"][str(game_state["you"])]["y"] = y
                if GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + min(GameMetrics.get_distances_to_borders(game_state, game_state["you"] - 1)) > max_value:
                    max_position = (x,y)
                    max_value = GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + min(GameMetrics.get_distances_to_borders(game_state, game_state["you"]-1))
        return max_position
