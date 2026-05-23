import heapq
import math
from typing import Hashable


Graph = dict[Hashable, dict[Hashable, float]]


def dijkstra(graph: Graph, source: Hashable) -> dict[Hashable, float]:
    if source not in graph:
        raise ValueError(f"source {source!r} is not in graph")

    distances: dict[Hashable, float] = {v: math.inf for v in graph}
    distances[source] = 0

    # heap entries: (distance, vertex)
    heap: list[tuple[float, Hashable]] = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        # stale entry — newer shorter path already processed
        if current_dist > distances[u]:
            continue
        for v, weight in graph[u].items():
            if weight < 0:
                raise ValueError(
                    f"negative weight on edge {u!r} -> {v!r}: {weight}; "
                    "Dijkstra requires non-negative weights"
                )
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return distances


def dijkstra_with_paths(
    graph: Graph, source: Hashable
) -> tuple[dict[Hashable, float], dict[Hashable, Hashable | None]]:
    if source not in graph:
        raise ValueError(f"source {source!r} is not in graph")

    distances: dict[Hashable, float] = {v: math.inf for v in graph}
    predecessors: dict[Hashable, Hashable | None] = {v: None for v in graph}
    distances[source] = 0

    heap: list[tuple[float, Hashable]] = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > distances[u]:
            continue
        for v, weight in graph[u].items():
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, predecessors


def reconstruct_path(
    predecessors: dict[Hashable, Hashable | None], target: Hashable
) -> list[Hashable]:
    path: list[Hashable] = []
    cur: Hashable | None = target
    while cur is not None:
        path.append(cur)
        cur = predecessors.get(cur)
    path.reverse()
    return path


if __name__ == "__main__":
    # Sample weighted undirected graph
    graph: Graph = {
        "A": {"B": 7, "C": 9, "F": 14},
        "B": {"A": 7, "C": 10, "D": 15},
        "C": {"A": 9, "B": 10, "D": 11, "F": 2},
        "D": {"B": 15, "C": 11, "E": 6},
        "E": {"D": 6, "F": 9},
        "F": {"A": 14, "C": 2, "E": 9},
    }

    source = "A"
    distances, preds = dijkstra_with_paths(graph, source)

    print(f"Shortest distances from {source!r}:")
    for v in sorted(distances):
        print(f"  {source} -> {v}: dist={distances[v]:>4}  path={' -> '.join(reconstruct_path(preds, v))}")
