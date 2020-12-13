import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import os
import json

from Source.InformatiCupGame.Player import Player
from random import randrange
from random import choice
import logreset



# class representing the playing board and the game logic
class Game:

    def __init__(self, height, width, player_count, logging_id):
        # set up logging, use unique logging_id as Game identifier
        logreset.reset_logging()
        self.logging_id = logging_id
        mkdir_p(os.path.dirname('logs/' + str(self.logging_id) + '/Game.log'))
        logging.basicConfig(filename='logs/' + str(self.logging_id) + '/Game.log', level=logging.INFO)
        self.logger = logging.getLogger()
        self.winner = 0
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.running = True
        self.counter = 0
        self.players = []
        directions = ["left", "right", "up", "down"]
        # initialize every player's starting position and id
        for i in range(player_count):
            player_id = i + 1
            x = randrange(1, width - 2)
            y = randrange(1, height - 2)
            self.board[y][x] = player_id
            name = "Player:" + str(id)
            direction = choice(directions)
            player = Player(player_id, x, y, name, direction, logging_id)
            self.players.append(player)


    def get_winner(self):
        return self.winner
    # checks if more than one player is still active
    def check_running(self):
        counter = 0
        for player in self.players:
            if player.get_active():
                counter = counter + 1
                self.winner = player.get_id()
        if counter > 1:
            self.running = True
        else:
            self.running = False
            #print("Winner: " + str(self.winner))
            self.logger.info("Winner: " + str(self.winner))



    # defines what happens for every tick of the game
    def tick(self, inputs):
        self.check_running()
        self.counter = self.counter + 1
        if self.running:
            self.collect_inputs(inputs)
            for player in self.players:
                old_x, old_y = player.get_position()
                player.move()
                new_x, new_y = player.get_position()
                if player.get_direction() == "right":  # player moves right
                    self.move_player_right(old_x, new_x, old_y, new_y, player)

                elif player.get_direction() == "left":  # player moves left
                    self.move_player_left(old_x, new_x, old_y, new_y, player)

                elif player.get_direction() == "up":  # player moves upwards
                    self.move_player_up(old_x, new_x, old_y, new_y, player)

                elif player.get_direction() == "down":  # player moves downwards
                    self.move_player_down(old_x, new_x, old_y, new_y, player)

                else:  # invalid player direction
                    player.deactivate()

    # move player left
    def move_player_left(self, old_x, new_x, old_y, new_y, player):
        if player.get_active() and new_x >= 0 and new_x < self.width and new_y < self.height and new_y >= 0:
            if self.counter % 6 != 0:  # normal turn (no jump)
                for i in range(old_x - new_x):
                    # cell was previously empty and is in range of board
                    if self.board[new_y][old_x - i-1] == 0 and self.check_pos_in_field(old_x - i-1, new_y):
                        self.board[new_y][old_x - i-1] = player.get_id()
                    else:
                        player.deactivate()
                        break
            else:  # for every 6th turn make the player "jump"
                if (self.board[new_y][old_x - 1] != 0) or (self.board[new_y][new_x] != 0):
                    player.deactivate()
                else:
                    self.board[new_y][old_x - 1] = player.get_id()
                    self.board[new_y][new_x] = player.get_id()
        else:
            player.deactivate()

    # move player right works like other move methods
    def move_player_right(self, old_x, new_x, old_y, new_y, player):
        if player.get_active() and new_x < self.width and new_x >= 0 and new_y < self.height and new_y >= 0:
            if self.counter % 6 != 0:
                for i in range(new_x - old_x):
                    if self.board[new_y][old_x + i+1] == 0 and self.check_pos_in_field(old_x + i+1, new_y):
                        self.board[new_y][old_x + i+1] = player.get_id()
                    else:
                        player.deactivate()
                        break
            else:
                if (self.board[new_y][old_x + 1] != 0) or (self.board[new_y][new_x] != 0):
                    player.deactivate()
                else:
                    self.board[new_y][old_x + 1] = player.get_id()
                    self.board[new_y][new_x] = player.get_id()
        else:
            player.deactivate()

    # move player up works like other move methods
    def move_player_up(self, old_x, new_x, old_y, new_y, player):
        if player.get_active() and new_y >= 0 and new_y < self.height and new_x < self.width and new_x >= 0:
            if self.counter % 6 != 0:
                for i in range(old_y - new_y):
                    if self.board[old_y - i-1][new_x] == 0 and self.check_pos_in_field(new_x, old_y - i-1):
                        self.board[old_y - i-1][new_x] = player.get_id()
                    else:
                        player.deactivate()
                        break
            else:
                if (self.board[old_y - 1][new_x] != 0) or (self.board[new_y][new_x] != 0):
                    player.deactivate()
                else:
                    self.board[old_y - 1][new_x] = player.get_id()
                    self.board[new_y][new_x] = player.get_id()
        else:
            player.deactivate()

    # move player down works like other move methods
    def move_player_down(self, old_x, new_x, old_y, new_y, player):
        if player.get_active() and new_y < self.height and new_y >= 0 and new_x < self.width and new_x >= 0:
            if self.counter % 6 != 0:
                for i in range(new_y - old_y):
                    if self.board[old_y + i+1][new_x] == 0 and self.check_pos_in_field(new_x, old_y + i+1):
                        self.board[old_y + i+1][new_x] = player.get_id()
                    else:
                        player.deactivate()
                        break
            else:
                if (self.board[old_y + 1][new_x] != 0) or (self.board[new_y][old_x] != 0):
                    player.deactivate()
                else:
                    self.board[old_y + 1][new_x] = player.get_id()
                    self.board[new_y][new_x] = player.get_id()
        else:
            player.deactivate()

    # collect the inputs for every player
    def collect_inputs(self, inputs):
        for player in self.players:
            command = inputs[player.get_id()-1]
            player.process_command(command)

    def check_pos_in_field(self, x, y):
        if 0 <= x <= self.width and 0 <= y <= self.height-1:
            return True
        else:
            return False

    # print out all the metrics of the game
    def log_game_state(self):
        self.logger.info(self.counter)
        for player in self.players:
            player.log_player(self.logger)
        for i in range(self.height):
            self.logger.info(self.board[i])

    # returns game state in json-like (dictionary) format that is supposed to mimic the real games report file
    def return_game_state(self, id):
        state_json = json.dumps(
            {'width': self.width,
             'height': self.height,
             'cells': self.board,
             'players': self.get_players_dict(),
             'you': id,
             'running': self.players[id - 1].get_active()
             }
        )
        return state_json

    # returns a json-like (dictionary) player representation
    def get_players_dict(self):
        players_dict = {}
        for player in self.players:
            players_dict[player.get_id()] = {
                'x': player.get_position()[0],
                'y': player.get_position()[1],
                'direction': player.get_direction(),
                'speed': player.get_speed(),
                'active': player.get_active()
              }
        return players_dict

    def plot_field(self):

        bounds = [0, 0, 1, 2, 3, 4, 5, 6]
        cmap = mpl.colors.ListedColormap(['white', 'red', 'green', 'blue', 'brown', 'orange', 'cyan'])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        #plt.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), ticks=bounds)
        plt.imshow(self.board, cmap=cmap)
        plt.savefig('logs/' + str(self.logging_id) + '/result' + '.png')
        plt.close()

    def get_counter(self):
        return self.counter

# create logging dir -> move to utils?
def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
