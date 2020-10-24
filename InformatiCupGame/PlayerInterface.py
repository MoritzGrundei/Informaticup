from .Player import Player

class PlayerInterface:

    def __init__(self, player_id, player):
        self.player_id = player_id
        self.player = player

    def get_player_move(self, next_move):
        if next_move == "speed_up":
            self.player.speed_up()

        elif next_move == "slow_down":
            self.player.slow_down()

        elif next_move == "turn_left":
            self.player.turn_left()

        elif next_move == "turn_right":
            self.player.turn_right()

        elif next_move == "change_nothing":
            self.player.change_nothing()

        else:
            self.player.deactivate()
