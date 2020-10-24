from .Player import Player
from random import randrange
from random import choice

# class representing the playing board and the game logic
class Game:

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.running = True
        self.counter = 0
        self.players = []
        directions = ("left", "right", "up", "down")
        for i in range(6):
           player_id = i+1
           x = randrange(width-1)
           y = randrange(height-1)
           name = "Player:" + id
           direction = choice(directions)
           player = Player(player_id, x, y, name, direction)
           self.players.append(player)

    # checks if more than one player is still active
    def check_running(self):
        counter = 0
        for player in self.players:
            if player.get_active() == True:
                counter = counter + 1
        if counter > 1:
            self.running = True
        else:
            self.running = False

    def get_player_position(self):

    def tick(self):
        for player in self.Players:
            old_x, old_y = player.get_position()
            # hier fehlt noch die Funktion um den Spieler seinen Befehl geben zu lassen
            player.move()
            new_x, new_y = player.get_position()
            if 0 < new_x < self.width - 1 or 0 < new_y < self.height - 1: #check if player still in range for playing field while moving horizontal or vertical
                if player.get_direction() == "right": #player moves right
                    if self.counter%6 != 0: #for normal turn (no jump)
                        for i in range(new_x - old_x):
                            if self.board[new_y[old_x + i]] == 0:
                                self.board[new_y[old_x + i]] = player.get_id()
                            else:
                                player.deactivate()
                                break
                    else: #for every 6th turn make the player "jump"
                        if (self.board[new_y[old_x + 1]] != 0) or (self.board[new_y[new_x]] != 0):
                            player.deactivate()
                            break
                        else:
                            self.board[new_y[old_x + 1]] = player.get_id()
                            self.board[new_y[new_x]] = player.get_id()

                elif player.get_direction() == "left": #player moves left
                    if self.counter%6 != 0: #normal turn (no jump)
                        for i in range(old_x - new_x):
                            if self.board[new_y[old_x - i]] == 0:
                                self.board[new_y[old_x - i]] == player.get_id()
                            else:
                                player.deactivate()
                                break
                    else: #for every 6th turn make the player "jump"
                        if (self.board[new_y[old_x - 1]] != 0) or (self.board[new_y[new_x]] != 0):
                            player.deactivate()
                            break
                        else:
                            self.board[new_y[old_x - 1]] = player.get_id()
                            self.board[new_y[new_x]] = player.get_id()

                elif player.get_direction() == "up": #player moves upwards

            else:
                player.deactivate()