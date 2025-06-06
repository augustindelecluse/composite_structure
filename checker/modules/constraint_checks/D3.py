from checker.classes import CSInstance, CSSolution


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
        for seq_idx in range(instance.n() - 3):
            if (
                seq[seq_idx] == seq[seq_idx + 1] and
                seq[seq_idx] == seq[seq_idx + 2] and
                seq[seq_idx] == seq[seq_idx + 3] and
                seq[seq_idx] == seq[seq_idx + 4]
            ):
                if verbose:
                    print(
                        f"Sequence {sequences.index(seq)} D3 constraint violation: "
                        f"from ply {seq_idx} and {seq_idx + 3}, "
                        f"{seq[seq_idx]}, {seq[seq_idx + 1]}, {seq[seq_idx + 2]}, and {seq[seq_idx + 3]} are equal."
                    )
                return False

    return True
