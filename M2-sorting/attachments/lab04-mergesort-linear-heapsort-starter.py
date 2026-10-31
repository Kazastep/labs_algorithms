#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 4. MergeSort, Counting, Radix и HeapSort: оценка производительности — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-04 и правилами использования генеративного ИИ
(docs/ai-verification.md). QuickSort перенесите из собственной ЛР 3.

Запуск: python lab04-mergesort-linear-heapsort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Сортировки (реализуются вручную; sorted() используется только как эталон)
# ---------------------------------------------------------------------------


def merge(left: list, right: list, key) -> list:
    """Стабильное слияние двух отсортированных списков в новый список.

    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: O(n).
    """
    # TODO: два индекса, сравнение key(left[i]) <= key(right[j])
    merge_arr = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merge_arr.append(left[i])
            i += 1
        else:
            merge_arr.append(right[j])
            j += 1

    merge_arr.extend(left[i:])
    merge_arr.extend(right[j:])

    return merge_arr





def merge_sort(a: list, key=lambda x: x) -> list:
    """MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: TODO."""
    # TODO: рекурсивное деление пополам + merge()
    if len(a) <= 1:
        return a
    
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])

    return merge(left, right, key)


def counting_sort(a: list[int], key_max: int) -> list[int]:
    """Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].

    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память:     
    Время: O(n + k).
    Память: O(n + k), где k = key_max + 1.
    """
    # TODO: реализовать; проход расстановки — с конца массива (иначе теряется устойчивость)
    count = [0] * (key_max + 1)

    for num in a:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    result = [0] * len(a)

    for i in range(len(a) - 1, -1, -1):
        num = a[i]
        position = count[num] - 1

        result[position] = num
        count[num] -= 1

    return result


def radix_sort_lsd(a: list[int]) -> list[int]:
    """RadixSort LSD по десятичным разрядам, неотрицательные целые.

    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему.
    Время: O(d * (n + 10)) = O(d * n).
    Память: O(n + 10) = O(n).
    n — количество элементов массива.
    d — количество разрядов максимального числа.
    k — основание системы счисления (у нас 10).
    """
    # TODO: цикл по разрядам (exp = 1, 10, 100, ...) с устойчивой сортировкой
    # по цифре (a[i] // exp) % 10; объяснить, почему без устойчивости
    # внутреннего прохода алгоритм неверен
    if not a:
        return []

    result = a.copy()
    max_num = max(result)
    exp = 1

    while max_num // exp > 0:
        count = [0] * 10
        output = [0] * len(result)

        for num in result:
            digit = (num // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(len(result) - 1, -1, -1):
            num = result[i]
            digit = (num // exp) % 10

            position = count[digit] - 1
            output[position] = num
            count[digit] -= 1

        result = output
        exp *= 10

    return result


def sift_down(a: list[int], i: int, n: int) -> None:
    """Просейка вниз элемента i в куче a[0:n] (max-heap), на месте."""
    # TODO: спуск с обменом с большим из потомков, пока нарушено свойство кучи
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < n and a[left] > a[largest]:
            largest = left

        if right < n and a[right] > a[largest]:
            largest = right

        if largest == i:
            break

        a[i], a[largest] = a[largest], a[i]
        i = largest


def heap_sort(a: list[int]) -> None:
    """HeapSort in-place: сортирует список a на месте, без вспомогательного массива.

    Схема: построение max-кучи просейками вниз (снизу вверх, O(n)),
    затем обмен вершины с последним элементом и просейка.     
    Время: O(n log n).
    Дополнительная память: O(1)..
    """
    # TODO: построение кучи + фаза извлечения максимумов
    n = len(a)

    # 1. Построение max-heap снизу вверх
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)

    # 2. Извлечение максимальных элементов
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)


def quick_sort(a: list[int]) -> list[int]:
    """QuickSort с рандомизацией опорного элемента — перенести из своей ЛР 3."""
    # TODO: скопировать собственную реализацию из ЛР 3 (КИМ-03)
    # Средняя ожидаемая сложность: O(n log n).
    # Худшая сложность: O(n²).
    if len(a) <= 1:
        return a.copy()

    pivot = random.choice(a)

    left = [x for x in a if x < pivot]
    middle = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# ---------------------------------------------------------------------------
