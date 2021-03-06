import json
import random
import numpy as np
from Source.Utility.Pathfinding.Graph import Graph

class GameMetrics:
    def __init__(self):
        self.game_state = 0

    # always set game state before getting metrics
    def set_game_state(self, game_state):
        self.game_state = game_state

    def get_distance_to_players(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        distances = [0, 0, 0, 0, 0, 0]
        current_position = (own_player["x"], own_player["y"])
        if self.game_state["players"][str(self.game_state["you"])]["active"]:
            for i in range(6):
                if i + 1 == self.game_state["you"]:
                    distances[i] = 0
                else:
                    if self.game_state["players"][str(i + 1)]["active"]:
                        enemy_position = (
                            self.game_state["players"][str(i + 1)]["x"], self.game_state["players"][str(i + 1)]["y"])
                        distance = np.sqrt(np.power(current_position[0] - enemy_position[0], 2) + np.power(
                            current_position[1] - enemy_position[1], 2))
                        distances[i] = distance
                    else:
                        distances[i] = 0
        max_distance = np.sqrt(np.power(self.game_state["width"], 2) + np.power(self.game_state["height"], 2))
        for i in range(len(distances)):
            distances[i] = distances[i] / max_distance
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
            return sum / counter

    def get_avg_speed(self):
        sum = 0.0
        counter = 0.0
        avg = 0.0
        if self.game_state["players"][str(self.game_state["you"])]["active"]:
            for i in range(6):
                if i + 1 == self.game_state["you"]:
                    pass
                else:
                    if self.game_state["players"][str(i + 1)]["active"]:
                        sum += self.game_state["players"][str(i + 1)]["speed"]
                        counter += 1
            if counter > 0:
                avg = sum / counter
        norm_avg = avg / 10
        return norm_avg

    def get_num_living_players(self):
        num = 0
        for i in range(6):
            if self.game_state["players"][str(i + 1)]["active"]:
                num += 1
        return num

    def get_player_data(self, id):
        x = self.game_state["players"][str(id + 1)]["x"]
        y = self.game_state["players"][str(id + 1)]["y"]
        speed = self.game_state["players"][str(id + 1)]["speed"]

        return x, y, speed

    def get_distances_to_borders(self, id):
        board_height = self.game_state["height"]
        board_width = self.game_state["width"]
        position = self.game_state["players"][str(id + 1)]["x"], self.game_state["players"][str(id + 1)]["y"]
        top_distance = position[1] - 1
        bottom_distance = (board_height - 1) - (position[1] - 1)
        right_distance = (board_width - 1) - (position[0] - 1)
        left_distance = position[0] - 1

        return top_distance, bottom_distance, right_distance, left_distance

    def get_own_speed(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]

        return speed

    def get_free_spaces(self, new_position):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]
        number_of_free_spaces = 0
        for i in range(-2, 3):
            for j in range(-2, 3):
                try:
                    if self.game_state["cells"][new_position[1] + i][new_position[0] + j] == 0:
                        number_of_free_spaces += 1
                except IndexError:
                    pass

        normalised_num = (number_of_free_spaces - speed) / 25.0
        return normalised_num

    def get_up_free(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]
        current_position = (own_player["x"], own_player["y"])
        free = True
        for i in range(speed):
            try:
                if self.game_state["cells"][current_position[1] - i] != 0 or current_position[1]-i <= 0:
                    free = False
            except IndexError:
                pass
        return free

    def get_down_free(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]
        current_position = (own_player["x"], own_player["y"])
        free = True
        for i in range(speed):
            try:
                if self.game_state["cells"][current_position[1] + i] != 0 or current_position[1]+i <= 0:
                    free = False
            except IndexError:
                pass
        return free

    def get_left_free(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]
        current_position = (own_player["x"], own_player["y"])
        free = True
        for i in range(speed):
            try:
                if self.game_state["cells"][current_position[0] - i] != 0 or current_position[0]-i <= 0:
                    free = False
            except IndexError:
                pass
        return free

    def get_right_free(self):
        own_player = self.game_state["players"][str(self.game_state["you"])]
        speed = own_player["speed"]
        current_position = (own_player["x"], own_player["y"])
        free = True
        for i in range(speed):
            try:
                if self.game_state["cells"][current_position[0] + i] != 0 or current_position[0]+i <= 0:
                    free = False
            except IndexError:
                pass
        return free

    def get_connected_fields_for_new_position(self, x, y, new_direction):
        graph = Graph(self.game_state["cells"],x,y, self.game_state["width"], self.game_state["height"], new_direction, 69)
        return len(graph.get_connected_components())


