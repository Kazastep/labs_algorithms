#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python3 lab03-simple-sorts-quicksort-starter.py --variant 10
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list, key=lambda x: x) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: O(n^2).

    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    # TODO: реализовать; считать сравнения и обмены
    arr_len = len(a)
    arr_copy = list(a)
    comparisons = 0
    exchange = 0
    for bypass in range(1,arr_len):
        swapped = False
        for k in range(0, arr_len - bypass):
            comparisons += 1
            if key(arr_copy[k]) > key(arr_copy[k+1]):
                arr_copy[k], arr_copy[k+1] = arr_copy[k+1], arr_copy[k]
                exchange += 1
                swapped = True
        if not swapped:
            return arr_copy, comparisons, exchange
    return arr_copy, comparisons, exchange


def insertion_sort(a: list, key=lambda x: x) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO O(n) O(n^2)."""
    # TODO: реализовать; считать сравнения и перемещения (сдвиги)
    arr_len = len(a)
    arr_copy = list(a)
    comparisons = 0
    exchange = 0
    for top in range(1, arr_len):
        k = top
        while k > 0:
            comparisons += 1
            if key(arr_copy[k]) < key(arr_copy[k-1]):
                arr_copy[k], arr_copy[k-1] = arr_copy[k-1], arr_copy[k]
                exchange += 1
                k -= 1
            else:
                break
    return arr_copy, comparisons, exchange



def selection_sort(a: list, key= lambda x: x) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO O(n^2)(почему не зависит от входа?)."""
    # TODO: реализовать; считать сравнения и обмены
    arr_len = len(a)
    arr_copy = list(a)
    comparisons = 0
    exchange = 0
    
    for pos in range(0,arr_len - 1):
        min_index = pos
        for k in range(pos+1,arr_len):
            comparisons += 1
            if key(arr_copy[k]) < key(arr_copy[min_index]):
                min_index = k
        if min_index != pos:
            arr_copy[pos], arr_copy[min_index] = arr_copy[min_index], arr_copy[pos]
            exchange += 1
    
    return arr_copy, comparisons, exchange


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None, key= lambda x: x) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность: в среднем O(n log n), в худшем случае O(n^2) (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    if rng is None:
        rng = random.Random()
    # TODO: реализовать (рекурсивно или циклом со стеком);
    # TODO: опорный элемент — a[rng.randrange(lo, hi)], не первый и не последний.
    if a is None:
        raise ValueError ("Список не получен")

    if len(a) < 2:
        return a

    if len(a) == 2:
        if key(a[0]) <= key(a[1]):
            return a
        return [a[1], a[0]]

    if len(a) <= 3:
        target = a[1]

    else:
        target = a[rng.randrange(1, len(a) - 1)]

    less = [n for n in a if key(n) < key(target)]
    equal = [n for n in a if key(n) == key(target)]
    great = [n for n in a if key(n) > key(target)]

    return quick_sort(less, rng, key= key) + equal + quick_sort(great,rng, key= key)



# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """
    # TODO: подготовить пары, прогнать все четыре сортировки, напечатать итог
    pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    bubble_result, _, _ = bubble_sort(
        pairs,
        key=lambda p: p[0]
    )

    insertion_result, _, _ = insertion_sort(
        pairs,
        key=lambda p: p[0]
    )

    selection_result, _, _ = selection_sort(
        pairs,
        key=lambda p: p[0]
    )

    rng = random.Random(40)

    quick_result = quick_sort(
        pairs,
        rng=rng,
        key=lambda p: p[0]
    )

    print("Исходный:", pairs)
    print("Bubble:", bubble_result)
    print("Insertion:", insertion_result)
    print("Selection:", selection_result)
    print("Quick:", quick_result)
    


# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]

    for name, fn, sizes in plans:

        results = {
            "упорядоченный": [],
            "случайный": [],
            "обратный": [],
        }

        print(f"\n{name}:")

        for n in sizes:
            for cls, data in make_inputs(n, seed).items():

                time_result = bench(fn, data)

                print(
                    f"  n={n:>7}  вход={cls:<13} "
                    f"t={time_result:.6f} c"
                )

                results[cls].append((n, time_result))

        for cls, values in results.items():
            x = [point[0] for point in values]
            y = [point[1] for point in values]

            plt.loglog(x, y, marker="o", label=cls)

        plt.xlabel("Размер входа n")
        plt.ylabel("Время, с")
        plt.title(name)
        plt.legend()
        plt.grid(True)
        plt.show()
    # TODO: построить log-log графики (matplotlib) по классам входов;
    # TODO: сопоставить наклоны с O(n^2) и O(n log n), объяснить расхождения
    #       (в т. ч. лучший случай вставок и поведение пузырька на упорядоченном входе);
    # TODO: включить в отчёт таблицы счётчиков сравнений/обменов.


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
