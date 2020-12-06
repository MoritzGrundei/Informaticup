from Source.InformatiCupGame.ReinforcementGameWrapper import ReinforcementGameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
import Source.Utility.GameMetrics as metrics
import numpy as np
import json
import random


class TrainingEnvironment:

    def __init__(self, width, height, player):
        self.game = ReinforcementGameWrapper(width, height, [player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), RandomPlayer(6)])
        self.action_space = np.array(["change_nothing", "turn_left", "turn_right", "slow_down", "speed_up"])
        self.width = width
        self.height = height
        self.player = player
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        self.latest_observations = np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                        metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]), self.gamestate),
                        metrics.get_avg_speed(self.gamestate)])
        self.obs = self.latest_observations

    def reset(self):
        self.game = ReinforcementGameWrapper(self.width, self.height, [self.player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), RandomPlayer(6)])
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        # return numpy array of initial observations
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        return np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                        metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]), self.gamestate),
                        metrics.get_avg_speed(self.gamestate)])

    def step(self):
        done = not self.game.tick()
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        if(self.own_player["active"] == False):
            self.game.terminate_game()
        self.obs = np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                        metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]),self.gamestate),
                        metrics.get_avg_speed(self.gamestate)])

        #pass reward into sigmoid function
        reward = ((self.obs[0] - self.latest_observations[0]) + (self.obs[1] - self.latest_observations[1]))
        reward = 0.5 * (1 + np.tanh(reward/2.0))
        self.latest_observations = self.obs
        return np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                        metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]), self.gamestate),
                        metrics.get_avg_speed(self.gamestate)]), reward, done, '_'

    def get_obs(self):
        return self.obs

    def get_action_space(self):
        return self.action_space
