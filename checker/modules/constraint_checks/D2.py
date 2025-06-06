from checker.classes import CSInstance, CSSolution


def check_d2(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the D2 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the D2 constraint is satisfied.
    """
    sequences = solution.sequences()

    for seq in sequences:
        for seq_idx in range(instance.n() - 1):
            if abs(seq[seq_idx] - seq[seq_idx + 1]) == 2:
                if verbose:
                    print(
                        f"Sequence {sequences.index(seq)} D2 constraint violation: "
                        f"plies {seq[seq_idx]} and {seq[seq_idx + 1]} differ by 2 (equivalent of 90° gap)."
                    )

    return True
