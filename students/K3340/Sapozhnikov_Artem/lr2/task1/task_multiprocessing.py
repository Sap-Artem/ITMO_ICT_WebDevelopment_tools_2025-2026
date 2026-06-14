import multiprocessing
import time

TOTAL_NUMBER = 1_000_000_000
NUM_PROCESSES = multiprocessing.cpu_count()


def calculate_sum(start: int, end: int) -> int:
    total = 0

    for i in range(start, end + 1):
        total += i

    return total


def main():
    start_time = time.perf_counter()

    chunk_size = TOTAL_NUMBER // NUM_PROCESSES

    ranges = []

    for i in range(NUM_PROCESSES):
        start = i * chunk_size + 1

        end = (
            (i + 1) * chunk_size
            if i < NUM_PROCESSES - 1
            else TOTAL_NUMBER
        )

        ranges.append((start, end))

    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)

    elapsed = time.perf_counter() - start_time

    print(f"Result: {total}")
    print(f"Time: {elapsed:.2f} sec")


if __name__ == "__main__":
    main()