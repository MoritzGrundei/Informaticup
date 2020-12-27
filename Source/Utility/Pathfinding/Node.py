
class Node:
    def __init__(self, x,y):
        # identify node by its x and y values
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"