import heapq
import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color: str = "skyblue") -> None:
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph: nx.DiGraph, node: Node | None, pos: dict, x: float = 0, y: float = 0, layer: int = 1) -> nx.DiGraph:
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def heap_to_tree(heap: list[int], color: str = "skyblue") -> Node | None:
    """Convert a heap (array form, parent at i, children at 2i+1 / 2i+2) to a Node tree."""
    if not heap:
        return None

    nodes = [Node(value, color=color) for value in heap]
    n = len(nodes)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n:
            nodes[i].left = nodes[left]
        if right < n:
            nodes[i].right = nodes[right]
    return nodes[0]


def draw_heap(heap: list[int], title: str | None = None) -> None:
    root = heap_to_tree(heap)
    if root is None:
        print("Empty heap — nothing to draw.")
        return

    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(tree, root, pos)

    colors = [tree.nodes[n]["color"] for n in tree.nodes]
    labels = {n: tree.nodes[n]["label"] for n in tree.nodes}

    plt.figure(figsize=(10, 6))
    if title:
        plt.title(title)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
    )
    plt.show()


if __name__ == "__main__":
    values = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
    heap = values[:]
    heapq.heapify(heap)
    print(f"input:        {values}")
    print(f"min-heap arr: {heap}")
    print("(level-order: heap[0] is root, heap[2i+1]/heap[2i+2] are children)")
    draw_heap(heap, title=f"Min-heap of {values}")
