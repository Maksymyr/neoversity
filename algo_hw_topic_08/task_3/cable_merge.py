import heapq


def min_merge_cost(cables: list[int]) -> int:
    if any(length < 0 for length in cables):
        raise ValueError("Cable lengths must be non-negative")
    if len(cables) < 2:
        return 0

    heap = list(cables)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        shorter = heapq.heappop(heap)
        longer = heapq.heappop(heap)
        cost = shorter + longer
        total += cost
        heapq.heappush(heap, cost)
    return total


if __name__ == "__main__":
    cables = [4, 3, 2, 6]
    print(f"Cables: {cables}")
    print(f"Minimum total merge cost: {min_merge_cost(cables)}")
