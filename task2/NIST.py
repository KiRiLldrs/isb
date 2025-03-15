import math

def open_file(filename: str)->str:
    with open (filename, "r") as file:
        sequence = file.read()
    return sequence


def frequency_test(sequence: str):
    length = len(sequence)
    one = sequence.count("1")
    zero = sequence.count("0")

    Sn = (abs(one-zero))/(length**0.5)
    probability = math.erfc(Sn/(2**0.5))

    return probability

def consecutive_identical_test(sequence: str):
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

