import json
import random
import numpy as np
import Source.Utility.GameMetrics
import Source.Utility.ActionChecker

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class HeuristicPlayer(PlayerInterface):

    def __init__(self, id, weights):
        self.id = id
        self.command = None
        self.weights = weights

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
        # if turn left: direction = (translated_direction - 1) % 4

        # define all valid actions

        delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
        delta_position_speed_up = self.get_position_delta(translated_direction, current_speed, 1)
        delta_position_slow_down = self.get_position_delta(translated_direction, current_speed, -1)
        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)

        valid_actions = Source.Utility.ActionChecker.get_valid_actions(current_position, current_speed, delta_position_change_nothing, delta_position_speed_up, delta_position_slow_down, delta_position_turn_left, delta_position_turn_right, self.state)

        scores = self.get_scores(valid_actions, current_position, current_speed, delta_position_change_nothing, delta_position_speed_up, delta_position_slow_down, delta_position_turn_left, delta_position_turn_right, self.state)

        action = " "
        try:
            if len(scores) > 0:
                action = valid_actions[scores.index(max(scores))]
                #print(action, max(scores))
        except IndexError:
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

    #returns the change of position when change_nothing is used
    def get_position_delta(self, translated_direction, speed, delta_speed=0):
        x_delta = y_delta = 0
        if translated_direction == 0 or translated_direction == 2:
            x_delta = (1 - translated_direction) * (speed + delta_speed)
        else:
            y_delta = (translated_direction - 2) * (speed + delta_speed)
        return (x_delta, y_delta)

    #currently ignores jumps
    def check_if_valid(self, current_position, position_delta):
        for i in range(abs(position_delta[0])):
            x_to_check = current_position[0] + np.sign(position_delta[0]) * (i + 1)
            try:
                if x_to_check < 0 or x_to_check > self.state["width"] - 1 or (self.state["cells"][current_position[1]][x_to_check]) != 0:
                    return False
            except:
                return False

        for i in range(abs(position_delta[1])):
            y_to_check = current_position[1] + np.sign(position_delta[1]) * (i + 1)
            try:
                if y_to_check < 0 or y_to_check > self.state["height"] - 1 or (self.state["cells"][y_to_check][current_position[0]]) != 0:
                    return False
            except:
                return False

        return True

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
                scores += [self.get_score(new_position_speed_up)]

            elif action == "slow_down":
                new_position_slow_down = (
                current_position[0] + delta_position_slow_down[0], current_position[1] + delta_position_slow_down[1])
                scores += [self.get_score(new_position_slow_down)]

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



