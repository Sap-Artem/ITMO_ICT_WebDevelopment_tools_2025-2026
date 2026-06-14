# Задача 1. Сравнение threading, multiprocessing и asyncio

## Постановка задачи

Необходимо реализовать три программы на Python, использующие разные подходы к параллельному выполнению задач:

* `threading`;
* `multiprocessing`;
* `asyncio`.

Каждая программа вычисляет сумму чисел в заданном диапазоне. Диапазон разбивается на несколько частей, после чего каждая часть обрабатывается отдельной задачей.

---

## Threading

В варианте с `threading` диапазон разбивается на части, после чего для каждой части создаётся отдельный поток.

```python
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
        end = (i + 1) * chunk_size if i < NUM_THREADS - 1 else TOTAL_NUMBER

        thread = threading.Thread(
            target=calculate_sum,
            args=(start, end, results, i)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
```

Ключевая особенность этого подхода заключается в том, что потоки работают в одном процессе и разделяют общую память. Однако для вычислительных задач ускорение почти не достигается из-за механизма GIL, который не позволяет нескольким потокам одновременно выполнять Python-код.

---

## Multiprocessing

В варианте с `multiprocessing` каждая часть диапазона обрабатывается отдельным процессом. Для распределения задач используется пул процессов.

```python
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
        end = (i + 1) * chunk_size if i < NUM_PROCESSES - 1 else TOTAL_NUMBER
        ranges.append((start, end))

    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)
```

Главное отличие от `threading` состоит в том, что каждый процесс имеет собственный интерпретатор Python и собственный GIL. Благодаря этому вычисления действительно выполняются параллельно на нескольких ядрах процессора.

---

## Asyncio

В варианте с `asyncio` для каждой части диапазона создаётся асинхронная задача. Результаты собираются с помощью `asyncio.gather()`.

```python
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
        end = (i + 1) * chunk_size if i < NUM_TASKS - 1 else TOTAL_NUMBER

        task = asyncio.create_task(
            calculate_sum(start, end)
        )

        tasks.append(task)

    results = await asyncio.gather(*tasks)

    total = sum(results)
```

Корутины выполняются в одном потоке. Так как внутри `calculate_sum()` нет операций `await`, переключение между задачами практически не происходит. Поэтому `asyncio` не даёт преимущества для CPU-bound задач и больше подходит для сетевых запросов, файловых операций и других I/O-bound сценариев.

---

## Результаты тестирования

| Подход          | Время выполнения |
| --------------- | ---------------: |
| Threading       |        31.42 сек |
| Multiprocessing |         4.42 сек |
| Asyncio         |        31.60 сек |

---

## Вывод

Результаты показывают, что для вычислительно сложной задачи наиболее эффективным оказался подход `multiprocessing`. Он позволяет распределить вычисления между несколькими процессами и реально задействовать несколько ядер процессора.

`threading` и `asyncio` показали близкое время выполнения. В случае `threading` это связано с ограничением GIL, а в случае `asyncio` — с тем, что асинхронный подход не предназначен для тяжёлых вычислений без операций ожидания.

Таким образом, для CPU-bound задач лучше использовать `multiprocessing`, а `threading` и `asyncio` целесообразнее применять для задач, связанных с ожиданием ввода-вывода.
