import re
#import concurrent.futures
from math import lcm

node_description_regex = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

class Node:
    def __init__(self, value, left_node, right_node):
        self.value = value
        self.left = left_node
        self.right = right_node



def puzzle_reader_factory(puzzle_input_file):
    with open(puzzle_input_file) as pf:
        for line in pf:
            yield line


if __name__ == "__main__":
    PUZZLE_FILENAME = "input.txt"
    puzzle_reader = puzzle_reader_factory(PUZZLE_FILENAME)

    traverse_instructions = next(puzzle_reader)
    traverse_instructions = traverse_instructions.strip()

    next(puzzle_reader) # skip empty line

    allocated_nodes_map = {}

    for node_index, node_description in enumerate(puzzle_reader):
        matches = node_description_regex.match(node_description)
        iter_node_value = matches[1]
        left_node_value = matches[2]
        right_node_value = matches[3]

        if iter_node_value not in allocated_nodes_map:
            allocated_nodes_map[iter_node_value] = Node(iter_node_value, None, None)

        if left_node_value not in allocated_nodes_map:
            allocated_nodes_map[left_node_value] = Node(left_node_value, None, None)
        
        if right_node_value not in allocated_nodes_map:
            allocated_nodes_map[right_node_value] = Node(right_node_value, None, None)

        allocated_nodes_map[iter_node_value].left = allocated_nodes_map[left_node_value]
        allocated_nodes_map[iter_node_value].right = allocated_nodes_map[right_node_value]


    ##Test whether inserted corectly
    for node in allocated_nodes_map.values():
        print(node.value, node.left.value if node.left is not None else "None", node.right.value if node.right is not None else "None")

    def part1():
        node = allocated_nodes_map["AAA"]
        j = 0
        while(True):
            #print(node.value, j % len(traverse_instructions))
            if node.value == "ZZZ":
                break

            if traverse_instructions[j % len(traverse_instructions)] == "L":
                node = node.left

            if traverse_instructions[j % len(traverse_instructions)] == "R":
                node = node.right

            j += 1

        print(f"Found ZZZ in {j} steps.")


    def take_step(node, j):
        if traverse_instructions[j] == "L":
            node = node.left

        if traverse_instructions[j] == "R":
            node = node.right

        return node, node.value[-1] == "Z", j+1 if j+1 < len(traverse_instructions) else 0


    def part2_bruteforce(): # This was my initial approach; It works in the sample but not in the puzzle input.

        start_nodes = [allocated_nodes_map[key] for key in allocated_nodes_map.keys() if key[-1] == "A"]

        print("###Start nodes###")
        print([node.value for node in start_nodes])

        js = [0] * len(start_nodes)

        num_steps = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(start_nodes)) as executor:
            while(True):
                iter_nodes, iter_reached_Z, iter_js = zip(*executor.map(take_step, start_nodes, js))
                js = list(iter_js) # update map position
                num_steps +=1
                reached_Z = list(iter_reached_Z)
                if all(reached_Z): # if all nodes end in Z, break#
                    break
                start_nodes = list(iter_nodes) # set start_nodes to end_nodes.

        print(f"All nodes end in Z after {num_steps} steps")

    def part2():
        '''
        The key is to notice three things:
        a) There are cycles in both the sampe graph and the puzzle input graph.
        b) The exists only one node that ends in Z for each path.
        c) The number of steps n it takes to reach a node that ends in Z from a node that ends in A is EQUAL to the number of steps of the cycle 
        i.e. looping from node ending in Z back to node ending in Z.

        For instance in the sample graph, the length of the path 11A -> 11Z is:
        |11A -> 11B -> 11Z| = 2
        which is equal to the length of the cycle:
        |11Z -> 11B -> 11Z| = 2

        Similarly for Path p' 22A -> 22Z:
        | 22A -> 22B -> 22C -> 22Z | = 3
        which is equal to the length of the cycle:
        | 22Z -> 22B -> 22C -> 22Z | = 3

        # Where does the least common multiple come into play?

        In the example sample graph, the 11Z node will always be reached in an 2 + 2*k steps | k = 1,2,3,..
        2 steps for path 11A -> 11Z  + multiple of 2 for the cycle 11Z->11Z.

        Similarly, the node 22Z will always be reached in 3*z steps | z = 1,2,3,...

        To reach 22Z and 11Z simultaneously, the number of steps need to be equal i.e. 3*(z) == 2*(k)

        Hence, the problem of finding the number of steps it taken to reach nodes ending in Z simultaneously is converted into
        finding the least common multiple between 2 and 3.

        Generally, the solution is given by lcm(steps_to_reach_z_path1, steps_to_reach_z_path2, ..., steps_to_reach_z_pathN)
        '''
        start_nodes = [allocated_nodes_map[key] for key in allocated_nodes_map.keys() if key[-1] == "A"]

        steps = [0] * len(start_nodes)
        for idx, node in enumerate(start_nodes):
            j = 0
            while(node.value[-1] != "Z"):
                direction = traverse_instructions[j]
                if direction == "L":
                    node = node.left
                else:
                    node = node.right
                steps[idx] += 1
                j = j+1 if j+1 != len(traverse_instructions) else 0

        lcm_steps = lcm(*steps)

        print(steps)
        print(f"All nodes end in Z after {lcm_steps} steps")

    part2()
