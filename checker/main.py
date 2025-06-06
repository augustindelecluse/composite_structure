import argparse
from argparse import RawTextHelpFormatter


def parse_args():
    parser = argparse.ArgumentParser(
        description=
        "DESCRIPTION\n"
        "---------------------------------------\n"
        "Check the validity of solutions of the composite structure problem.\n\n"
        "INSTANCE FILE\n"
        "---------------------------------------\n"
        "The instance file must be in .dzn format and must contain the following elements:\n"
        "  - edges: an array of tuples that represents the edges from the input graph.\n"
        "    The first element of the tuple is the parent (thickest sequence) while the second element is the child.\n"
        "    EXAMPLE: if we have the graph 0 -> 1 -> 2, the edges array will be:\n"
        "    edges = [(0, 1), (1, 2)];\n"
        "  - counts: an array of arrays that represents the number of plies for each angle that must be present in\n"
        "    each stacking sequence.\n"
        "    Every sub-array must have 4 values (one for each angle).\n"
        "    EXAMPLE: the counts array for a structure with two sequences should look like this:\n"
        "    counts = [|1, 2, 3, 4,|2, 3, 1, 0,|];\n\n"
        "SOLUTION FILE\n"
        "---------------------------------------\n"
        "The solution file must be in .dzn format and must follow one of 2 formats:\n"
        "  - The first contains two 2D arrays: seqs and indexes.\n"
        "    The sequences array contains the stacking sequences, while the indexes array contains the indexes of the\n"
        "    plies in the sequences. All the sub arrays (for the sequences AND the indexes) must be of the same\n"
        "    length, which is the length of the thickest stacking sequence.\n"
        "    EXAMPLE: seqs = [|1, 2, 3, 4|2, 3, 1, 0|];\n"
        "             indexes = [|0, 1, 2, 3|0, 1, 2, 3|];\n"
        "  - The second contains a separate 1D array for each stacking sequence and for the indexes of the plies.\n"
        "    The sequences array contains the stacking sequences, while the indexes array contains the indexes of the\n"
        "    plies in the sequences. The arrays are allowed to be of different length.\n"
        "    EXAMPLE: seq0 = [1, 2, 3, 4];\n"
        "             seq1 = [2, 3, 1];\n"
        "             ...\n"
        "             i0 = [0, 1, 2, 3];\n"
        "             i1 = [0, 1, 2, 3];\n"
        "             ...\n",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("instance_file", type=str, help="The instance file of the composite structure.")
    parser.add_argument("solution_file", type=str, help="The solution file to check against the instance.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output.", default=False)
    return parser.parse_args()


def check_equivalence(instance, solution):
    """
    Checks if the instance and solution are equivalent.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    """
    if instance.n() != len(solution.sequences()):
        raise ValueError(
            f"Number of sequences mismatch: instance n = {instance.n()}, "
            f"solution has {len(solution.sequences())} sequences. "
            "The solution must have the same number of sequences as the instance.\n"
            "Please make sure that the solution file matches the instance file."
        )

    for seq_idx in range(instance.n()):
        if solution.thickness(seq_idx) != instance.thickness(seq_idx):
            raise ValueError(
                f"Thickness mismatch for sequence {seq_idx}: "
                f"instance thickness = {instance.thickness(seq_idx)}, "
                f"solution thickness = {solution.thickness(seq_idx)}. "
                "The solution must have the same thickness for each sequence as the instance.\n"
                "Please make sure that the solution file matches the instance file."
            )


def print_report(checks):
    """
    Prints the report of the checks performed on the solution.
    :param checks: dictionary containing the results of the checks.
    """
    OK_GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    print("\nReport of checks:")
    print("-----------------")
    for check_name, result in checks.items():
        if result:
            print(f"{check_name}: {OK_GREEN}PASSED{ENDC}")
        else:
            print(f"{check_name}: {FAIL}FAILED{ENDC}")
    print("-----------------")


def main():
    args = parse_args()
    instance = CSInstance(args.instance_file)
    solution = CSSolution(args.solution_file)
    check_equivalence(instance, solution)

    checks = {
        "B1": B1.check_b1(instance, solution, args.verbose),
        "B2": B2.check_b2(instance, solution, args.verbose),
        "B3": B3.check_b3(instance, solution, args.verbose),
        "B4": B4.check_b4(instance, solution, args.verbose),
        "D1": D1.check_d1(instance, solution, args.verbose),
        "D2": D2.check_d2(instance, solution, args.verbose),
        "D3": D3.check_d3(instance, solution, args.verbose),
        "D4": D4.check_d4(instance, solution, args.verbose),
        "D5": D5.check_d5(instance, solution, args.verbose),
    }

    print_report(checks)


if __name__ == '__main__':
    from modules.classes.CSInstance import CSInstance
    from modules.classes.CSSolution import CSSolution
    from modules.constraint_checks import (
        B1, B3, B4, D1, D2, D4
    )
    from modules.constraint_checks import D5, D3, B2
    main()
