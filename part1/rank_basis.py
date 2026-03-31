from gaussian import gaussian_eliminate

def rank_and_basis(A):
    if not A: return 0, [], []
    nr = len(A)
    nc = len(A[0])
    b = [[] for _ in range(nr)]
    res, _, _ = gaussian_eliminate(A, b)
    
    rank = 0
    row_basis = []
    col_basis_idx = []
    
    # Check pivot columns in the result matrix
    for r in range(len(res)):  # Use actual number of rows in res after filtering
        for c in range(min(len(res[r]), nc)):
            if abs(res[r][c]) > 1e-9:  # Found pivot in this row
                rank = r + 1
                row_basis.append(res[r][:nc])
                col_basis_idx.append(c)
                break
            
    # Extract column basis from original matrix
    col_basis = [[A[row][i] for row in range(nr)] for i in col_basis_idx]

    return rank, row_basis, col_basis
