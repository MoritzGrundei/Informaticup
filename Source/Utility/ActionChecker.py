import json
import random
import numpy as np

def check_if_valid(current_position, position_delta, game_state):
    for i in range(abs(position_delta[0])):
        x_to_check = current_position[0] + np.sign(position_delta[0]) * (i + 1)
        try:
            if x_to_check < 0 or x_to_check > game_state["width"] - 1 or (
            game_state["cells"][current_position[1]][x_to_check]) != 0:
                return False
        except:
            return False

    for i in range(abs(position_delta[1])):
        y_to_check = current_position[1] + np.sign(position_delta[1]) * (i + 1)
        try:
            if y_to_check < 0 or y_to_check > game_state["height"] - 1 or (
            game_state["cells"][y_to_check][current_position[0]]) != 0:
                return False
        except:
            return False

    return True

def get_valid_actions(current_position, current_speed, delta_change_nothing, delta_speed_up, delta_slow_down, delta_turn_left, delta_turn_right, game_state):
    valid_actions = []
    if check_if_valid(current_position, delta_change_nothing, game_state):
        valid_actions += ["change_nothing"]

    if current_speed < 10:
        if check_if_valid(current_position, delta_speed_up, game_state):
            valid_actions += ["speed_up"]

    if current_speed > 1:
        if check_if_valid(current_position, delta_slow_down, game_state):
            valid_actions += ["slow_down"]

    if check_if_valid(current_position, delta_turn_left, game_state):
        valid_actions += ["turn_left"]

    if check_if_valid(current_position, delta_turn_right, game_state):
        valid_actions += ["turn_right"]

    return valid_actions


