from Source.Utility.Pathfinding.Node import Node


class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self):
        return "(" + str(self.node1) + "," +  str(self.node2) + "," +str(self.weight) + ")"