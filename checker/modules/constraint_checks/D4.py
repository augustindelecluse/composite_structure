from checker.classes import CSInstance, CSSolution
import math


def check_d4(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the D4 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the D4 constraint is satisfied.
    """
    authorized_middle = {
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 4],
        [1, 3],
        [3, 1],
        [1, 2, 1],
        [1, 4, 1],
        [2, 2, 2],
        [2, 4, 2],
        [3, 2, 3],
        [3, 4, 3],
        [4, 2, 4],
        [4, 4, 4],
        [1, 2, 3],
        [1, 4, 3],
        [3, 2, 1],
        [3, 4, 1],
    }

    sequences = solution.sequences()

    for seq in sequences:
        start_middle = math.floor(len(seq) / 2) - 1
        end_middle = math.ceil(len(seq) / 2)

        for ply_idx in range(start_middle):
            if seq[ply_idx] != seq[(len(seq) - 1) - ply_idx]:
                if verbose:
                    print(
                        f"Sequence {sequences.index(seq)} D4 symmetry constraint violation: "
                        f"ply {ply_idx} ({seq[ply_idx]}) does not match "
                        f"ply {len(seq) - 1 - ply_idx} ({seq[len(seq) - 1 - ply_idx]})."
                    )
                return False

        middle = seq[start_middle:end_middle + 1]
        if middle not in authorized_middle:
            if verbose:
                print(
                    f"Sequence {sequences.index(seq)} D4 symmetry constraint violation in the middle part: "
                    f"middle sequence {middle} is not in the authorized set."
                )
            return False

    return True
