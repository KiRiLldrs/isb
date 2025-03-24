import math

import scipy.special as sp


def open_file(filename: str)->str:
    """
    Opens the file with the random sequence
    :param filename: directory of the file
    :return: sequence as str
    """
    with open (filename, "r") as file:
        sequence = file.read()
    return sequence


def frequency_test(sequence: str):
    """
    NIST frequency bitwise test
    :param sequence: random sequence
    :return: P-value
    """
    length = len(sequence)
    one = sequence.count("1")
    zero = sequence.count("0")

    Sn = (abs(one-zero))/(length**0.5)
    probability = math.erfc(Sn/(2**0.5))

    return probability


def consecutive_identical_test(sequence: str):
    """
    NIST test for identical consecutive bits.
    :param sequence: random sequence
    :return: P-value
    """
    length = len(sequence)
    ones_percentage  = sequence.count("1")/length
    if abs(ones_percentage - 1/2) < 2/(length**0.5):
        Vn = 0
        for i in range(length-1):
            if sequence[i]!=sequence[i+1]:
                Vn += 1

        numerator = abs(Vn - 2*length*ones_percentage*(1-ones_percentage))
        denominator = 2*(2*length)**0.5 * ones_percentage*(1-ones_percentage)
        return math.erfc(numerator/denominator)
    else:
        return 0


def max_consecutive_ones(block)->int:
    """
    Calculates the maximum sequence of identical bits in block
    :param block: the block of 8 bits
    :return: length of maximum sequence
    """
    max_len = 0
    current_len = 0
    for bit in block:
        if bit == "1":
            current_len+=1
            max_len = max(max_len, current_len)
        else:
            current_len = 0
    return max_len


def block_statistic(sequence)->tuple:
    """
    Calculates statistic of identical bits in each block
    :param sequence: random sequence
    :return: statistic as tuple
    """
    blocks = [sequence[i:i+8] for i in range(0, len(sequence), 8)]
    V1, V2, V3, V4 = 0, 0, 0, 0

    for block in blocks:
        max_len = max_consecutive_ones(block)
        if max_len <= 1:
            V1 += 1
        elif max_len == 2:
            V2 += 1
        elif max_len == 3:
            V3 +=1
        else:
            V4 += 1

    return V1, V2, V3, V4


def longest_sequence_in_block_test(results: tuple)->int:
    """
    NIST test for the longest sequence of units in a block.
    :param results: statistic as tuple
    :return: P-value
    """
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_square = 0

    for i in range(0,4):
        chi_square += ((results[i] - 16*pi[i])**2) / (16*pi[i])

    return sp.gammainc(3/2, chi_square/2)
