from modules.classes import CSInstance, CSSolution


def check_d5(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the D5 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the D5 constraint is satisfied.
    """
    sequences = solution.sequences()

    for seq in sequences:
        if seq[0] not in {1, 3}:
            if verbose:
                print(
                    "----------------------------------\n"
                    f"Sequence {sequences.index(seq)} D5 constraint violation: \n"
                    f"\tfirst ply {seq[0]} is not 1 (-45°) or 3 (45°).\n"
                    "----------------------------------\n"
                )
            return False

        if seq[-1] not in {1, 3}:
            if verbose:
                print(
                    "----------------------------------\n"
                    f"Sequence {sequences.index(seq)} D5 constraint violation: \n"
                    f"\tlast ply {seq[-1]} is not 1 (-45°) or 3 (45°).\n"
                    "----------------------------------\n"
                )
            return False

    return True
