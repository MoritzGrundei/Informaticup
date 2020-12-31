import json
import random
import numpy as np

import Source
from Source.Utility.Pathfinding.Graph import Graph
import Source.Utility.GameMetrics as GameMetrics
from Source.Utility.Pathfinding.Node import Node
from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class PathFindingPlayer(PlayerInterface):

    def __init__(self, field_size):
        self.graph = None
        self.field_size = field_size

    def get_command(self, game_state):
        print("Thinking...")
        game_state = json.loads(game_state)
        x = game_state["players"][str(game_state["you"])]["x"]
        y = game_state["players"][str(game_state["you"])]["y"]
        self.graph = Graph(game_state["cells"], x, y, game_state["width"], game_state["height"], game_state["players"][str(game_state["you"])]["direction"], self.field_size)
        destination = self.get_destination(self.graph.get_connected_components(), game_state)
        path = self.graph.get_shortest_path(destination)
        try:
            return self.get_action_from_path(path, game_state["players"][str(game_state["you"])]["direction"])
        except IndexError:
            return "change_nothing"

    def get_action_from_path(self, path, direction):
        starting_node = path[0]
        try:
            dest_node = path[1]
        except IndexError:
            print("Index Error with path" + str(path[0]))
            return "change_nothing"
        # refactor this!
        if abs(dest_node.get_y() - starting_node.get_y()) > 1:
            print("Error : There should be no edge")
            print(self.graph)
        #direction is up
        if direction == "up" and dest_node.get_y() < starting_node.get_y():
            return "change_nothing"

        elif direction == "up" and dest_node.get_y() > starting_node.get_y():
            print("accident with direction: " + direction)
            return "turn_right"

        elif direction == "up" and dest_node.get_x() < starting_node.get_x():
            return "turn_left"

        elif direction == "up" and dest_node.get_x() > starting_node.get_x():
            return "turn_right"

        #direction is right
        if direction == "right" and dest_node.get_y() < starting_node.get_y():
            return "turn_left"

        elif direction == "right" and dest_node.get_y() > starting_node.get_y():
            return "turn_right"

        elif direction == "right" and dest_node.get_x() > starting_node.get_x():
            return "change_nothing"

        elif direction == "right" and dest_node.get_x() < starting_node.get_x():
            print("accident with direction: " + direction)
            return "change_nothing"

        #direction is left
        if direction == "left" and dest_node.get_y() > starting_node.get_y():
            return "turn_left"

        elif direction == "left" and dest_node.get_y() < starting_node.get_y():
            return "turn_right"

        elif direction == "left" and dest_node.get_x() > starting_node.get_x():
            print("accident with direction: " + direction)
            return "change_nothing"

        elif direction == "left" and dest_node.get_x() < starting_node.get_x():
            return "change_nothing"

        #direction is down
        if direction == "down" and dest_node.get_y() < starting_node.get_y():
            print("accident with direction: " + direction)
            return "turn_right"

        elif direction == "down" and dest_node.get_y() > starting_node.get_y():
            return "change_nothing"

        elif direction == "down" and dest_node.get_x() < starting_node.get_x():
            return "turn_right"

        elif direction == "down" and dest_node.get_x() > starting_node.get_x():
            return "turn_left"

    def get_destination(self, nodes, game_state):
        width = game_state["width"]
        height = game_state["height"]
        max_value = - np.inf
        max_position = None
        current_x = game_state["players"][str(game_state["you"])]["x"]
        current_y = game_state["players"][str(game_state["you"])]["y"]
        for node in nodes:
            x = node.get_x()
            y = node.get_y()
            if (x >= 0 and x < width and y >= 0 and y < height) and not (x == current_x and y == current_y):
                game_state["players"][str(game_state["you"])]["x"] = x
                game_state["players"][str(game_state["you"])]["y"] = y
                if self.get_avg_speed(game_state) +  self.get_average_distance(self.get_distance_to_players(game_state)) + self.get_free_spaces([x,y], game_state) > max_value:
                        #GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + 0 * min(GameMetrics.get_distances_to_borders(game_state, game_state["you"] - 1)) > max_value:
                    max_position = node
                    max_value = self.get_avg_speed(game_state) +  self.get_average_distance(self.get_distance_to_players(game_state)) + self.get_free_spaces([x,y], game_state)
                        # GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) + 0 * min(GameMetrics.get_distances_to_borders(game_state, game_state["you"]-1))
        return max_position

    def translate_direction(self, direction):
        if direction == "right":
            return 0
        elif direction == "up":
            return 1
        elif direction == "left":
            return 2
        else:
            return 3

    def get_distance_to_players(self, state):
        return Source.Utility.GameMetrics.get_distance_to_players(state)

    def get_average_distance(self, distances):
        return Source.Utility.GameMetrics.get_average_distance(distances)

    def get_free_spaces(self, new_position, state):
        return Source.Utility.GameMetrics.get_free_spaces(new_position, state)


    def get_avg_speed(self, state):
        return Source.Utility.GameMetrics.get_avg_speed(state)
