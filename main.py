import hashlib
import multiprocessing
import itertools
import json
from typing import Generator
import random

import CONST


def generate_possible_numbers(bin: str, last_four: str)-> Generator[str, None,None]:
    middle_length = 6
    for middle in itertools.product('0123456789', repeat=middle_length):
        yield bin + ''.join(middle) + last_four


def check_card_hash(args: tuple[str,str])-> str | None:
    hash, card_number = args
    hashed = hashlib.blake2b(card_number.encode(), digest_size=32).hexdigest()
    return card_number if hash == hashed else None


def get_num_processes()->int:
    return multiprocessing.cpu_count()


def generate_random_card(bin: str, last_four: str)-> str:
    middle = ''.join(random.choices('0123456789', k=6))
    return bin+middle+last_four


def find_card_number(bin: str, last_four: str, hash: str)-> str:
    result = None
    with multiprocessing.Pool(processes=get_num_processes()) as pool:
        tasks = ((hash, num) for num in generate_possible_numbers(bin, last_four)) #создание генератора задач
        for res in pool.imap_unordered(check_card_hash, tasks, chunksize=10000):
            if res:
                result = res
                pool.terminate()
                break

    return result


def get_report(result: str | None, bin: str, hash: str, last_four: str)-> dict[str, str | None | int]:
    report = {
        "status": "success" if result else "fail",
        "card_number": result,
        "bin": bin,
        "hash": hash,
        "last_four_numbers": last_four,
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


def main():
    not_none_count = 0

    for bin in CONST.SBERBANK_VISA_DEBIT_BINS:
        card_number = find_card_number(bin, CONST.LAST_FOUR, CONST.HASH)
        if card_number:
            write_report(get_report(card_number, bin, CONST.HASH, CONST.LAST_FOUR))

            if luhn_check(card_number) == 1:
                print(f"Card number is correct")
            else:
                print(f"Card number isn't correct")

            break
        print(f"BIN: {bin} -> Card: {card_number}")

    if not_none_count == 0:
        random_bin = random.choice(CONST.SBERBANK_VISA_DEBIT_BINS)

        print(
            f"Not a single correct card number was found, "
            f"the Luhn algorithm will be demonstrated with a deliberately incorrect number."
        )

        card_number = generate_random_card(random_bin, CONST.LAST_FOUR)
        write_report(get_report(card_number, random_bin, CONST.HASH, CONST.LAST_FOUR))

        if luhn_check(card_number) == 1:
            print(f"Card number is correct")
        else:
            print(f"Card number isn't correct")


if __name__ == "__main__":
    main()

