# My solution to [Advent of Code - Day 8](https://adventofcode.com/2023/day/8)


The trickiest part of Day 8 is Part 2 which I failed to solve by myself (I tried a bruteforce approach) and peeked at others solution.

Since I have not seen a very good explanation of why using the least common multiple of the number of steps to reach Z$ for all possible paths, here is my breakdown:


## Advent Of Code - Day 8, Part 2 Explainer

The key is to notice three things:

a) There are cycles in both the sample graph (sample3.txt) and the puzzle input graph.

b) The exists only one cycle for each walk from node ending in A to node ending in Z and that cycle is the cycle that starts and ends at node Z.
in other words: there is a unique *path* p from A to Z given the map instructions (L or R).

c) The number of steps n it takes to reach a node that ends in Z from a node that ends in A (i.e. the length of the path A->Z) is EQUAL to the number of steps of the cycle 
i.e. looping from node ending in Z back to node ending in Z.

For instance in the sample graph, the length of the path 11A -> 11Z is:
|11A -> 11B -> 11Z| = 2
which is equal to the length of the cycle:
|11Z -> 11B -> 11Z| = 2

Similarly for Path p' 22A -> 22Z:
| 22A -> 22B -> 22C -> 22Z | = 3
which is equal to the length of the cycle:
| 22Z -> 22B -> 22C -> 22Z | = 3

### Where does the least common multiple come into play?

In the example sample graph, the 11Z node will always be reached in an `2 + 2*k steps` | k = 1,2,3,..
2 steps for path 11A -> 11Z  + multiple of 2 for the cycle 11Z->11Z.

Similarly, the node 22Z will always be reached in `3*z steps` | z = 1,2,3,...

To reach 22Z and 11Z simultaneously, the number of steps need to be equal i.e. `3*(z) == 2*(k)`

Hence, the problem of finding the number of steps it takes to reach nodes ending in Z simultaneously is converted into
finding the least common multiple between 2 and 3.

Generally, the solution is given by lcm(steps_to_reach_z_path1, steps_to_reach_z_path2, ..., steps_to_reach_z_pathN)
