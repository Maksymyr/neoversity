import uuid
from collections import deque
from typing import Callable

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


def gradient_color(step: int, total: int, base_hue: tuple[int, int, int] = (18, 150, 240)) -> str:
    """Generate a colour for visit number `step` (0..total-1).
    The first visited node gets the darkest shade, the last — the lightest.
    Returns a #RRGGBB hex string.
    """
    if total <= 1:
        ratio = 0.0
    else:
        ratio = step / (total - 1)
    # interpolate between dark (factor 0.25) and light (factor 1.0)
    factor = 0.25 + 0.75 * ratio
    r, g, b = base_hue
    rr = min(255, int(r * factor + (255 - r) * (ratio * 0.4)))
    gg = min(255, int(g * factor + (255 - g) * (ratio * 0.4)))
    bb = min(255, int(b * factor + (255 - b) * (ratio * 0.4)))
    return f"#{rr:02X}{gg:02X}{bb:02X}"


def count_nodes(root: Node | None) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def dfs_iterative(root: Node | None) -> list[Node]:
    """Iterative DFS using a stack — left child visited before right (pre-order)."""
    if root is None:
        return []
    order: list[Node] = []
    stack: list[Node] = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        # push right first so left is popped first
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def bfs_iterative(root: Node | None) -> list[Node]:
    """Iterative BFS using a queue — level-order traversal."""
    if root is None:
        return []
    order: list[Node] = []
    queue: deque[Node] = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


def draw_traversal(root: Node, traversal: Callable[[Node | None], list[Node]], title: str) -> None:
    visit_order = traversal(root)
    total = len(visit_order)
    # assign gradient colours by visit order
    for step, node in enumerate(visit_order):
        node.color = gradient_color(step, total)

    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(tree, root, pos)

    colors = [tree.nodes[n]["color"] for n in tree.nodes]
    # label: "value (step+1)"
    visit_step = {node.id: i + 1 for i, node in enumerate(visit_order)}
    labels = {
        n: f"{tree.nodes[n]['label']}\n#{visit_step.get(n, '?')}"
        for n in tree.nodes
    }

    plt.figure(figsize=(10, 6))
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


def build_sample_tree() -> Node:
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.right = Node(8)
    root.right.right.left = Node(7)
    return root


if __name__ == "__main__":
    print("DFS (stack, pre-order):")
    root = build_sample_tree()
    draw_traversal(root, dfs_iterative, title="DFS traversal (stack, pre-order)")

    print("BFS (queue, level-order):")
    root = build_sample_tree()
    draw_traversal(root, bfs_iterative, title="BFS traversal (queue, level-order)")
