# Player class
class Player:

    # setting up of variables
    def __inti__(self, player_id, x, y, name, direction):
        self.id = player_id
        self.x = x
        self.y = y
        self.speed = 1
        self.name = name
        self. direction = direction
        self.active = True

    def print_player(self):
        print("ID:" + str(self.id) + " x:" + str(self.x) + " y:" + str(self.y) + " speed:" + str(self.speed) + " direction:" + self.direction + " active:" + str(self.active))
    #function to return current x and y position
    def get_position(self):
        return self.x, self.y

    def get_speed(self):
        return self.speed

    def speed_up(self):
        self.speed = self.speed + 1

    def slow_down(self):
        self.speed = self.speed - 1

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