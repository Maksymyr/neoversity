from __future__ import annotations


class Node:
    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    def push_back(self, value: int) -> None:
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = node

    def to_list(self) -> list[int]:
        result: list[int] = []
        cur = self.head
        while cur is not None:
            result.append(cur.value)
            cur = cur.next
        return result

    @classmethod
    def from_list(cls, values: list[int]) -> "LinkedList":
        ll = cls()
        for v in values:
            ll.push_back(v)
        return ll

    def __repr__(self) -> str:
        return " -> ".join(str(v) for v in self.to_list()) or "<empty>"


def reverse(head: Node | None) -> Node | None:
    prev: Node | None = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def reverse_list(ll: LinkedList) -> LinkedList:
    ll.head = reverse(ll.head)
    return ll


def merge_sort(head: Node | None) -> Node | None:
    if head is None or head.next is None:
        return head
    mid = _split(head)
    left = merge_sort(head)
    right = merge_sort(mid)
    return _merge_sorted_nodes(left, right)


def _split(head: Node) -> Node | None:
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    assert slow is not None
    mid = slow.next
    slow.next = None
    return mid


def _merge_sorted_nodes(a: Node | None, b: Node | None) -> Node | None:
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def sort_list(ll: LinkedList) -> LinkedList:
    ll.head = merge_sort(ll.head)
    return ll


def merge_two_sorted(a: LinkedList, b: LinkedList) -> LinkedList:
    merged = LinkedList()
    merged.head = _merge_sorted_nodes(a.head, b.head)
    a.head = None
    b.head = None
    return merged


if __name__ == "__main__":
    ll = LinkedList.from_list([1, 2, 3, 4, 5])
    print(f"original: {ll}")
    print(f"reversed: {reverse_list(LinkedList.from_list([1, 2, 3, 4, 5]))}")

    unsorted = LinkedList.from_list([5, 1, 4, 2, 8, 3, 7, 6])
    print(f"unsorted: {unsorted}")
    print(f"  sorted: {sort_list(unsorted)}")

    a = LinkedList.from_list([1, 3, 5, 7])
    b = LinkedList.from_list([2, 4, 6, 8, 10])
    print(f"merge({a}, {b}) = {merge_two_sorted(a, b)}")
