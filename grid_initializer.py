from grid import Grid
from node import *


class GridInitializer:
    def __init__(self):
        self.grid = Grid()
        self.error_flag = False
        self.paths = []

    def populate_grid(self):
        try:
            n = int(input("Please insert your grid size (n): "))

        except ValueError:
            print("Please enter a valid number.")
            self.populate_grid()

        else:
            self.grid.size = n
            print("Please insert your grid row by row separating each node by a space: ")

            for i in range(n):
                row = input().split()
                row_nodes = []

                if len(row) != n:
                    return None, True

                for j in range(n):
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
            print("Invalid symbol")
            return None, True

        return node, False