from modules.classes import CSInstance, CSSolution


def check_b4(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the B4 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the B4 constraint is satisfied.
    """
    indexes = solution.indexes()
    edges = instance.edges()

    for edge_idx, (parent, child) in enumerate(edges):
        for ply_idx in range(solution.thickness(child) - 1):
            if (indexes[edge_idx][ply_idx + 1] - indexes[edge_idx][ply_idx]) > 4:
                if verbose:
                    print(
                        "----------------------------------\n"
                        f"Edge {edge_idx} ({parent}-->{child}) ply {ply_idx} B4 constraint violation: \n"
                        f"\tindexes[{edge_idx}][{ply_idx}]={indexes[edge_idx][ply_idx]}, \n"
                        f"\tindexes[{edge_idx}][{ply_idx + 1}]={indexes[edge_idx][ply_idx + 1]}, \n"
                        f"\tdifference={indexes[edge_idx][ply_idx + 1] - indexes[edge_idx][ply_idx]}\n"
                        "----------------------------------\n"
                    )
                return False

    return True
