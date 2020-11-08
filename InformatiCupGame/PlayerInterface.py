class PlayerInterface:
    def __init__(self, id, game):
        self.id = id
        self.game = game
        self.command = None

    def get_command(self, game_state):
        return self.command

    def set_command(self, new_command):
        self.command = new_command

    def is_gave_command(self):
        return self.gave_command

    def get_player_game_state(self):
        return self.game.get_game_state(self.id)