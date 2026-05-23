import math

from dijkstra import dijkstra, dijkstra_with_paths, reconstruct_path


def run_tests() -> None:
    # single vertex, no edges
    g1 = {"A": {}}
    assert dijkstra(g1, "A") == {"A": 0}

    # two vertices connected
    g2 = {"A": {"B": 5}, "B": {"A": 5}}
    assert dijkstra(g2, "A") == {"A": 0, "B": 5}

    # disconnected vertex is at infinity
    g3 = {"A": {"B": 1}, "B": {"A": 1}, "C": {}}
    assert dijkstra(g3, "A") == {"A": 0, "B": 1, "C": math.inf}

    # classic example from Cormen
    g_classic = {
        "s": {"t": 10, "y": 5},
        "t": {"x": 1, "y": 2},
        "y": {"t": 3, "x": 9, "z": 2},
        "x": {"z": 4},
        "z": {"s": 7, "x": 6},
    }
    assert dijkstra(g_classic, "s") == {"s": 0, "t": 8, "y": 5, "x": 9, "z": 7}

    # path reconstruction
    distances, preds = dijkstra_with_paths(g_classic, "s")
    assert reconstruct_path(preds, "x") == ["s", "y", "t", "x"]
    assert reconstruct_path(preds, "z") == ["s", "y", "z"]
    assert reconstruct_path(preds, "s") == ["s"]

    # negative weight raises
    g_neg = {"A": {"B": -1}, "B": {}}
    try:
        dijkstra(g_neg, "A")
        assert False, "expected ValueError for negative weight"
    except ValueError:
        pass

    # missing source raises
    try:
        dijkstra({"A": {}}, "Z")
        assert False, "expected ValueError for missing source"
    except ValueError:
        pass

    # the standard 6-vertex graph from the demo
    g_demo = {
        "A": {"B": 7, "C": 9, "F": 14},
        "B": {"A": 7, "C": 10, "D": 15},
        "C": {"A": 9, "B": 10, "D": 11, "F": 2},
        "D": {"B": 15, "C": 11, "E": 6},
        "E": {"D": 6, "F": 9},
        "F": {"A": 14, "C": 2, "E": 9},
    }
    expected = {"A": 0, "B": 7, "C": 9, "D": 20, "E": 20, "F": 11}
    assert dijkstra(g_demo, "A") == expected

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
