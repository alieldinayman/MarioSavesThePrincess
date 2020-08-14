from grid_initializer import *
from grid_solver import *
import sys

if __name__ == "__main__":
    grid_initializer = GridInitializer()
    grid, error_flag = grid_initializer.populate_grid()

    if error_flag is True:
        sys.exit("An error occurred while populating the grid")

    grid_solver = GridSolver(grid, True)
    paths, error_flag = grid_solver.traverse_grid()

    if error_flag is True:
        sys.exit("There is no valid path to the princess")

    print("\nGoal reached in steps: " + str(paths), "\nError flag: " + str(error_flag))