from InformatiCupGame.Player import Player
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
        directions = ["left", "right", "up", "down"]
        # initialize every player's starting position and id
        for i in range(1):
            player_id = i + 1
            x = randrange(width - 1)
            y = randrange(height - 1)
            self.board[y][x] = player_id
            name = "Player:" + str(id)
            direction = choice(directions)
            # Moritz: fixed typo in Player
            player = Player(player_id, x, y, name, direction)
            self.players.append(player)

    # checks if more than one player is still active
    def check_running(self):
        counter = 0
        for player in self.players:
            if player.get_active():
                counter = counter + 1
        if counter >= 1:
            self.running = True
        else:
            self.running = False

    # defines what happens for every tick of the game
    def tick(self):
        self.check_running()
        self.counter = self.counter + 1
        self.collect_inputs()
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
        if player.get_active() and new_x >= 0:
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
        if player.get_active() and new_x < self.width:
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
        if player.get_active() and new_y >= 0:
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
        if player.get_active() and new_y < self.height:
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
    def collect_inputs(self):
        for player in self.players:
            command = input("give command: ")
            print(command)
            player.process_command(command)

    def check_pos_in_field(self, x, y):
        if 0 <= x <= self.width and 0 <= y <= self.height-1:
            return True
        else:
            return False

    # print out all the metrics of the game
    def print_game_state(self):
        print(self.counter)
        for player in self.players:
            player.print_player()
        for i in range(self.height):
            print(self.board[i])
