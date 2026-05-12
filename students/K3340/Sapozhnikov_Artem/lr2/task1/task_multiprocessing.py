import multiprocessing
import time


N = 10_000_000_000_000
PROCESSES_COUNT = 10


def get_ranges(target, processes_count):
    """
    Разбивает общий диапазон от 1 до target
    на части для отдельных процессов.
    """
    chunk_size = target // processes_count
    ranges = []

    for i in range(processes_count):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < processes_count - 1 else target
        ranges.append((start, end))

    return ranges


def calculate_sum(start, end):
    """
    Считает сумму чисел в диапазоне от start до end.
    """
    return (start + end) * (end - start + 1) // 2


if __name__ == "__main__":
    start_time = time.time()

    ranges = get_ranges(N, PROCESSES_COUNT)

    with multiprocessing.Pool(PROCESSES_COUNT) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total_sum = sum(results)
    check_sum = N * (N + 1) // 2

    print("Multiprocessing result:", total_sum)
    print("Check result:", check_sum)
    print("Correct:", total_sum == check_sum)
    print("Execution time:", time.time() - start_time)