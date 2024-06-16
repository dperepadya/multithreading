import multiprocessing
from multiprocessing import Process
from threading import Thread
import time


def get_sum_of_digits(number):
    return sum(int(digit) for digit in str(number))


def check_lucky(start_n, end_n):
    counter = 0
    for n in range(start_n, min(end_n, pow(10, 6) - 1) + 1):
        num_str = str(n).zfill(6)
        left_part = num_str[:3]
        right_part = num_str[3:]
        # print(n, left_part, right_part)
        if get_sum_of_digits(left_part) == get_sum_of_digits(right_part):
            counter += 1
    return counter


def check_lucky_thread(start_n, end_n, result, thread_id):
    print(f'tread {thread_id} started')
    result[thread_id] = check_lucky(start_n, end_n)
    print(f'tread {thread_id} ended')


def check_lucky_process(start_n, end_n, queue, process_id):
    print(f'tread {process_id} started')
    queue.put((process_id, check_lucky(start_n, end_n)))
    print(f'tread {process_id} ended')


def multithreads_handler(ranges):
    results = {}
    threads = []
    start_time = time.perf_counter()
    for i, (start_num, end_num) in enumerate(ranges):
        thread = Thread(target=check_lucky_thread, args=(start_num, end_num, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    return sum(results.values()), (end_time - start_time) * 1000


def multiprocess_handler(ranges):
    queue = multiprocessing.Queue()
    processes = []

    start_time = time.perf_counter()
    for i, (start_num, end_num) in enumerate(ranges):
        process = Process(target=check_lucky_process, args=(start_num, end_num, queue, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {}
    while not queue.empty():
        process_id, counter = queue.get()
        results[process_id] = counter

    end_time = time.perf_counter()

    return sum(results.values()), (end_time - start_time) * 1000


if __name__ == '__main__':
    # brute_force_ranges = [(0, 999999)]
    # brute_force_ranges = [(0, 500000), (500001, 999999)]
    brute_force_ranges = [(0, 333333), (333334, 666667), (666668, 999999)]

    print('Get the number of lucky tickets')
    print('1. multithreading test')

    lucky_tickets_num, duration_ms = multithreads_handler(brute_force_ranges)

    print(f'number of lucky tickets: {lucky_tickets_num}')
    print(f'number of threads: {len(brute_force_ranges)}')
    print(f'computation time: {duration_ms:.2f} ms')

    print('1. multiprocesses test')

    lucky_tickets_num, duration_ms = multiprocess_handler(brute_force_ranges)
    print(f'number of lucky tickets: {lucky_tickets_num}')
    print(f'number of threads: {len(brute_force_ranges)}')
    print(f'computation time: {duration_ms:.2f} ms')


