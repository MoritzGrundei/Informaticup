import numpy as np
class Node:
    def __init__(self, x,y):
        # identify node by its x and y values
        self.x = x
        self.y = y
        self.pred = None
        self.dist = np.inf

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def set_pred(self, predecessor):
        self.pred = predecessor

    def get_pred(self):
        return self.pred

    def set_dist(self, distance):
        self.dist = distance

    def get_dist(self):
        return self.dist