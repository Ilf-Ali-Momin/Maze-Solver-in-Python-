import sys
import matplotlib.pyplot as plt

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    # class -> define a way to generate objects
    def __init__(self):  # Created a frontier that initially is empty (list)
        self.frontier = []

    def add(self, node):  # Add something to frontier
        self.frontier.append(node)  # append adds something at the end of the list

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)  # check if frontier contains a particular state

    def empty(self):  # check if frontier is empty
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")  # Nothing can be done if frontier is empty
        else:
            node = self.frontier[-1]  # remove last item (stack behavior)
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):  # Same approach, but remove from front (queue behavior)
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():
    def __init__(self, filename):
        # Read file and set height and width of the maze
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point (A)")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal (B)")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")  # Use block character for walls
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        """Finds a solution to the maze, if one exists."""

        self.num_explored = 0  # Count of states explored

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()  # Or QueueFrontier() for BFS
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                print(f"Number of states explored before failure: {self.num_explored}")
                raise Exception("No solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print(f"Number of states explored: {self.num_explored}")
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_xticks([])
        ax.set_yticks([])

        solution = self.solution[1] if self.solution is not None else None

        for i in range(self.height):
            for j in range(self.width):
                if self.walls[i][j]:
                    color = "black"
                elif (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.goal:
                    color = "red"
                elif show_solution and solution is not None and (i, j) in solution:
                    color = "blue"
                else:
                    color = "white"

                rect = plt.Rectangle((j, self.height - i - 1), 1, 1, facecolor=color, edgecolor='gray')
                ax.add_patch(rect)

        plt.savefig(filename)
        print(f"Maze image saved as {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python Maze.py maze1.txt")

    m = Maze(sys.argv[1])
    m.solve()
    m.print()
    m.output_image("maze_solution.png")
