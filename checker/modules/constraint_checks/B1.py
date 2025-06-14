from modules.classes import CSInstance, CSSolution


def check_b1(instance: CSInstance, solution: CSSolution, verbose: bool) -> bool:
    """
    Checks if the B1 constraint is satisfied in the given solution.
    :param instance: instance of CSInstance containing the problem data.
    :param solution: solution of CSSolution containing the sequences and indexes.
    :param verbose: boolean flag to print detailed mismatch information.
    :return: boolean indicating whether the B1 constraint is satisfied.
    """
    sequences = solution.sequences()
    indexes = solution.indexes()
    edges = instance.edges()

    for edge_idx, (parent, child) in enumerate(edges):
        for ply_idx, ply in enumerate(sequences[child]):
            if ply != sequences[parent][indexes[edge_idx][ply_idx]]:
                if verbose:
                    print(
                        "----------------------------------\n"
                        f"Edge {edge_idx} ({parent}-->{child}) ply {ply_idx} blending error: \n"
                        f"\tindexes[{edge_idx}][{ply_idx}]={indexes[edge_idx][ply_idx]}, \n"
                        f"\tparent[{indexes[edge_idx][ply_idx]}]={sequences[parent][indexes[edge_idx][ply_idx]]}, \n"
                        f"\tchild[{ply_idx}]={ply}\n"
                        "----------------------------------\n"
                    )
                return False

    return True
