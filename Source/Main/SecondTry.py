import json
import random
import numpy as np

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class PassivePlayer(PlayerInterface):

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
        valid_actions = []

        delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
        if self.check_if_valid(current_position, delta_position_change_nothing):
            valid_actions += ["change_nothing"]
        if current_speed < 10:
            delta_position_speed_up = self.get_position_delta(translated_direction, current_speed, 1)
            if self.check_if_valid(current_position, delta_position_speed_up):
                valid_actions += ["speed_up"]
        if current_speed > 1:
            delta_position_slow_down = self.get_position_delta(translated_direction, current_speed, -1)
            if self.check_if_valid(current_position, delta_position_slow_down):
                valid_actions += ["slow_down"]

        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        if self.check_if_valid(current_position, delta_position_turn_left):
            valid_actions += ["turn_left"]

        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)
        if self.check_if_valid(current_position, delta_position_turn_right):
            valid_actions += ["turn_right"]

        try:
            action = random.choice(valid_actions)
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

    def get_distance_to_player(self):
        distances = []
        current_position = (self.own_player["x"], self.own_player["y"])
        for i in range(6):
            if i + 1 == self.state["you"]:
                distances[i] = 0
            else:
                enemy_position = self.state["players"][i + 1]


