from enum import Enum
import math


class NodeState(Enum):
    EMPTY = 1
    OBSTACLE = 2
    START = 3
    GOAL = 4


class Node:
    def __init__(self, position, state):
        self.position = position
        self.state = state
        self.parent = None
        self.g_cost = None
        self.h_cost = None
        self.f_cost = None

    # Updates the node's costs whenever the node is approached by a new parent
    def update_costs(self, potential_parent, goal):
        if potential_parent is None:
            self.parent = potential_parent

        new_g_cost = potential_parent.g_cost + 1
        # Euclidean distance
        new_h_cost = math.sqrt((self.position[0] - goal.position[0]) ** 2 + (self.position[1] - goal.position[1]) ** 2)
        new_f_cost = new_g_cost + new_h_cost

        # Set the f_cost to a new value if it is null or if the new value is bigger than the current value
        if (self.f_cost is None) or (new_f_cost < self.f_cost):
            self.g_cost = new_g_cost
            self.f_cost = new_f_cost
            self.parent = potential_parent
