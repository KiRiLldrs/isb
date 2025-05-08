import hashlib
import multiprocessing
import itertools
import json
from typing import Generator
import time

import matplotlib.pyplot as plt

import CONST


def generate_possible_numbers(bin: str, last_four: str)-> Generator[str, None,None]:
    middle_length = 6
    for middle in itertools.product('0123456789', repeat=middle_length):
        yield bin + ''.join(middle) + last_four


def check_card_hash(args: tuple[str,str])-> str | None:
    hash, card_number = args
    hashed = hashlib.blake2b(card_number.encode(), digest_size=64).hexdigest()
    return card_number if hash == hashed else None


def get_num_processes()->int:
    return multiprocessing.cpu_count()


def find_card_number(bin: str, last_four: str, hash: str, num_processes=get_num_processes())-> str | None:
    result = None
    with multiprocessing.Pool(processes=num_processes) as pool:
        tasks = ((hash, num) for num in generate_possible_numbers(bin, last_four)) #создание генератора задач
        for res in pool.imap_unordered(check_card_hash, tasks):
            if res:
                result = res
                pool.terminate()
                break

    return result


def get_graph(time_data: list)->None:
    processes = list(range(1,int(get_num_processes()*1.5) + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(processes, time_data)

    plt.title("Time dependence on the number of processes")
    plt.xlabel("Number of processes")
    plt.ylabel("Time (seconds)")

    plt.xticks(processes)
    plt.grid(True)

    min_time = min(time_data)
    min_processes = time_data.index(min_time) + 1
    plt.scatter(min_processes, min_time, color="red", label="Point of global minimum")
    plt.show()


def get_report(result: str | None, bin: str, hash: str, last_four: str)-> dict[str, str | None | int]:
    report = {
        "status": "success" if result else "fail",
        "card_number": result,
        "bin": bin,
        "last_four_numbers": last_four,
        "hash": hash,
        "processes_used": get_num_processes()
    }
    return report

def write_report(report: dict[str, str | None | int])-> None:
    with open(CONST.JSON_RES, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def luhn_check(card_number: str)->bool:
    print(f"card number: {card_number}")

    numbers = [int(d) for d in reversed(card_number)]
    print(f"reveres: {numbers}")

    for i in range(1, len(card_number), 2):
        doubled = numbers[i] * 2
        numbers[i] = doubled - 9 if doubled > 9 else doubled
    print(f"Doubling digits in odd positions: {numbers}")
    print(f"Sum: {sum(numbers)}")
    print(f"Remainder of the division by 10: {sum(numbers) % 10}")
    return sum(numbers) % 10 == 0


def get_json_data():
    with open(CONST.JSON_RES, 'r') as file:
        data = json.load(file)
    return data

def clear_report():
    with open(CONST.JSON_RES, 'w') as file:
        json.dump({}, file)
