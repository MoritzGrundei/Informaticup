from Source.InformatiCupGame.ReinforcementGameWrapper import ReinforcementGameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
import Source.Utility.GameMetrics as metrics
import Source.Utility.RewardFunctions as rewards
import numpy as np
import json
import random


class TrainingEnvironment:

    def __init__(self, width, height, player):
        self.game = ReinforcementGameWrapper(width, height, [player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), HeuristicPlayer(6, [1, 1, 1])])
        self.action_space = np.array(["turn_left", "turn_right"]) #"change_nothing", "slow_down", "speed_up"
        self.width = width
        self.height = height
        self.player = player
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        player_1_data = metrics.get_player_data(self.gamestate, 0)
        player_2_data = metrics.get_player_data(self.gamestate, 1)
        player_3_data = metrics.get_player_data(self.gamestate, 2)
        player_4_data = metrics.get_player_data(self.gamestate, 3)
        player_5_data = metrics.get_player_data(self.gamestate, 4)
        player_6_data = metrics.get_player_data(self.gamestate, 5)
        distances = metrics.get_distances_to_borders(self.gamestate, self.gamestate["you"])
        self.obs = np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                             metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]), self.gamestate),
                             metrics.get_avg_speed(self.gamestate), metrics.get_num_living_players(self.gamestate),
                             player_1_data[0], player_1_data[1], player_1_data[2],
                             player_2_data[0], player_2_data[1], player_2_data[2],
                             player_3_data[0], player_3_data[1], player_3_data[2],
                             player_4_data[0], player_4_data[1], player_4_data[2],
                             player_5_data[0], player_5_data[1], player_5_data[2],
                             player_6_data[0], player_6_data[1], player_6_data[2],
                             distances[0], distances[1], distances[2], distances[3]])
        self.set_obs(self.gamestate)
        self.latest_observations = self.obs

    def reset(self):
        self.game = ReinforcementGameWrapper(self.width, self.height, [self.player, HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]),HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), HeuristicPlayer(6, [1, 1, 1])])
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        # return numpy array of initial observations
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        self.set_obs(self.gamestate)
        return self.get_obs()

    def step(self):
        done = not self.game.tick()
        self.gamestate = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.gamestate["players"][str(self.gamestate["you"])]
        self.set_obs(self.gamestate)
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
        player_1_data = metrics.get_player_data(game_state, 0)
        player_2_data = metrics.get_player_data(game_state, 1)
        player_3_data = metrics.get_player_data(game_state, 2)
        player_4_data = metrics.get_player_data(game_state, 3)
        player_5_data = metrics.get_player_data(game_state, 4)
        player_6_data = metrics.get_player_data(game_state, 5)
        distances = metrics.get_distances_to_borders(game_state, game_state["you"])
        self.ops = np.array([metrics.get_average_distance(metrics.get_distance_to_players(self.gamestate)),
                   metrics.get_free_spaces((self.own_player["x"], self.own_player["y"]), self.gamestate),
                   metrics.get_avg_speed(self.gamestate), metrics.get_num_living_players(self.gamestate),
                             player_1_data[0], player_1_data[1], player_1_data[2],
                             player_2_data[0], player_2_data[1], player_2_data[2],
                             player_3_data[0], player_3_data[1], player_3_data[2],
                             player_4_data[0], player_4_data[1], player_4_data[2],
                             player_5_data[0], player_5_data[1], player_5_data[2],
                             player_6_data[0], player_6_data[1], player_6_data[2],
                             distances[0], distances[1], distances[2], distances[3]])
