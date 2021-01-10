from Source.InformatiCupGame.PlayerInterface import PlayerInterface

class ReinforcementPlayer(PlayerInterface):
    def __init__(self, id):
        self.id = id
        self.command = None

    def get_command(self, game_state):
        return self.command

    def set_command(self, new_command):
        self.command = new_command

    def is_gave_command(self):
        return self.gave_command

    def get_id(self):
        return self.id