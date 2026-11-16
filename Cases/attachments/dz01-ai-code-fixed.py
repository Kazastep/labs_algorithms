from __future__ import annotations
import random


def quicksort(data: list[int]) -> list[int]:
    """Sort integers using randomized three-way quicksort.

    Expected time complexity: O(n log n).
    Worst-case time complexity: O(n²).
    Expected recursion depth: O(log n).
    The input list is not modified.
    """
    if len(data) <= 1:
        return list(data)
    pivot = random.choice(data)
    smaller = [x for x in data if x < pivot]
    same = [x for x in data if x == pivot]
    larger = [x for x in data if x > pivot]
    return quicksort(smaller) + same + quicksort(larger)


if __name__ == "__main__":
    example = [5, 2, 9, 1, 7]
    print("Input :", example)
    print("Sorted:", quicksort(example))
