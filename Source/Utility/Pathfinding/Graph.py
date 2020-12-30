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
        reachable_nodes = []
        temp_edges = self.edges.copy()


        while len(starting_edges) > 0:
            for edge in starting_edges:
                if not edge.get_nodes()[0] in reachable_nodes:
                    reachable_nodes.append(edge.get_nodes()[0])
                    for temp_edge in temp_edges:
                        if edge.get_nodes()[0] in temp_edge.get_nodes() and not temp_edge in starting_edges:
                            starting_edges.append(temp_edge)

                if not edge.get_nodes()[1] in reachable_nodes:
                    reachable_nodes.append(edge.get_nodes()[1])
                    for temp_edge in temp_edges:
                        if edge.get_nodes()[1] in temp_edge.get_nodes() and not temp_edge in starting_edges :
                            starting_edges.append(temp_edge)
                starting_edges.remove(edge)
                temp_edges.remove(edge)
        return reachable_nodes

    # implementation of Dijkstra
    def get_shortest_path(self, dest_node):
        # initialize
        start_node = self.get_start_node()
        start_node.set_dist(0)
        nodes_queue = self.nodes.copy()

        #find shortest path (until dest_node)
        while len(nodes_queue) > 0:
            min_node = self.get_node_with_lowest_dist(nodes_queue)
            nodes_queue.remove(min_node)
            if min_node == dest_node:
                break
            neighbors, weights = self.get_neighbors(min_node)
            for i in range(len(neighbors)):
                new_dist = min_node.get_dist() + weights[i]
                if new_dist < neighbors[i].get_dist():
                    neighbors[i].set_dist(new_dist)
                    neighbors[i].set_pred(min_node)

        path = [dest_node]
        current_node = dest_node
        while current_node.get_pred():
            current_node = current_node.get_pred()
            path.append(current_node)
        return path[::-1]

    def get_node_with_lowest_dist(self, nodes):
        min_dist = np.inf
        min_node = None
        for node in nodes:
            if node.get_dist() < min_dist:
                min_dist = node.get_dist()
                min_node = node
        return min_node

    def get_neighbors(self, node):
        neighbors = []
        weights = []
        for edge in self.edges:
            if edge.get_nodes()[0] == node:
                neighbors.append(edge.get_nodes()[1])
            elif edge.get_nodes()[1] == node:
                neighbors.append(edge.get_nodes()[0])
            else:
                continue
            weights.append(edge.get_weight())
        return neighbors, weights

    def get_start_node(self):
        for node in self.nodes:
            if node.get_x() == self.current_position_x and node.get_y() == self.current_position_y:
                return node