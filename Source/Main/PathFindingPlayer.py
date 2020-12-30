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
        path = self.graph.get_shortest_path(destination)
        return self.get_action_from_path(path, game_state["players"][str(game_state["you"])]["direction"])

    def get_action_from_path(self, path, direction):
        starting_node = path[0]
        dest_node = path[1]
        # refactor this!
        if direction == "up" and dest_node.get_y() - starting_node.get_y() < 0:
            return "change_nothing"
        elif direction == "up" and dest_node.get_y() - starting_node.get_y() > 0:
            print("accident")
            return "turn_right"
        elif direction == "up" and dest_node.get_x() - starting_node.get_x() < 0:
            return "turn_left"
        elif direction == "up" and dest_node.get_x() - starting_node.get_x() > 0:
            return "turn_right"
        if direction == "right" and dest_node.get_y() - starting_node.get_y() < 0:
            return "turn_left"
        elif direction == "right" and dest_node.get_y() - starting_node.get_y() > 0:
            return "turn_right"
        elif direction == "right" and dest_node.get_x() - starting_node.get_x() < 0:
            print("accident")
            return "turn_left"
        elif direction == "right" and dest_node.get_x() - starting_node.get_x() > 0:
            return "change_nothing"
        if direction == "left" and dest_node.get_y() - starting_node.get_y() < 0:
            return "turn_right"
        elif direction == "left" and dest_node.get_y() - starting_node.get_y() > 0:
            return "turn_left"
        elif direction == "left" and dest_node.get_x() - starting_node.get_x() < 0:
            return "change_nothing"
        elif direction == "left" and dest_node.get_x() - starting_node.get_x() > 0:
            print("accident")
            return "turn_right"
        if direction == "down" and dest_node.get_y() - starting_node.get_y() < 0:
            print("accident")
            return "turn_right"
        elif direction == "down" and dest_node.get_y() - starting_node.get_y() > 0:
            return "change_nothing"
        elif direction == "down" and dest_node.get_x() - starting_node.get_x() < 0:
            return "turn_right"
        elif direction == "down" and dest_node.get_x() - starting_node.get_x() > 0:
            return "turn_left"

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
                    max_position = node
                    max_value = GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + min(GameMetrics.get_distances_to_borders(game_state, game_state["you"]-1))
        return max_position
