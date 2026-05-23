from tree_traversal import (
    Node,
    bfs_iterative,
    build_sample_tree,
    dfs_iterative,
    gradient_color,
)


def run_tests() -> None:
    # empty tree
    assert dfs_iterative(None) == []
    assert bfs_iterative(None) == []

    # single node
    only = Node(42)
    assert [n.val for n in dfs_iterative(only)] == [42]
    assert [n.val for n in bfs_iterative(only)] == [42]

    # sample tree from the task code:
    #         0
    #        / \
    #       4   1
    #      / \ / \
    #     5  10 3 8
    #             /
    #            7
    root = build_sample_tree()
    assert [n.val for n in dfs_iterative(root)] == [0, 4, 5, 10, 1, 3, 8, 7]
    assert [n.val for n in bfs_iterative(root)] == [0, 4, 1, 5, 10, 3, 8, 7]

    # gradient: returns valid hex strings, first is darker than last (lower sum of RGB)
    total = 8
    first = gradient_color(0, total)
    last = gradient_color(total - 1, total)
    assert first.startswith("#") and len(first) == 7
    assert last.startswith("#") and len(last) == 7

    def brightness(hex_color: str) -> int:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return r + g + b

    assert brightness(first) < brightness(last), (first, last)

    # all colors are distinct (sequence of 10 colors)
    colors = [gradient_color(i, 10) for i in range(10)]
    assert len(set(colors)) == 10

    # monotonic: each next color is brighter
    for i in range(1, len(colors)):
        assert brightness(colors[i - 1]) < brightness(colors[i])

    # singleton total
    assert gradient_color(0, 1).startswith("#")

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
