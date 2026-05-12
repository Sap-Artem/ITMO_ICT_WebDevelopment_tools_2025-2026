import threading
import time


N = 10_000_000_000_000
THREADS_COUNT = 100


def get_ranges(target, threads_count):
    """
    Разбиваем диапазон от 1 до target на несколько частей.
    Каждая часть будет обрабатываться отдельным потоком.
    """
    chunk_size = target // threads_count
    ranges = []

    for i in range(threads_count):
        start = i * chunk_size + 1

        if i == threads_count - 1:
            end = target
        else:
            end = (i + 1) * chunk_size

        ranges.append((start, end))

    return ranges


def calculate_sum(start, end, results, index):
    """
    Считает сумму чисел на участке от start до end.
    """
    results[index] = (start + end) * (end - start + 1) // 2


if __name__ == "__main__":
    start_time = time.time()

    ranges = get_ranges(N, THREADS_COUNT)
    results = [0] * THREADS_COUNT
    threads = []

    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(
            target=calculate_sum,
            args=(start, end, results, index)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    check_sum = N * (N + 1) // 2

    print("Threading result:", total_sum)
    print("Check result:", check_sum)
    print("Correct:", total_sum == check_sum)
    print("Execution time:", time.time() - start_time)