import json
import random
import numpy as np


def get_distance_to_players(game_state):
    own_player = game_state["players"][str(game_state["you"])]
    distances = [0, 0, 0, 0, 0, 0]
    current_position = (own_player["x"], own_player["y"])
    if game_state["players"][str(game_state["you"])]["active"]:
        for i in range(6):
            if i + 1 == game_state["you"]:
                distances[i] = 0
            else:
                if game_state["players"][str(i + 1)]["active"]:
                    enemy_position = (game_state["players"][str(i + 1)]["x"], game_state["players"][str(i + 1)]["y"])
                    distance = np.sqrt(np.power(current_position[0] - enemy_position[0], 2) + np.power(
                        current_position[1] - enemy_position[1], 2))
                    distances[i] = distance
                else:
                    distances[i] = 0
    max_distance = np.sqrt(np.power(game_state["width"], 2) + np.power(game_state["height"], 2))
    for i in range(len(distances)):
        distances[i] = distances[i] / max_distance
    return distances


def get_average_distance(distances):
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


def get_free_spaces(new_position, game_state):
    number_of_free_spaces = 0
    for i in range(-4, 5):
        for j in range(-4, 5):
            try:
                if game_state["cells"][new_position[1] + i][new_position[0] + j] == 0:
                    number_of_free_spaces += 1
            except IndexError:
                pass
    normalised_num = number_of_free_spaces / 81.0
    return normalised_num


def get_avg_speed(game_state):
    sum = 0.0
    counter = 0.0
    avg = 0.0
    if game_state["players"][str(game_state["you"])]["active"]:
        for i in range(6):
            if i + 1 == game_state["you"]:
                pass
            else:
                if game_state["players"][str(i + 1)]["active"]:
                    sum += game_state["players"][str(i + 1)]["speed"]
                    counter += 1
        if counter > 0:
            avg = sum / counter
    norm_avg = avg / 10
    return norm_avg
