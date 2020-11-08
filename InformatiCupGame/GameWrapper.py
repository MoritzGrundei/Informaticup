from Game import Game
from PlayerInterface import PlayerInterface
import time

class GameWrapper:
    def __init__(self, width, height, players):
        self.game = Game(width, height, len(players), time.time())
        self.players = players
        self.run()

    def run(self):
        print(self.get_game_state(1))
        print(self.game.running)
        while self.game.running:
            counter = 1
            inputs = []
            for player in self.players:
                inputs.append(player.get_command(self.game.return_game_state(counter)))
                counter = counter + 1
                print(player.get_player_game_state())
            self.game.tick(inputs)
        self.game.plot_field()

    def get_game_state(self, id):
        return self.game.return_game_state(id)

GameWrapper()
