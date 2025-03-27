import argparse

import NIST


def create_parser()->tuple:
    parser = argparse.ArgumentParser()
    parser.add_argument("cpp_sequence", type=str, help="path to file with sequence, created in c++")
    parser.add_argument("java_sequence", type=str, help="path to file with sequence, created in java")
    parser.add_argument("result_file", type=str, help="path to file where result will be written")
    args=parser.parse_args()
    return args.cpp_sequence, args.java_sequence, args.result_file


def main():
    try:
        cpp_sequence = NIST.open_file(create_parser()[0])
        java_sequence = NIST.open_file(create_parser()[1])
        result_file = create_parser()[2]

        NIST.write_file("Frequency bitwise test:\n", result_file)
        NIST.write_file(f"cpp: {NIST.frequency_test(cpp_sequence)}\n", result_file)
        NIST.write_file(f"java: {NIST.frequency_test(java_sequence)}\n", result_file)

        NIST.write_file("The consecutive identical bits test:\n", result_file)
        NIST.write_file(f"cpp: {NIST.consecutive_identical_test(cpp_sequence)}\n", result_file)
        NIST.write_file(f"java: {NIST.consecutive_identical_test(java_sequence)}\n", result_file)

        NIST.write_file("The longest sequence of units in block test:\n", result_file)
        NIST.write_file(f"cpp: {NIST.longest_sequence_in_block_test(NIST.block_statistic(cpp_sequence))}\n", result_file)
        NIST.write_file(f"java: {NIST.longest_sequence_in_block_test(NIST.block_statistic(java_sequence))}\n", result_file)

    except Exception as e:
        print(f"An error occurred while accessing the directory: {e} ")


if __name__ == "__main__":
    main()
