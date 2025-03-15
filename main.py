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
    print(NIST.frequency_test(cpp_sequence))
    print(NIST.frequency_test(java_sequence))

    print(NIST.consecutive_identical_test(cpp_sequence))
    print(NIST.consecutive_identical_test(java_sequence))


if __name__ == "__main__":
    main()