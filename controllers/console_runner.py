from controllers.grid_solver import GridSolver
import sys


# The console runner module allows for running/debugging the backend logic without communicating with the server/web app
if __name__ == "__main__":

    while True:
        try:
            n = int(input("Please insert your grid size (n): "))

        except ValueError:
            print("Please enter a valid number.")

        else:
            break

    print("Please insert your grid row by row separating each node by a space: ")
    grid = []

    # Split the input grid into n rows
    for i in range(n):
        grid.append(input().split())

    # Call the grid solver class to validate and solve the grid
    grid_solver = GridSolver()
    paths, error_flag = grid_solver.solve_grid(n, grid)

    if error_flag is True:
        sys.exit("Grid is not valid or there is no valid path to the princess")

    print("\nGoal reached in steps: " + str(paths), "\nError flag: " + str(error_flag))