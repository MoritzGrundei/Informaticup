import logging

# Player class that serves as a direct representation of Player in the Game. Be aware that this is NOT the agent
class Player:

    # setting up variables
    def __init__(self, player_id, x, y, name, direction, logging_id):
        # set up logging, use unique logging_id as Game identifier
        self.id = player_id
        self.x = x
        self.y = y
        self.speed = 1
        self.name = name
        self. direction = direction
        self.active = True

    def log_player(self, logger):
        logger.info("ID:" + str(self.id) + " x:" + str(self.x) + " y:" + str(self.y) + " speed:" + str(self.speed) + " direction:" + self.direction + " active:" + str(self.active))
    #function to return current x and y position
    def get_position(self):
        return self.x, self.y

    def get_speed(self):
        return self.speed

    def speed_up(self):
        self.speed = self.speed + 1
        if self.speed > 10:
            self.deactivate()

    def slow_down(self):
        self.speed = self.speed - 1
        if self.speed < 0:
            self.deactivate()

    # function in case the player changes nothing
    def change_nothing(self):
        return

    # function to deactivate player once he lost
    def deactivate(self):
        self.active = False

    def get_active(self):
        return self.active

    def get_id(self):
        return self.id

    def get_direction(self):
        return self.direction

    # fuction to turn the player left depending on previous direction
    def turn_left(self):
        if self.direction == "up":
            self.direction = "left"

        elif self.direction == "left":
            self.direction = "down"

        elif self.direction == "down":
            self.direction = "right"

        else:
            self.direction = "up"

    # function to turn the player right based on previus direction
    def turn_right(self):
        if self.direction == "up":
            self.direction = "right"

        elif self.direction == "right":
            self.direction = "down"

        elif self.direction == "down":
            self.direction = "left"

        else:
            self.direction = "up"

    # function to calculate the new position of the player
    # takes the player object
    # return the new x and y pos as tuple
    def move(self):
        if self.direction == "down":
            self.y = self.y + self.speed

        elif self.direction == "up":
            self.y = self.y - self.speed

        elif self.direction == "right":
            self.x = self.x + self.speed

        else:
            self.x = self.x - self.speed

        new_pos = {self.x, self.y}

        return new_pos

    def process_command(self, command):
        if command == "turn_right":
            self.turn_right()
        elif command == "speed_up":
            self.speed_up()
        elif command == "slow_down":
            self.slow_down()
        elif command == "turn_left":
            self.turn_left()
        elif command == "change_nothing":
            self.change_nothing()
        else:
            self.deactivate()