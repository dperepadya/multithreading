import multiprocessing
from multiprocessing import Process
from threading import Thread
import time


def get_sum_of_digits(number):
    return sum(int(digit) for digit in str(number))


def check_lucky(start_n, end_n, digits=6):
    counter = 0
    for n in range(start_n, min(end_n, pow(10, digits) - 1) + 1):
        num_str = str(n).zfill(digits)
        left_part_len = digits // 2
        left_part = num_str[:left_part_len]
        right_part = num_str[left_part_len:]
        # print(n, left_part, right_part)
        if get_sum_of_digits(left_part) == get_sum_of_digits(right_part):
            counter += 1
    return counter


def check_lucky_thread(start_n, end_n, digits, result, thread_id):
    print(f'thread {thread_id} started')
    result[thread_id] = check_lucky(start_n, end_n, digits)
    print(f'thread {thread_id} ended')


def check_lucky_process(start_n, end_n, digits, queue, process_id):
    print(f'process {process_id} started')
    queue.put((process_id, check_lucky(start_n, end_n, digits)))
    print(f'process {process_id} ended')


def multithreads_handler(ranges, digits):
    results = {}
    threads = []
    start_time = time.perf_counter()
    for i, (start_num, end_num) in enumerate(ranges):
        thread = Thread(target=check_lucky_thread, args=(start_num, end_num, digits, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    return sum(results.values()), (end_time - start_time) * 1000


def multiprocess_handler(ranges, digits):
    queue = multiprocessing.Queue()
    processes = []

    start_time = time.perf_counter()
    for i, (start_num, end_num) in enumerate(ranges):
        process = Process(target=check_lucky_process, args=(start_num, end_num, digits, queue, i))
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


def split_range(digits, subranges_num):
    max_value = 10 ** digits - 1
    step = (max_value + 1) // subranges_num
    subranges = []

    for i in range(subranges_num):
        start = i * step
        end = (i + 1) * step - 1 if i != subranges_num - 1 else max_value
        subranges.append((start, end))

    return subranges


if __name__ == '__main__':
    length = 8
    ranges_num = 3

    brute_force_ranges = split_range(length, ranges_num)

    print(f'Get the number of lucky tickets with {length} digits')
    print('1. multithreading test')

    lucky_tickets_num, duration_ms = multithreads_handler(brute_force_ranges, length)

    print(f'number of lucky tickets: {lucky_tickets_num}')
    print(f'number of threads: {ranges_num}')
    print(f'computation time: {duration_ms:.2f} ms')

    print('1. multiprocesses test')

    lucky_tickets_num, duration_ms = multiprocess_handler(brute_force_ranges, length)
    print(f'number of lucky tickets: {lucky_tickets_num}')
    print(f'number of processes: {ranges_num}')
    print(f'computation time: {duration_ms:.2f} ms')


