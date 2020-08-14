from Node import NodeState


class Grid:
    def __init__(self):
        self.size = 0
        self.data = []
        self.start = None
        self.goal = None

    def get_node(self, coordinates):
        if (coordinates[0] < 0 or coordinates[0] > self.size - 1) or \
                (coordinates[1] < 0 or coordinates[1] > self.size - 1):
            return None

        req_node = self.data[coordinates[0]][coordinates[1]]

        if req_node is not None:
            return req_node

    def print_grid(self):
        for row in self.data:
            for node in row:
                print(str(node.position) + ": " + str(node.state), end=" ")  # Row's nodes separated by a space
            print("")  # New line

    def print_raw_grid(self):
        print(self.data)

    def print_cost_grid(self):
        for row in self.data:
            for node in row:
                if node.f_cost is None:
                    if node.state == NodeState.EMPTY:
                        print("-", end="   ")
                    elif node.state == NodeState.OBSTACLE:
                        print("x", end="   ")
                    elif node.state == NodeState.GOAL:
                        print("p", end="   ")
                else:
                    print(str(round(node.f_cost, 1)), end="   ")  # Row's nodes separated by a space

            print("")  # New line
