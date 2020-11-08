from InformatiCupGame import PlayerInterface


class TestPlayer(PlayerInterface):

    def set_command(self, new_command):
        self.command = new_command

    def get_command(self, game_state):
        #calculate new command
        self.set_command('turn_left')
        return self.command
