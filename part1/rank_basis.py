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
    
    for r in range(min(nr, nc)):
        if abs(res[r][r]) > 1e-9:
            rank += 1
            row_basis.append(res[r][:nc])
            col_basis_idx.append(r)
            
    col_basis = [[A[row][i] for row in range(nr)] for i in col_basis_idx]

    return rank, row_basis, col_basis
