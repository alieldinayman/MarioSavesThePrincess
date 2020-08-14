from Node import NodeState


class GridSolver:
    def __init__(self, grid, show_costs):
        self.grid = grid
        self.open = []
        self.closed = []
        self.show_costs = show_costs

    def traverse_grid(self):
        # Seed the solver's open list with the start node
        start = self.grid.start
        goal = self.grid.goal

        start.g_cost = 0
        start.h_cost = ((start.position[0] - goal.position[0]) ** 2) + ((start.position[1] - goal.position[1]) ** 2)
        start.f_cost = start.g_cost + start.h_cost

        self.open.append(start)

        while len(self.open) > 0:
            current = min(self.open, key=lambda n: n.f_cost)

            if self.show_costs is True:
                self.grid.print_cost_grid()
                print("Current node is: " + str(current.position) + "\n")

            self.open.remove(current)
            self.closed.append(current)

            if current.state == NodeState.GOAL:
                return self.get_shortest_path(goal), False

            for neighbour in self.get_valid_neighbours(current):
                neighbour.update_costs(current, self.grid.goal)
                if neighbour not in self.open:
                    self.open.append(neighbour)

        return None, True

    def get_valid_neighbours(self, node):
        valid_neighbours = []

        west = self.grid.get_node([node.position[0] - 1, node.position[1]])
        north = self.grid.get_node([node.position[0], node.position[1] + 1])
        east = self.grid.get_node([node.position[0] + 1, node.position[1]])
        south = self.grid.get_node([node.position[0], node.position[1] - 1])

        if west is not None and west.state is not NodeState.OBSTACLE and west not in self.closed:
            valid_neighbours.append(west)

        if north is not None and north.state is not NodeState.OBSTACLE and north not in self.closed:
            valid_neighbours.append(north)

        if east is not None and east.state is not NodeState.OBSTACLE and east not in self.closed:
            valid_neighbours.append(east)

        if south is not None and south.state is not NodeState.OBSTACLE and south not in self.closed:
            valid_neighbours.append(south)

        return valid_neighbours

    def get_shortest_path(self, goal):
        node = goal
        paths = []

        while node.parent is not None:
            paths.append(self.get_step_direction(node.parent.position, node.position))
            node = node.parent

        paths.reverse()
        return paths

    def get_step_direction(self, source, destination):
        if destination[1] == source[1] - 1:  # left
            return "LEFT"
        elif destination[0] == source[0] - 1:  # up
            return "UP"
        elif destination[1] == source[1] + 1:  # right
            return "RIGHT"
        elif destination[0] == source[0] + 1: # down
            return "DOWN"
