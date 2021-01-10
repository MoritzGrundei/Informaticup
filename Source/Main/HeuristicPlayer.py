import json
import random
import numpy as np
import Source.Utility.GameMetrics as GameMetrics
import Source.Utility.ActionChecker

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class HeuristicPlayer(PlayerInterface):

    def __init__(self, id, weights, field_size):
        self.id = id
        self.command = None
        self.weights = weights
        self.field_size = field_size

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
        delta_position_speed_up = self.get_position_delta(translated_direction, current_speed, 1)
        delta_position_slow_down = self.get_position_delta(translated_direction, current_speed, -1)
        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        #get connected components for turn_left
        turn_left_connected_components =  0
        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)
        #get connected components for turn right
        turn_right_connected_components = 0



        valid_actions = Source.Utility.ActionChecker.get_valid_actions(current_position, current_speed, delta_position_change_nothing, delta_position_speed_up, delta_position_slow_down, delta_position_turn_left, delta_position_turn_right, self.state)


        scores = self.get_scores(valid_actions, current_position, current_speed, delta_position_change_nothing, delta_position_speed_up, delta_position_slow_down, delta_position_turn_left, delta_position_turn_right, self.state)

        action = " "
        try:
            if len(scores) > 0:
                action = valid_actions[scores.index(max(scores))]
                #print(action, max(scores))
                for valid_action in valid_actions:
                    if valid_action == 'turn_right':
                        turn_right_connected_components = GameMetrics.get_connected_fields_for_new_position(delta_position_turn_right[0] + current_position[0], delta_position_turn_right[1] + current_position[1], self.translate_direction_inverse((translated_direction - 1) % 4), game_state, self.field_size)
                    elif valid_action == 'turn_left':
                        turn_left_connected_components = GameMetrics.get_connected_fields_for_new_position(delta_position_turn_left[0] + current_position[0], delta_position_turn_left[1] + current_position[1], self.translate_direction_inverse((translated_direction + 1) % 4), game_state, self.field_size)
                    elif valid_action == 'change_nothing':
                        change_nothing_connected_components = GameMetrics.get_connected_fields_for_new_position(delta_position_change_nothing[0] + current_position[0], delta_position_change_nothing[1] + current_position[1], current_direction, game_state, self.field_size)

                    # ignore Speedup and Slowdown
                    else:
                        pass

                connected_components = {"change_nothing": change_nothing_connected_components, "turn_left": turn_left_connected_components, "turn_right": turn_right_connected_components}
                print("connected components for: ")
                print("turn right: " + str(turn_right_connected_components))
                print("turn left: " + str(turn_left_connected_components))
                print("change nothing: " + str(change_nothing_connected_components))

                # Override action if connected components can be increased dramatically
                mean_connected_components = np.mean([change_nothing_connected_components, turn_right_connected_components, turn_left_connected_components])
                if connected_components[action] / float(mean_connected_components) < 1:
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

    def get_distance_to_players(self, state):
        return Source.Utility.GameMetrics.get_distance_to_players(state)

    def get_average_distance(self, distances):
        return Source.Utility.GameMetrics.get_average_distance(distances)

    def get_free_spaces(self, new_position, state):
        return Source.Utility.GameMetrics.get_free_spaces(new_position, state)


    def get_avg_speed(self, state):
        return Source.Utility.GameMetrics.get_avg_speed(state)

    def get_score(self, new_position):
        return  self.weights[0] * self.get_avg_speed(self.state) +  self.weights[1] * self.get_average_distance(self.get_distance_to_players(self.state)) + self.weights[2] * self.get_free_spaces(new_position, self.state)

    def get_scores(self, valid_actions, current_position, current_speed, delta_position_change_nothing, delta_position_speed_up, delta_position_slow_down, delta_position_turn_left, delta_position_turn_right, game_state):
        scores = []
        for action in valid_actions:
            if action == "change_nothing":
                new_position_change_nothing = (current_position[0] + delta_position_change_nothing[0],
                                               current_position[1] + delta_position_change_nothing[1])
                scores += [self.get_score(new_position_change_nothing)]

            elif action == "speed_up":
                new_position_speed_up = (
                current_position[0] + delta_position_speed_up[0], current_position[1] + delta_position_speed_up[1])
                scores += [-100] #[self.get_score(new_position_speed_up)]

            elif action == "slow_down":
                new_position_slow_down = (
                current_position[0] + delta_position_slow_down[0], current_position[1] + delta_position_slow_down[1])
                scores += [-100] #[self.get_score(new_position_slow_down)]

            elif action == "turn_left":
                new_position_turn_left = (
                current_position[0] + delta_position_turn_left[0], current_position[1] + delta_position_turn_left[1])
                scores += [self.get_score(new_position_turn_left)]

            elif action == "turn_right":
                new_position_turn_right = (
                current_position[0] + delta_position_turn_right[0], current_position[1] + delta_position_turn_right[1])
                scores += [self.get_score(new_position_turn_right)]

            else:
                pass
        return scores



