from .gaussian import gaussian_eliminate

# numerical tolerance
EPS = 1e-10

def rank_and_basis(A):
    """
    Compute matrix rank and return bases.\n

    Returns a tuple ``(rank, row_basis, col_basis, null_basis)`` where
    ``row_basis`` is a list of independent rows, ``col_basis`` is the
    corresponding column basis from the original matrix, and ``null_basis``
    is a basis for the nullspace.
    """
    
    if not A:
        return 0, [], [], []

    nr, nc = len(A), len(A[0])
    U, _, _ = gaussian_eliminate(A)

    row_basis = []
    col_basis_idx = []

    for row in U:
        for j in range(nc):
            if abs(row[j]) > EPS:
                row_basis.append(row[:nc])
                col_basis_idx.append(j)
                break

    rank = len(row_basis)

    # column basis from original matrix
    col_basis = [[A[i][j] for i in range(nr)] for j in col_basis_idx]

    # null space basis: solve Ux = 0 for each free variable
    free_vars = [j for j in range(nc) if j not in col_basis_idx]
    pivot_row = {}
    for i, row in enumerate(U):
        for j in range(nc):
            if abs(row[j]) > EPS:
                pivot_row[j] = i
                break

    null_basis = []
    for fv in free_vars:
        vec = [0.0] * nc
        vec[fv] = 1.0
        # back-substitute: for each pivot column (bottom to top)
        for pcol in reversed(col_basis_idx):
            r = pivot_row[pcol]
            s = sum(U[r][j] * vec[j] for j in range(nc) if j != pcol)
            vec[pcol] = -s / U[r][pcol]
        null_basis.append(vec)

    return rank, row_basis, col_basis, null_basis
