# SearchAlgorithms
# CSCI 561 Fall 2019
Global search strategies used in Artificial Intelligence

The goals is to implement the following algorithms to find the optimal path for navigation of a rover based on a particular objective.
- Breadth-first search (BFS)
- Uniform-cost search (UCS)
- A* search (A*)

It takes an input file that describes the terrain map, landing site, target sites, and characteristics of the robot. For each target site, an optimal safe path is found from the landing site to that target. A path is composed of a sequence of elementary moves. Each elementary move consists of moving the rover to one of its 8 neighbors. The algorithm will return an optimal path, that is, with shortest possible operational path length. If an optimal path cannot be found, the algorithm returns “FAIL”.
