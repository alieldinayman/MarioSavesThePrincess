from controllers.grid import Grid
from controllers.node import Node, NodeState


class GridInitializer:
    def __init__(self, n):
        self.grid = Grid()
        self.grid.size = n

    # Validates the input data and populates a Grid instance with it
    def populate_grid(self, data):
        # Validate that the number of rows from the input is equal to n
        if len(data) != self.grid.size:
            return self.raise_error_flag()

        for i in range(self.grid.size):
            row = data[i]
            row_nodes = []

            # Validate that the number of nodes in the row is equal to n
            if len(row) != self.grid.size:
                return self.raise_error_flag()

            for j in range(self.grid.size):
                node, error_flag = self.initialize_node([i, j], row[j])

                if error_flag is True:
                    return self.raise_error_flag()

                row_nodes.append(node)

            self.grid.data.append(row_nodes)

        # Validate that the grid has a start and goal (Mario and Princess)
        if self.grid.start is None or self.grid.goal is None:
            return self.raise_error_flag()

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
                return self.raise_error_flag()

        elif symbol == 'p':
            node = Node(coordinates, NodeState.GOAL)

            # Validate there is only one Princess
            if self.grid.goal is None:
                self.grid.goal = node
            else:
                return self.raise_error_flag()

        # Invalid symbol
        else:
            return self.raise_error_flag()

        # Return the node if there were no issues
        return node, False

    def raise_error_flag(self):
        return None, True
