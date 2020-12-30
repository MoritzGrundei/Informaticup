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
        self.create_graph(width, height)
        self.get_connected_components()

    def create_graph(self, width, height):
        # create nodes
        for i in range(-4,5):
            for j in range(-4,5):
                node_x = self.current_position_x + i
                node_y = self.current_position_y + j
                #idea: include "dead" nodes for now
                #if x >= 0 and x < width and y >= 0 and y < height:
                self.nodes.append(Node(node_x, node_y))
        # create edges
        self.board[self.current_position_y][self.current_position_x] = 0
        for node in range(0,len(self.nodes),2):
            x = self.nodes[node].get_x()
            y = self.nodes[node].get_y()
            if 0 <= x < width and 0 <= y < height:

                # creates edge to right neighbor
                if x + 1 < width and x < self.current_position_x + 4:
                    if self.board[y][x] == 0  and self.board[y][x+1] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node+1], 1))

                # creates edge to left neighbor
                if x - 1 >= 0 and x > self.current_position_x - 4:
                    if self.board[y][x] == 0 and self.board[y][x-1] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node - 1], 1))

                # creates edge to upper neighbor
                if node >= 9 and y > 0 and y > self.current_position_y - 4:
                    if self.board[y][x] == 0 and self.board[y-1][x] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node - 9], 1))

                # creates edge to bottom neighbor
                if node < len(self.nodes) - 9 and y < height - 1 and y < self.current_position_y + 4:
                    if self.board[y][x] == 0 and self.board[y+1][x] == 0:
                        self.edges.append(Edge(self.nodes[node], self.nodes[node + 9], 1))
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
