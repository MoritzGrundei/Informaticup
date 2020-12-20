from gym.spaces import Discrete

import Source
from Source.Utility.ActionChecker import get_valid_actions
from Source.InformatiCupGame.ReinforcementGameWrapper import ReinforcementGameWrapper
from Source.Utility.GameObersvations import GameObservations
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
from Source.Utility.GameMetricsNew import GameMetrics
import Source.Utility.RewardFunctions as rewards
import numpy as np
import json
import random


class TrainingEnvironment:

    # set up all variables in order to create an environment to train a RLPlayer
    def __init__(self, width, height, player):
        self.game = ReinforcementGameWrapper(width, height,
                                             [player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),
                                              HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]),
                                              HeuristicPlayer(6, [1, 1, 1])])
        self.action_space = np.array(["turn_left", "turn_right", "change_nothing"]) # , "slow_down", "speed_up"
        self.width = width
        self.height = height
        self.player = player
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        # self.game_metrics = GameMetrics()
        # self.game_metrics.set_game_state(self.game_state)
        # player_distances = self.game_metrics.get_distance_to_players()
        # distances = self.game_metrics.get_distances_to_borders(self.game_state["you"])
        # self.obs = np.array([self.game_metrics.get_average_distance(self.game_metrics.get_distance_to_players()),
        # self.game_metrics.get_free_spaces((self.own_player["x"], self.own_player["y"])),
        # self.game_metrics.get_avg_speed(), self.game_metrics.get_num_living_players(), self.game_metrics.get_own_speed(),
        # player_distances[0], player_distances[1], player_distances[2], player_distances[3], player_distances[4], player_distances[5],
        # distances[0], distances[1], distances[2], distances[3]])
        self.game_observer = GameObservations()
        self.obs = self.game_observer.get_obs_1(self.game_state)
        self.latest_observations = self.obs
        #for testing
        self.alive = True

    # Reset the Game
    def reset(self):
        self.game = ReinforcementGameWrapper(self.width, self.height,
                                             [self.player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),
                                              HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]),
                                              HeuristicPlayer(6, [1, 1, 1])])
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        # return numpy array of initial observations
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.set_obs()
        return self.get_obs()

    # One Step in the Game/Training Cycle
    def step(self, action):
        current_speed = self.own_player["speed"]
        current_direction = self.own_player["direction"]
        translated_direction = self.translate_direction(current_direction)
        current_position = (self.own_player["x"], self.own_player["y"])
        delta_position_change_nothing = self.get_position_delta(translated_direction, current_speed)
        delta_position_speed_up = self.get_position_delta(translated_direction, current_speed, 1)
        delta_position_slow_down = self.get_position_delta(translated_direction, current_speed, -1)
        delta_position_turn_left = self.get_position_delta((translated_direction + 1) % 4, current_speed)
        delta_position_turn_right = self.get_position_delta((translated_direction - 1) % 4, current_speed)

        valid_actions = get_valid_actions(current_position, current_speed,
                                                                       delta_position_change_nothing,
                                                                       delta_position_speed_up,
                                                                       delta_position_slow_down,
                                                                       delta_position_turn_left,
                                                                       delta_position_turn_right, self.game_state)

        if action == 0:
            act = 'turn_left'
        elif action == 1:
            act = 'turn_right'
        else:
            act = "change_nothing"
        if act in valid_actions:
            self.player.set_command(action)
            done = not self.game.tick()
            self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
            self.own_player = self.game_state["players"][str(self.game_state["you"])]
            self.set_obs()
            if not self.own_player["active"]:
                self.game.terminate_game()
                self.alive = False

            # pass reward into sigmoid function
            reward = rewards.reward_8(self.obs, self.latest_observations)
            self.latest_observations = self.obs
            return self.get_obs(), reward, done, '_'

        else:
            temp_player = HeuristicPlayer(self.game_state["you"], [1,1,1])
            action = temp_player.get_command(json.dumps(self.game_state))
            if action == 'turn_left':
                action = 0
            elif action == 'turn_right':
                action = 1
            else:
                action = 2
            self.player.set_command(action)
            done = not self.game.tick()
            self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
            self.own_player = self.game_state["players"][str(self.game_state["you"])]
            self.set_obs()
            if not self.own_player["active"]:
                self.game.terminate_game()
                self.alive = False

            # pass reward into sigmoid function
            reward = -1
            self.latest_observations = self.obs
            return self.get_obs(), reward, done, '_'

    def get_obs(self):
        return self.obs

    def get_action_space(self):
        return np.array(self.action_space)

    def set_obs(self):
        self.obs = self.game_observer.get_obs_1(self.game_state)
        # player_distances = self.game_metrics.get_distance_to_players()
        # distances = self.game_metrics.get_distances_to_borders(self.game_state["you"])
        # self.obs = np.array([self.game_metrics.get_average_distance(self.game_metrics.get_distance_to_players()),
                            # self.game_metrics.get_free_spaces((self.own_player["x"], self.own_player["y"])),
                            # self.game_metrics.get_avg_speed(), self.game_metrics.get_num_living_players(),
                            # self.game_metrics.get_own_speed(),
                            # player_distances[0], player_distances[1], player_distances[2], player_distances[3],
                            # player_distances[4], player_distances[5],
                            # distances[0], distances[1], distances[2], distances[3]])

    def get_discrete_action_space(self):
        return Discrete(self.action_space.shape[0])

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
        return  self.weights[0] * self.get_avg_speed(self.game_state) +  self.weights[1] * self.get_average_distance(self.get_distance_to_players(self.game_state)) + self.weights[2] * self.get_free_spaces(new_position, self.game_state)

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