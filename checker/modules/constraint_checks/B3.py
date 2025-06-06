from checker.classes import CSInstance, CSSolution


def check_b3(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the B3 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the B3 constraint is satisfied.
    """
    indexes = solution.indexes()
    edges = instance.edges()

    for edge_idx, (parent, child) in enumerate(edges):
        continuous_top_ply = indexes[edge_idx][0] == indexes[edge_idx + 1][0]
        last_ply = solution.thickness(child) - 1
        continuous_bottom_ply = indexes[edge_idx][last_ply] == indexes[edge_idx + 1][last_ply]

        if not (continuous_top_ply and continuous_bottom_ply):
            if verbose:
                print(
                    f"Edge {edge_idx} ({parent}-->{child}) does not satisfy B3 constraint: "
                    f"indexes[{edge_idx}][0]={indexes[edge_idx][0]}, "
                    f"indexes[{edge_idx + 1}][0]={indexes[edge_idx + 1][0]}, "
                    f"indexes[{edge_idx}][{last_ply}]={indexes[edge_idx][last_ply]}, "
                    f"indexes[{edge_idx + 1}][{last_ply}]={indexes[edge_idx + 1][last_ply]}"
                )
            return False

    return True