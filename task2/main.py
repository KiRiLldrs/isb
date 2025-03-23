import argparse

import NIST

def create_parser()->tuple:
    parser = argparse.ArgumentParser()
    parser.add_argument("cpp_sequence", type=str, help="path to file with sequence, created in c++")
    parser.add_argument("java_sequence", type=str, help="path to file with sequence, created in java")
    args=parser.parse_args()
    return args.cpp_sequence, args.java_sequence


def main():
    cpp_sequence = NIST.open_file(create_parser()[0])
    java_sequence = NIST.open_file(create_parser()[1])

    print("Frequency bitwise test:")
    print("cpp: ", NIST.frequency_test(cpp_sequence))
    print("java: ", NIST.frequency_test(java_sequence))

    print("The consecutive identical bits test:")
    print("cpp: ", NIST.consecutive_identical_test(cpp_sequence))
    print("java: ", NIST.consecutive_identical_test(java_sequence))

    print("The longest sequence of units in block test:")
    print("cpp: ", NIST.longest_sequence_in_block_test(NIST.block_statistic(cpp_sequence)))
    print("java: ", NIST.longest_sequence_in_block_test(NIST.block_statistic(java_sequence)))


if __name__ == "__main__":
    main()
