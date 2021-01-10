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
        self.action_space = np.array(["turn_left", "turn_right", "change_nothing", "slow_down", "speed_up"])
        self.width = width
        self.height = height
        self.player = player
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.game_observer = GameObservations()
        self.obs = np.array(self.game_state["cells"])
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
        if action == 0:
            act = 'turn_left'
        elif action == 1:
            act = 'turn_right'
        elif action == 2:
            act = "change_nothing"
        elif action == 3:
            act = "slow_down"
        elif action == 4:
            act = "speed_up"
        self.player.set_command(act)
        latest_obs = self.game_state
        old_position = self.game_state["players"][str(self.game_state["you"])]["x"], self.game_state["players"][str(self.game_state["you"])]["y"]
        done = not self.game.tick()
        self.game_state = json.loads(self.game.get_game_state(self.player.get_id()))
        new_position = self.game_state["players"][str(self.game_state["you"])]["x"], self.game_state["players"][str(self.game_state["you"])]["y"]
        self.own_player = self.game_state["players"][str(self.game_state["you"])]
        self.set_obs()
        if not self.own_player["active"]:
            self.game.terminate_game()
            self.alive = False

        # pass reward into sigmoid function
        reward = rewards.reward_9(latest_obs, old_position, self.game_state, new_position)
        self.latest_observations = self.obs
        return self.get_obs(), reward, done, '_'


    def get_obs(self):
        return self.obs

    def get_action_space(self):
        return np.array(self.action_space)

    def set_obs(self):
        self.obs = np.array(self.game_state["cells"])

    def get_discrete_action_space(self):
        return Discrete(self.action_space.shape[0])