# 2. Верификация: инварианты + сверка с эталоном sorted()
#    (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Граничные и типовые случаи, стабильность, сверка с эталоном sorted()."""
    # Граничные случаи: пустой массив, один элемент, все элементы равны
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([5, 5, 5]) == [5, 5, 5]
    assert counting_sort([], key_max=10) == []
    assert radix_sort_lsd([0]) == [0]
    single = [42]
    heap_sort(single)
    assert single == [42]

    # Стабильность слияния: пары (ключ, порядковый номер); эталон sorted() стабилен,
    # поэтому при равных ключах порядок номеров обязан совпасть
    rng = random.Random(0)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    assert merge_sort(pairs, key=lambda p: p[0]) == sorted(pairs, key=lambda p: p[0])

    # Случайные тесты: инвариант перестановки + сверка с эталоном
    for _ in range(200):
        a = [rng.randint(0, 999) for _ in range(rng.randint(0, 60))]
        expected = sorted(a)
        assert merge_sort(a) == expected
        assert counting_sort(a, key_max=999) == expected
        assert radix_sort_lsd(a) == expected
        buf = list(a)
        heap_sort(buf)
        assert buf == expected
        assert sorted(buf) == expected  # выход — перестановка входа
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 3. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5
SMALL_KEY_MAX = 100        # узкий диапазон: counting уместен
WIDE_KEY_MAX = 10**9       # широкий диапазон: counting теряет смысл (обсудить в отчёте)


def make_datasets(rng: random.Random, n: int) -> dict[str, list[int]]:
    """Массивы разных распределений и диапазонов ключей для размера n."""
    almost = list(range(n))
    for _ in range(max(1, n // 100)):  # ~1 % случайных обменов
        i, j = rng.randrange(n), rng.randrange(n)
        almost[i], almost[j] = almost[j], almost[i]
    return {
        "random_wide": [rng.randint(0, WIDE_KEY_MAX) for _ in range(n)],
        "random_small": [rng.randint(0, SMALL_KEY_MAX) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "almost_sorted": almost,
    }


def bench(fn, data: list[int]) -> float:
    """Медиана времени fn на копии data по REPEATS запускам, с прогревом.

    Каждый запуск получает свежую копию: сортировка на месте не должна
    превращать последующие запуски в сортировку уже отсортированного массива.
    """
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        buf = list(data)
        t0 = time.perf_counter()
        fn(buf)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    rng = random.Random(seed)

    algorithms = [
        ("merge_sort", merge_sort),
        ("counting_sort", lambda a: counting_sort(a, key_max=max(a, default=0))),
        ("radix_sort_lsd", radix_sort_lsd),
        ("heap_sort", heap_sort),
        ("quick_sort (ЛР 3)", quick_sort),
        ("sorted() (эталон)", sorted),
    ]

    # Сохраняем результаты измерений
    results = {}

    for n in SIZES:
        datasets = make_datasets(rng, n)
        print(f"\nn = {n}:")

        for dist_name, data in datasets.items():
            print(f"  распределение {dist_name}:")

            if dist_name not in results:
                results[dist_name] = {}

            for algo_name, fn in algorithms:

                if algo_name == "counting_sort" and dist_name == "random_wide":
                    print(f"    {algo_name:>18}: пропуск (диапазон ключей)")
                    continue

                t = bench(fn, data)

                print(f"    {algo_name:>18}: t = {t:.6f} c")

                if algo_name not in results[dist_name]:
                    results[dist_name][algo_name] = {
                        "sizes": [],
                        "times": []
                    }

                results[dist_name][algo_name]["sizes"].append(n)
                results[dist_name][algo_name]["times"].append(t)

    # Строим графики по каждому распределению
    for dist_name, algorithms_data in results.items():

        plt.figure(figsize=(10, 6))

        for algo_name, measurements in algorithms_data.items():
            plt.plot(
                measurements["sizes"],
                measurements["times"],
                marker="o",
                label=algo_name
            )

        plt.xscale("log")
        plt.yscale("log")

        plt.xlabel("Размер массива n (log)")
        plt.ylabel("Время выполнения, секунды (log)")
        plt.title(f"Сравнение сортировок — {dist_name}")

        plt.grid(True, which="both", linestyle="--", alpha=0.4)
        plt.legend()
        plt.tight_layout()

        plt.savefig(f"benchmark_{dist_name}.png", dpi=300)
        plt.show()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
