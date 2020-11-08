class PlayerTest:
    def __init__(self, id, game):
        self.id = id
        self.game = game

    def get_command(self):
        return 'turn_right'

    def get_player_game_state(self):
        return self.game.get_game_state(self.id)