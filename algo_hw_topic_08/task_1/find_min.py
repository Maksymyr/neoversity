class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: "Node | None" = None
        self.right: "Node | None" = None


class BST:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        self.root = _insert(self.root, value)


def _insert(node: Node | None, value: int) -> Node:
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = _insert(node.left, value)
    elif value > node.value:
        node.right = _insert(node.right, value)
    return node


def find_min(tree: BST) -> int:
    if tree.root is None:
        raise ValueError("Tree is empty")
    node = tree.root
    while node.left is not None:
        node = node.left
    return node.value


def build_bst(values: list[int]) -> BST:
    tree = BST()
    for value in values:
        tree.insert(value)
    return tree


if __name__ == "__main__":
    tree = build_bst([50, 30, 70, 20, 40, 60, 80, 10])
    print(f"Minimum value: {find_min(tree)}")
