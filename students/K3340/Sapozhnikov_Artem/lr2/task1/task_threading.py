import threading
import time
from multiprocessing import cpu_count

TOTAL_NUMBER = 1_000_000_000
NUM_THREADS = cpu_count()


def calculate_sum(start: int, end: int, results: list[int], index: int) -> None:
    total = 0

    for i in range(start, end + 1):
        total += i

    results[index] = total


def main():
    start_time = time.perf_counter()

    chunk_size = TOTAL_NUMBER // NUM_THREADS

    results = [0] * NUM_THREADS
    threads = []

    for i in range(NUM_THREADS):
        start = i * chunk_size + 1
        end = (
            (i + 1) * chunk_size
            if i < NUM_THREADS - 1
            else TOTAL_NUMBER
        )

        thread = threading.Thread(
            target=calculate_sum,
            args=(start, end, results, i)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)

    elapsed = time.perf_counter() - start_time

    print(f"Result: {total}")
    print(f"Time: {elapsed:.2f} sec")


if __name__ == "__main__":
    main()