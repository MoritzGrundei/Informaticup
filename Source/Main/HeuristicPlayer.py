import json
import random
import numpy as np

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class HeuristicPlayer(PlayerInterface):

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
        scores = []

        delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
        if self.check_if_valid(current_position, delta_position_change_nothing):
            new_position_change_nothing = (current_position[0] + delta_position_change_nothing[0], current_position[1] + delta_position_change_nothing[1])
            scores += [self.get_score(new_position_change_nothing)]
            valid_actions += ["change_nothing"]
        if current_speed < 10:
            delta_position_speed_up = self.get_position_delta(translated_direction, current_speed, 1)
            if self.check_if_valid(current_position, delta_position_speed_up):
                new_position_speed_up = (current_position[0] + delta_position_speed_up[0], current_position[1] + delta_position_speed_up[1])
                scores += [self.get_score(new_position_speed_up)]
                valid_actions += ["speed_up"]
        if current_speed > 1:
            delta_position_slow_down = self.get_position_delta(translated_direction, current_speed, -1)
            if self.check_if_valid(current_position, delta_position_slow_down):
                new_position_slow_down = (current_position[0] + delta_position_slow_down[0], current_position[1] + delta_position_slow_down[1])
                scores += [self.get_score(new_position_slow_down)]
                valid_actions += ["slow_down"]

        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        if self.check_if_valid(current_position, delta_position_turn_left):
            new_position_turn_left = (current_position[0] + delta_position_turn_left[0], current_position[1] + delta_position_turn_left[1])
            scores += [self.get_score(new_position_turn_left)]
            valid_actions += ["turn_left"]

        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)
        if self.check_if_valid(current_position, delta_position_turn_right):
            new_position_turn_right = (current_position[0] + delta_position_turn_right[0], current_position[1] + delta_position_turn_right[1])
            scores += [self.get_score(new_position_turn_right)]
            valid_actions += ["turn_right"]

        if len(scores) > 0:
            action = valid_actions[scores.index(max(scores))]
            print(action, max(scores))

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

    def get_distance_to_players(self):
        distances = [0, 0, 0, 0, 0, 0]
        current_position = (self.own_player["x"], self.own_player["y"])
        if self.state["players"][str(self.state["you"])]["active"]:
            for i in range(6):
                    if i + 1 == self.state["you"]:
                        distances[i] = 0
                    else:
                        if self.state["players"][str(i + 1)]["active"]:
                            enemy_position = (self.state["players"][str(i + 1)]["x"], self.state["players"][str(i + 1)]["y"])
                            distance = np.sqrt(np.power(current_position[0] - enemy_position[0], 2) + np.power(current_position[1] - enemy_position[1], 2))
                            distances[i] = distance
                        else:
                            distances[i] = 0
        max_distance = np.sqrt(np.power(self.state["width"], 2) + np.power(self.state["height"], 2))
        for i in range(len(distances)):
            distances[i] = distances[i]/max_distance
        return distances

    def get_average_distance(self, distances):
        sum = counter = 0.0
        for i in range(len(distances)):
            if distances[i] == 0:
                pass
            else:
                sum += distances[i]
                counter += 1
        if counter == 0:
            return 0
        else:
            return sum/counter

    def get_free_spaces(self, new_position):
        number_of_free_spaces = 0
        for i in range(-4, 5):
            for j in range(-4, 5):
                try:
                    if self.state["cells"][new_position[1] + i][new_position[0] + j] == 0:
                        number_of_free_spaces += 1
                except IndexError:
                    pass
        normalised_num = number_of_free_spaces / 81.0
        return normalised_num


    def get_avg_speed(self):
        sum = 0.0
        counter = 0.0
        avg = 0.0
        if self.state["players"][str(self.state["you"])]["active"]:
            for i in range(6):
                if i + 1 == self.state["you"]:
                    pass
                else:
                    if self.state["players"][str(i + 1)]["active"]:
                        sum += self.state["players"][str(i + 1)]["speed"]
                        counter += 1
            if counter > 0:
                avg = sum/counter
        norm_avg = avg / 10
        return norm_avg

    def get_score(self, new_position):
        return self.get_avg_speed() + self.get_average_distance(self.get_distance_to_players()) + self.get_free_spaces(new_position)
