from modules.classes import CSInstance, CSSolution


def check_b2(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the B2 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the B2 constraint is satisfied.
    """
    indexes = solution.indexes()
    edges = instance.edges()

    for edge_idx, (parent, child) in enumerate(edges):
        for ply_idx in range(solution.thickness(child) - 1):
            if indexes[edge_idx][ply_idx] >= indexes[edge_idx][ply_idx + 1]:
                if verbose:
                    print(
                        "----------------------------------\n"
                        f"Edge {edge_idx} ({parent}-->{child}) ply {ply_idx} crossing detected: \n"
                        f"\tindexes[{edge_idx}][{ply_idx}]={indexes[edge_idx][ply_idx]}, \n"
                        f"\tindexes[{edge_idx}][{ply_idx + 1}]={indexes[edge_idx][ply_idx + 1]}\n"
                        "----------------------------------\n"
                    )
                return False

    return True
