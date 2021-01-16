import json
import random
import numpy as np

import Source
from Source.Utility.Pathfinding.Graph import Graph
import Source.Utility.GameMetrics as GameMetrics
from Source.Utility.Pathfinding.Node import Node
from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class PathFindingPlayer(PlayerInterface):

    def __init__(self, field_size, components_size):
        self.graph = None
        self.field_size = field_size
        self.components_size = components_size

    def get_command(self, game_state):
        print("Thinking...")
        game_state_no_json = game_state
        game_state = json.loads(game_state)
        x = game_state["players"][str(game_state["you"])]["x"]
        y = game_state["players"][str(game_state["you"])]["y"]
        self.own_player = game_state["players"][str(game_state["you"])]
        self.graph = Graph(game_state["cells"], x, y, game_state["width"], game_state["height"], game_state["players"][str(game_state["you"])]["direction"], self.field_size)
        destination = self.get_destination(self.graph.get_connected_components(), game_state)
        path = self.graph.get_shortest_path(destination)
        try:
            current_direction = self.own_player["direction"]
            current_speed = self.own_player["speed"]
            current_position = (self.own_player["x"], self.own_player["y"])

            translated_direction = self.translate_direction(current_direction)
            # if turn left: direction = (translated_direction + 1) % 4
            # if turn right: direction = (translated_direction - 1) % 4

            delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
            # get connected components for change nothing
            change_nothing_connected_components = 0
            delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
            # get connected components for turn_left
            turn_left_connected_components = 0
            delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)
            # get connected components for turn right
            turn_right_connected_components = 0

            valid_actions = Source.Utility.ActionChecker.get_valid_actions(current_position, current_speed,
                                                                           delta_position_change_nothing, None, None,
                                                                           delta_position_turn_left,
                                                                           delta_position_turn_right, game_state)


            action = self.get_action_from_path(path, game_state["players"][str(game_state["you"])]["direction"])
            if len(valid_actions) > 0:
                # print(action, max(scores))
                for valid_action in valid_actions:
                    if valid_action == 'turn_right':
                        turn_right_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_turn_right[0] + current_position[0],
                            delta_position_turn_right[1] + current_position[1],
                            self.translate_direction_inverse((translated_direction - 1) % 4), game_state_no_json,
                            self.components_size)
                    elif valid_action == 'turn_left':
                        turn_left_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_turn_left[0] + current_position[0],
                            delta_position_turn_left[1] + current_position[1],
                            self.translate_direction_inverse((translated_direction + 1) % 4), game_state_no_json,
                            self.components_size)
                    elif valid_action == 'change_nothing':
                        change_nothing_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_change_nothing[0] + current_position[0],
                            delta_position_change_nothing[1] + current_position[1], current_direction, game_state_no_json,
                            self.components_size)

                    # ignore Speedup and Slowdown
                    else:
                        pass

                connected_components = {"change_nothing": change_nothing_connected_components,
                                            "turn_left": turn_left_connected_components,
                                            "turn_right": turn_right_connected_components}

                # Override action if connected components can be increased dramatically
                mean_connected_components = np.mean(
                    [change_nothing_connected_components, turn_right_connected_components,
                     turn_left_connected_components])
                if connected_components[action] / float(mean_connected_components) < 0.9:
                    max_connected_components_action = max(connected_components.values())
                    for key, value in connected_components.items():
                        if value == max_connected_components_action and key in valid_actions:
                            prev_action = action
                            action = key
                            print("changed action from " + prev_action + " to " + action)
            return action
        except (IndexError, ZeroDivisionError):
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
                position_value = GameMetrics.get_average_distance(GameMetrics.get_distance_to_players(game_state)) +  min(GameMetrics.get_distances_to_borders(game_state, game_state["you"]-1)) + self.get_free_spaces([x,y], game_state)
                if position_value > max_value:
                    max_position = node
                    max_value = position_value
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

    #returns the change of position when change_nothing is used
    def get_position_delta(self, translated_direction, speed, delta_speed=0):
        x_delta = y_delta = 0
        if translated_direction == 0 or translated_direction == 2:
            x_delta = (1 - translated_direction) * (speed + delta_speed)
        else:
            y_delta = (translated_direction - 2) * (speed + delta_speed)
        return (x_delta, y_delta)

    def translate_direction_inverse(self, translated_direction):
        if translated_direction == 0:
            return "right"
        elif translated_direction == 1:
            return "up"
        elif translated_direction  == 2:
            return "left"
        else:
            return "down"
