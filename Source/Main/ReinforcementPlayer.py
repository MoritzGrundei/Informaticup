from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class ReinforcementPlayer(PlayerInterface):
    def __init__(self, id):
        self.id = id
        self.command = None
        self.action_space = ["turn_left", "turn_right", "change_nothing", "speed_up", "slow_down"] # , "slow_down", "speed_up"

    def get_command(self, game_state):
        return self.command

    def set_command(self, new_command):
        self.command = self.action_space[new_command]

    def is_gave_command(self):
        return self.gave_command

    def get_id(self):
        return self.id