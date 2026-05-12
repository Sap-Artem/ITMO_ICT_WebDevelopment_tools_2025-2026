import asyncio
import time


N = 10_000_000_000_000
TASKS_COUNT = 10


def get_ranges(target, tasks_count):
    """
    Разбивает общий диапазон от 1 до target
    на части для асинхронных задач.
    """
    chunk_size = target // tasks_count
    ranges = []

    for i in range(tasks_count):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < tasks_count - 1 else target
        ranges.append((start, end))

    return ranges


async def calculate_sum(start, end):
    """
    Асинхронная задача для вычисления суммы диапазона.
    """
    return (start + end) * (end - start + 1) // 2


async def main():
    start_time = time.time()

    ranges = get_ranges(N, TASKS_COUNT)

    tasks = [
        calculate_sum(start, end)
        for start, end in ranges
    ]

    results = await asyncio.gather(*tasks)

    total_sum = sum(results)
    check_sum = N * (N + 1) // 2

    print("Async result:", total_sum)
    print("Check result:", check_sum)
    print("Correct:", total_sum == check_sum)
    print("Execution time:", time.time() - start_time)


if __name__ == "__main__":
    asyncio.run(main())