from Source.InformatiCupGame.PlayerInterface import PlayerInterface


class TestPlayer(PlayerInterface):

    def set_command(self, new_command):
        self.command = new_command

    def get_command(self, game_state):
        #calculate new command
        self.set_command('change_nothing')
        return self.command
