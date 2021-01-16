import json
import random
import numpy as np
import Source.Utility.GameMetrics as GameMetrics
import Source.Utility.ActionChecker

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class SimplePlayer(PlayerInterface):

    def __init__(self, field_size):
        self.field_size = field_size
        self.command = None

    def set_command(self, new_command):
        self.command = new_command

    def get_command(self, game_state):
        #get current game state
        self.state = json.loads(game_state)
        self.own_player = self.state["players"][str(self.state["you"])]

        current_direction = self.own_player["direction"]
        current_speed = self.own_player["speed"]
        current_position = (self.own_player["x"], self.own_player["y"])

        translated_direction = self.translate_direction(current_direction)
        # if turn left: direction = (translated_direction + 1) % 4
        # if turn right: direction = (translated_direction - 1) % 4

        # define all valid actions

        delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
        #get connected components for change nothing
        change_nothing_connected_components = 0
        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        #get connected components for turn_left
        turn_left_connected_components =  0
        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)
        #get connected components for turn right
        turn_right_connected_components = 0



        valid_actions = Source.Utility.ActionChecker.get_valid_actions(current_position, current_speed, delta_position_change_nothing, None, None, delta_position_turn_left, delta_position_turn_right, self.state)


        action = " "
        try:
            if len(valid_actions) > 0:
                #print(action, max(scores))
                for valid_action in valid_actions:
                    if valid_action == 'turn_right':
                        turn_right_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_turn_right[0] + current_position[0],
                            delta_position_turn_right[1] + current_position[1],
                            self.translate_direction_inverse((translated_direction - 1) % 4), game_state,
                            self.field_size)
                    elif valid_action == 'turn_left':
                        turn_left_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_turn_left[0] + current_position[0],
                            delta_position_turn_left[1] + current_position[1],
                            self.translate_direction_inverse((translated_direction + 1) % 4), game_state,
                            self.field_size)
                    elif valid_action == 'change_nothing':
                        change_nothing_connected_components = GameMetrics.get_connected_fields_for_new_position(
                            delta_position_change_nothing[0] + current_position[0],
                            delta_position_change_nothing[1] + current_position[1], current_direction, game_state,
                            self.field_size)

                    # ignore Speedup and Slowdown
                    else:
                        pass

                    action = valid_action

                connected_components = {"change_nothing": change_nothing_connected_components, "turn_left": turn_left_connected_components, "turn_right": turn_right_connected_components}

                # Override action if connected components can be increased dramatically
                mean_connected_components = np.mean([change_nothing_connected_components, turn_right_connected_components, turn_left_connected_components])
                if connected_components[action] / float(mean_connected_components) < 0.5:
                    max_connected_components_action = max(connected_components.values())
                    for key, value in connected_components.items():
                        if value == max_connected_components_action and key in valid_actions:
                            prev_action = action
                            action = key
                            print("changed action from " + prev_action + " to " + action)

        except (IndexError, ZeroDivisionError):
            action = " "

        self.set_command(action)
        return self.command

    def translate_direction(self, direction):
        if direction == "right":
            return 0
        elif direction == "up":
            return 1
        elif direction == "left":
            return 2
        else:
            return 3

    def translate_direction_inverse(self, translated_direction):
        if translated_direction == 0:
            return "right"
        elif translated_direction == 1:
            return "up"
        elif translated_direction  == 2:
            return "left"
        else:
            return "down"

    #returns the change of position when change_nothing is used
    def get_position_delta(self, translated_direction, speed, delta_speed=0):
        x_delta = y_delta = 0
        if translated_direction == 0 or translated_direction == 2:
            x_delta = (1 - translated_direction) * (speed + delta_speed)
        else:
            y_delta = (translated_direction - 2) * (speed + delta_speed)
        return (x_delta, y_delta)