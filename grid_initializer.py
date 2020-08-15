from grid import Grid
from node import *


class GridInitializer:
    def __init__(self, n):
        self.grid = Grid()
        self.grid.size = n

    def populate_grid(self, data):
        if len(data) != self.grid.size:
            return None, True

        for i in range(self.grid.size):
            row = data[i]
            row_nodes = []

            if len(row) != self.grid.size:
                return None, True

            for j in range(self.grid.size):
                node, error_flag = self.initialize_node([i, j], row[j])

                if error_flag is True:
                    return None, error_flag

                row_nodes.append(node)

            self.grid.data.append(row_nodes)

        return self.grid, False

    def initialize_node(self, coordinates, symbol):
        if symbol == '-':
            node = Node(coordinates, NodeState.EMPTY)
        elif symbol == 'x':
            node = Node(coordinates, NodeState.OBSTACLE)
        elif symbol == 'm':
            node = Node(coordinates, NodeState.START)

            # Validate there is only one Mario
            if self.grid.start is None:
                self.grid.start = node
            else:
                return None, True

        elif symbol == 'p':
            node = Node(coordinates, NodeState.GOAL)

            # Validate there is only one Princess
            if self.grid.goal is None:
                self.grid.goal = node
            else:
                return None, True

        else:
            return None, True

        return node, False
