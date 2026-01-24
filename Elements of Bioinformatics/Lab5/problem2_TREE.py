#Completing a Tree
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = """10
1 2
2 8
4 10
5 9
6 10
7 9"""

def ParseInput(data):
    lines = data.strip().split("\n")
    n = int(lines[0])
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    return n, edges

def MinToProduceTree(n, edges):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = 0

    for node in range(1, n + 1):
        if node not in visited:
            components += 1
            queue = deque([node])
            visited.add(node)

            while queue:
                current = queue.popleft()
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components - 1

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_tree.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    n, edges = ParseInput(data)
    result = MinToProduceTree(n, edges)

    pyperclip.copy(result)
    print(result)