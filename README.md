# Maze Solver in Python 🧩
This repository contains a Python-based maze-solving algorithm that implements a Depth-First Search (DFS) approach and visualizes the solution using matplotlib.

# 🛠️ Features:
-Maze Parsing: Loads maze from a text file, handles walls, start, and goal points.

-Search Algorithms: Implements DFS for maze traversal and pathfinding.

-Solution Visualization: Displays the path from start to goal, highlighting the explored states and walls.

-Image Output: Saves the solution path as a PNG image, visually representing the maze and the solving process.

# 📚 How It Works:
-Load the Maze: The maze is loaded from a .txt file where A represents the start, B represents the goal, and # represents walls.

-Solve the Maze: The DFS algorithm explores the maze by traversing through possible moves (up, down, left, right), marking each state as explored.

-Visualize the Solution: Once the goal is reached, the path is plotted using matplotlib, showing walls, paths, start, and goal points. The solution is saved as a PNG file.
![maze_solution](https://github.com/user-attachments/assets/6d9c307a-4bb8-4cc7-b748-03a57e9b42ba)
