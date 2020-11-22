import json
import random

from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class RandomPlayer(PlayerInterface):

    def set_command(self, new_command):
        self.command = new_command

    def get_command(self, game_state):
        state = json.loads(game_state)
        own_player = state["players"][str(state["you"])]
        current_direction = own_player["direction"]
        valid_actions = ["turn_left", "turn_right", "change_nothing"]
        if own_player["speed"] < 10:
            valid_actions += ["speed_up"]
        if own_player["speed"] > 1:
            valid_actions += ["slow_down"]
        action = random.choice(valid_actions)
        self.set_command(action)
        return self.command