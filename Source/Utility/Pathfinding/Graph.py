from Source.Utility.Pathfinding.Edge import Edge
from Source.Utility.Pathfinding.Node import Node
import numpy as np

class Graph:

    def __init__(self, board, current_position_x, current_position_y, width, height):
        self.current_position_x = current_position_x
        self.current_position_y = current_position_y
        self.board = board
        self.nodes = []
        self.edges = []
        self.create_graph(current_position_x, current_position_y, width, height)
        self.get_connected_components()

    def create_graph(self, current_position_x, current_position_y, width, height):
        # create nodes
        for i in range(-4,5):
            for j in range(-4,5):
                x = current_position_x + i
                y = current_position_y + j
                #idea: include "dead" nodes for now
                #if x >= 0 and x < width and y >= 0 and y < height:
                self.nodes.append(Node(x,y))
        # create edges
        print(self.board[current_position_x][current_position_y])
        for node in range(0,len(self.nodes),2):
            x = self.nodes[node].get_x()
            y = self.nodes[node].get_y()
            if 0 <= x < width and 0 <= y < height:

                # creates edge to right neighbor
                if x + 1 < width and x < current_position_x + 4:
                    print(
                        "checking: " + str((x, y)) + "to " + str((x + 1, y)) + ": " + str(self.board[x][y]) + " " + str(
                            self.board[x + 1][y]))
                    if self.board[x][y] == 0  and self.board[x + 1][y] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node+1], 1))

                # creates edge to left neighbor
                if x - 1 >= 0 and x > current_position_x - 4:
                    print(
                        "checking: " + str((x, y)) + "to " + str((x - 1, y)) + ": " + str(self.board[x][y]) + " " + str(
                            self.board[x - 1][y]))
                    if self.board[x][y] == 0 and self.board[x - 1][y] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node - 1], 1))

                # creates edge to upper neighbor
                if node >= 9 and y > 0 and y > current_position_y - 4:
                    print(
                        "checking: " + str((x, y)) + "to " + str((x, y - 1)) + ": " + str(self.board[x][y]) + " " + str(
                            self.board[x][y - 1]))
                    if self.board[x][y] == 0 and self.board[x][y-1] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node - 9], 1))

                # creates edge to bottom neighbor
                if node < len(self.nodes) - 9 and y < height - 1 and y < current_position_y + 4:
                    print(
                        "checking: " + str((x, y)) + "to " + str((x, y + 1)) + ": " + str(self.board[x][y]) + " " + str(
                            self.board[x][y + 1]))
                    if self.board[x][y] == 0 and self.board[x][y + 1] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node + 9], 1))
        print("edges length: " + str(len(self.edges)))
    def __str__(self):
        nodes = ""
        for i in range(len(self.nodes)):
            nodes = nodes + ", " + str(self.nodes[i])
        edges = ""
        for i in range(len(self.edges)):
            edges = edges + ", " + str(self.edges[i])

        return "nodes :" + nodes + "\nedges: " + edges

    def get_connected_components(self):
        start_node = None
        #get start node
        for node in self.nodes:
            if node.get_x() == self.current_position_x and node.get_y() == self.current_position_y:
                start_node = node
        starting_edges = []
        for edge in self.edges:
            if start_node in edge.get_nodes():
                starting_edges.append(edge)

        print("starting node: " + str(start_node))
        print("starting edges: ")
        for edge in starting_edges:
            print(str(edge))
