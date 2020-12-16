
from Source.InformatiCupGame.ReinforcementGameWrapper import ReinforcementGameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
from Source.Utility.GameMetricsNew import GameMetrics
import Source.Utility.RewardFunctions as rewards
import numpy as np
import json
import random


class TrainingEnvironment:

    #set up all variables in order to create an environment to train a RLPlayer
    def __init__(self, width, height, player):
        self.game = ReinforcementGameWrapper(width, height, [player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), HeuristicPlayer(6, [1, 1, 1])])
        self.action_space = np.array(["turn_left", "turn_right", "change_nothing", "slow_down", "speed_up"])
        self.width = width
        self.height = height
        self.player = player
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.game_metrics = GameMetrics()
        self.game_metrics.set_game_state(self.game_state)
        player_distances = self.game_metrics.get_distance_to_players()
        distances = self.game_metrics.get_distances_to_borders(self.game_state["you"])
        self.obs = np.array([self.game_metrics.get_average_distance(self.game_metrics.get_distance_to_players()),
                              self.game_metrics.get_free_spaces((self.own_player["x"], self.own_player["y"])),
                              self.game_metrics.get_avg_speed(), self.game_metrics.get_num_living_players(), self.game_metrics.get_own_speed(),
                              player_distances[0], player_distances[1], player_distances[2], player_distances[3], player_distances[4], player_distances[5],
                              distances[0], distances[1], distances[2], distances[3]])
        self.set_obs(self.game_state)
        self.latest_observations = self.obs

    #Reset the Game
    def reset(self):
        self.game = ReinforcementGameWrapper(self.width, self.height, [self.player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), HeuristicPlayer(6, [1, 1, 1])])
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        # return numpy array of initial observations
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.set_obs(self.game_state)
        return self.get_obs()

    #One Step in the Game/Training Cycle
    def step(self):
        done = not self.game.tick()
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.set_obs(self.game_state)
        if(self.own_player["active"] == False):
            self.game.terminate_game()

        #pass reward into sigmoid function
        reward = rewards.reward_1(self.obs, self.latest_observations)
        self.latest_observations = self.obs
        return self.get_obs(), reward, done, '_'

    def get_obs(self):
        return self.obs

    def get_action_space(self):
        return self.action_space

    def set_obs(self, game_state):
        self.game_metrics.set_game_state(self.game_state)
        player_distances = self.game_metrics.get_distance_to_players()
        distances = self.game_metrics.get_distances_to_borders(self.game_state["you"])
        self.obs = np.array([self.game_metrics.get_average_distance(self.game_metrics.get_distance_to_players()),
                              self.game_metrics.get_free_spaces((self.own_player["x"], self.own_player["y"])),
                              self.game_metrics.get_avg_speed(), self.game_metrics.get_num_living_players(), self.game_metrics.get_own_speed(),
                              player_distances[0], player_distances[1], player_distances[2], player_distances[3], player_distances[4], player_distances[5],
                              distances[0], distances[1], distances[2], distances[3]])
