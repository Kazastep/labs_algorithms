#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ДЗ 1. Верификация ИИ-сгенерированной сортировки — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-01 (Cases) и методикой верификации по шагам 1–4
(docs/ai-verification.md). Проверяемый код лежит рядом, в dz01-ai-code.py;
исправлять его до завершения верификации запрещено.

Запуск: python dz01-verification-starter.py --variant N
"""
from __future__ import annotations

import argparse
import importlib.util
import random
import statistics
import time
from pathlib import Path
from collections import Counter


# ---------------------------------------------------------------------------
# 0. Загрузка проверяемого кода
# ---------------------------------------------------------------------------
# Имя файла содержит дефисы, поэтому обычный import не подходит —
# модуль загружается по пути через importlib.

# AI_CODE_PATH = Path(__file__).with_name("dz01-ai-code.py")
AI_CODE_PATH = Path(__file__).with_name("dz01-ai-code-fixed.py")


def load_quicksort():
    """Загружает функцию quicksort из соседнего файла dz01-ai-code.py."""
    spec = importlib.util.spec_from_file_location("dz01_ai_code", AI_CODE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.quicksort


quicksort = load_quicksort()

# ---------------------------------------------------------------------------
# 1. Шаг 1 методики: инварианты сортировки
# ---------------------------------------------------------------------------


def is_sorted(a: list[int]) -> bool:
    """Инвариант 1: последовательность упорядочена по неубыванию."""
    # TODO: реализовать проверку соседних пар
    for i in range(1, len(a)):
        if a[i - 1] > a[i]:
            return False
    return True


def same_multiset(a: list[int], b: list[int]) -> bool:
    """Инвариант 2: b — перестановка a (мультимножества элементов совпадают)."""
    # TODO: реализовать через collections.Counter
    return Counter(a) == Counter(b)


def check_invariants(original: list[int], result: list[int]) -> list[str]:
    """Возвращает список нарушенных инвариантов (пустой список — нарушений нет)."""
    # TODO: проверить оба инварианта и вернуть понятные сообщения о нарушениях
    errors =[]
    if not is_sorted(result):
        errors.append("Нарушен порядок")
    if not same_multiset(original, result):
        errors.append("Нарушено мультимножество")
    return errors


# ---------------------------------------------------------------------------
# 2. Шаг 2 методики: репрезентативные тесты
# ---------------------------------------------------------------------------


def representative_cases(rng: random.Random) -> list[tuple[str, list[int]]]:
    """Именованные тестовые входы по классам методики.

    Обязательные классы: граничные (пустой, один, два элемента);
    вырожденные (все элементы равны, уже отсортированный, обратно
    отсортированный); типовые случайные с дубликатами и отрицательными
    числами (генерируются через rng — seed по варианту).
    """
    # TODO: вернуть список пар (название класса, вход)
    cases = [
        # Граничные случаи
        ("Пустой массив", []),
        ("Один элемент", [5]),
        ("Два элемента", [2, 1]),
        ("Два одинаковых элемента", [2, 2]),

        # Вырожденные случаи
        ("Все элементы равны", [5] * 20),
        ("Отсортированный", list(range(20))),
        ("Обратно отсортированный", list(range(19, -1, -1))),

        # Типовые случаи
        ("С дубликатами", [3, 1, 3, 2, 1, 2]),
        ("С отрицательными числами", [-5, 3, -2, 0, -1]),
    ]

    # Случайные массивы с воспроизводимыми значениями
    for n in (10, 50, 100):
        a = [rng.randint(-10, 10) for _ in range(n)]
        cases.append((f"Случайный массив n={n}", a))

    return cases


def run_representative_tests(rng: random.Random) -> None:
    """Прогоняет quicksort по всем классам входов и печатает нарушения инвариантов."""
    # TODO: для каждого входа вызвать quicksort и check_invariants;
    # TODO: зафиксировать, какой класс входов вскрывает какой дефект.
    cases = representative_cases(rng)
    for name, a in cases:
        result = quicksort(a)
        errors = check_invariants(a, result)
    if errors:
        print(f"FAIL: {name}")
        print(f"  Вход: {a}")
        print(f"  Результат: {result}")
        print(f"  Нарушения: {errors}")
    else:
        print(f"OK: {name}")


# ---------------------------------------------------------------------------
# 3. Шаг 3 методики: сравнение с эталоном sorted()
# ---------------------------------------------------------------------------


def compare_with_reference(rng: random.Random, runs: int = 300) -> None:
    """Сверка quicksort с sorted() на сотнях случайных входов.

    Генерируйте входы разных размеров (включая маленькие: именно на них
    удобно локализовать расхождение), обязательно с дубликатами и
    отрицательными числами. Каждое расхождение печатайте вместе со входом,
    чтобы затем свести его к минимальному контрпримеру.
    """
    # TODO: цикл на runs итераций: вход -> quicksort(вход) vs sorted(вход);
    # TODO: подсчитать и напечатать число расхождений и минимальный контрпример.
    mismatches = 0
    min_case = None

    for _ in range(runs):
        n = rng.randint(0, 30)
        a = [rng.randint(-10, 10) for _ in range(n)]

        result = quicksort(a)
        expected = sorted(a)

        if result != expected:
            mismatches += 1
            print(a, result, expected)
            if min_case is None or len(a) < len(min_case):
                min_case = a.copy()

    print(f"Всего тестов: {runs}")
    print(f"Расхождений: {mismatches}")    
    print(f"Минимальный найденный контрпример: {min_case}")

# ---------------------------------------------------------------------------
# 4. Шаг 4 методики: бенчмарк на трёх классах входов
# (методика — docs/reproducibility.md: прогрев, >=5 повторов, медиана)
# ---------------------------------------------------------------------------

SIZES = [500, 1_000, 2_000, 4_000, 8_000]
REPEATS = 5
INPUT_KINDS = ("random", "sorted", "reversed")


def make_input(rng: random.Random, n: int, kind: str) -> list[int]:
    """Вход размера n одного из трёх классов: random / sorted / reversed."""
    a = [rng.randint(-1000, 1000) for _ in range(n)]
    if kind == "sorted":
        a.sort()
    elif kind == "reversed":
        a.sort(reverse=True)
    return a


def bench(fn, data: list[int]) -> float:
    """Медиана времени выполнения fn(data) по REPEATS запускам, с прогревом."""
    fn(data)  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn(data)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры QuickSort и анализ роста времени выполнения."""
    rng = random.Random(seed)

    for kind in INPUT_KINDS:
        print(f"\nКласс входа: {kind}")

        previous_time = None
        previous_n = None

        for n in SIZES:
            data = make_input(rng, n, kind)

            try:
                current_time = bench(quicksort, data)

                print(f"  n={n:>6}  t={current_time:.6f} c", end="")

                if previous_time is not None:
                    ratio = current_time / previous_time
                    print(f"  рост времени: x{ratio:.2f}")
                else:
                    print()

                previous_time = current_time
                previous_n = n

            except RecursionError:
                print(f"  n={n:>6}  RecursionError")
                previous_time = None
                previous_n = None



