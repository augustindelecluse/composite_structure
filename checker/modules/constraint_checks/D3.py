from modules.classes import CSInstance, CSSolution


def check_d3(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the D3 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the D3 constraint is satisfied.
    """
    sequences = solution.sequences()

    for seq in sequences:
        for seq_idx in range(len(seq) - 3):
            if (
                seq[seq_idx] == seq[seq_idx + 1] and
                seq[seq_idx] == seq[seq_idx + 2] and
                seq[seq_idx] == seq[seq_idx + 3]
            ):
                if verbose:
                    print(
                        "----------------------------------\n"
                        f"Sequence {sequences.index(seq)} D3 constraint violation: \n"
                        f"\tfrom ply {seq_idx} and {seq_idx + 3}, \n"
                        f"\t{seq[seq_idx]}, {seq[seq_idx + 1]}, {seq[seq_idx + 2]}, and {seq[seq_idx + 3]} are equal.\n"
                        "----------------------------------\n"
                    )
                return False

    return True
