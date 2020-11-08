from .Game import Game
import time

# wrapper class that is supposed to serve as an "interface" to other applications
class GameWrapper:
    # constructor expects width, height and a set of players that inherit methods from PlayerInterface
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
            print(self.get_game_state(1))
            for player in self.players:
                inputs.append(player.get_command(self.game.return_game_state(counter)))
                counter = counter + 1
            self.game.tick(inputs)
        self.game.plot_field()

    def get_game_state(self, id):
        return self.game.return_game_state(id)

