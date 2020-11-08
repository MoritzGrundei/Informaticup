from InformatiCupGame import PlayerInterface


class TestPlayer(PlayerInterface):

    def set_command(self, new_command):
        self.command = 'turn_right'
