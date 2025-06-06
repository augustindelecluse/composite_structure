from checker.classes import CSInstance, CSSolution


def check_d1(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the D1 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the D1 constraint is satisfied.
    """
    sequences = solution.sequences()
    actual_counts = [[0, 0, 0, 0] for _ in range(len(sequences))]
    expected_counts = solution.counts()

    for seq_idx, seq in enumerate(sequences):
        for ply in seq:
            if 1 <= ply <= 4:
                actual_counts[seq_idx][ply - 1] += 1
            else:
                ValueError(f"Invalid ply value {ply} in sequence {seq_idx}. Expected values are between 1 and 4.")

        for actual_count, expected_count in zip(actual_counts[seq_idx], expected_counts[seq_idx]):
            if actual_count != expected_count:
                if verbose:
                    print(
                        f"Sequence {seq_idx} ply count mismatch (D1 constraint violation): "
                        f"actual={actual_counts[seq_idx]}, expected={expected_counts[seq_idx]}"
                    )
                return False

    return True
