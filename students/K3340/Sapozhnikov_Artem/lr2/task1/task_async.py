import asyncio
import time
from multiprocessing import cpu_count

TOTAL_NUMBER = 1_000_000_000
NUM_TASKS = cpu_count()


async def calculate_sum(start: int, end: int) -> int:
    total = 0

    for i in range(start, end + 1):
        total += i

    return total


async def main():
    start_time = time.perf_counter()

    chunk_size = TOTAL_NUMBER // NUM_TASKS

    tasks = []

    for i in range(NUM_TASKS):
        start = i * chunk_size + 1

        end = (
            (i + 1) * chunk_size
            if i < NUM_TASKS - 1
            else TOTAL_NUMBER
        )

        tasks.append(
            asyncio.create_task(
                calculate_sum(start, end)
            )
        )

    results = await asyncio.gather(*tasks)

    total = sum(results)

    elapsed = time.perf_counter() - start_time

    print(f"Result: {total}")
    print(f"Time: {elapsed:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())