# ---------------------------------------------------------------------------
# 5. Самопроверка каркаса (граничные случаи + сверка с эталоном stdlib)
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Проверяет вспомогательные функции до основной верификации."""
    assert is_sorted([]) and is_sorted([7]) and is_sorted([1, 2, 2, 3])
    assert not is_sorted([3, 1, 2])
    assert same_multiset([], []) and same_multiset([2, 1, 2], [1, 2, 2])
    assert not same_multiset([1, 1, 2], [1, 2, 2])
    rng = random.Random(0)
    for _ in range(100):  # сверка помощников с эталоном стандартной библиотеки
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        assert is_sorted(sorted(a))          # эталон sorted() упорядочен
        assert same_multiset(a, sorted(a))   # эталон — перестановка входа
    print("self_check: OK")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant  # вариантность — см. docs/reproducibility.md
    random.seed(seed)
    self_check()
    rng = random.Random(seed)
    run_representative_tests(rng)          # шаги 1–2
    compare_with_reference(rng, runs=300)  # шаг 3
    run_benchmarks(seed)                   # шаг 4
    # TODO: по итогам шагов 1–4 сформулировать в отчёте вердикт о применимости
    # TODO: (принять / принять с доработкой / отклонить), исправить дефекты в копии
    # TODO: файла и подтвердить исправление повторной полной верификацией.


if __name__ == "__main__":
    main()
