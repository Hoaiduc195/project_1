import numpy as np
from back_substitution import Expression, back_substitution


# Helper functions for gaussian_eliminate()
###
def swap_row(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]

def mul_row(A, i, c):
    for k in range(len(A[i])):
        A[i][k] *= c

def add_row(A, c, j, i):
    for k in range(len(A[i])):
        A[i][k] += A[j][k] * c

def build_augmented_matrix(A, b):
    aug = [row[:] for row in A]
    for i in range(len(A)):
        aug[i].extend(b[i][:])
    return aug
###

def gaussian_eliminate(A, b=None):
    if not A: 
        # return matrix of Expression if A is empty
        return [], [[Expression()]], 0
    
    nr = len(A)
    nc = len(A[0])
    
    # Handle b parameter: convert 1D to 2D if needed
    if b is None:
        b = [[] for _ in range(nr)]
    elif b and isinstance(b[0], (int, float)):
        # b is 1D array like [0, 0, 0], convert to [[0], [0], [0]]
        b = [[val] for val in b]
    elif not b or len(b[0]) == 0:
        b = [[] for _ in range(nr)]
        
    aug = build_augmented_matrix(A, b)
    a_cols = nc
    num_swaps = 0
    
    pivot_row = 0
    for k in range(a_cols):
        if pivot_row >= nr:
            break
        # find largest pivot in column k
        max_idx = pivot_row
        while max_idx < nr and aug[max_idx][k] == 0:
            max_idx += 1

        if max_idx == nr:
            continue  # no pivot in this column, move to next column (same row)

        for u in range(max_idx, nr):
            if abs(aug[u][k]) > abs(aug[max_idx][k]):
                max_idx = u
        if pivot_row != max_idx:
            swap_row(aug, pivot_row, max_idx)
            num_swaps += 1
        # eliminate all rows below pivot_row
        for u in range(pivot_row + 1, nr):
            if aug[pivot_row][k] != 0:
                q = float(aug[u][k]) / aug[pivot_row][k]
                add_row(aug, -q, pivot_row, u)
        pivot_row += 1
    
    # check for inconsistency and collect non-zero rows
    filtered_aug = []
    for row in aug:
        coeff_part = row[:a_cols]
        rhs_part = row[a_cols:]
        
        if all(abs(v) < 1e-10 for v in coeff_part):
            if any(abs(v) > 1e-10 for v in rhs_part):
                return None, None, num_swaps  # inconsistent
            continue
        filtered_aug.append(row)
    
    # extract upper triangle matrix and c from filtered augmented matrix
    U = [row[:a_cols] for row in filtered_aug]
    c_part = [row[a_cols:] for row in filtered_aug]
    
    x = back_substitution(U, c_part) if (c_part and len(c_part[0]) > 0) else []
    
    return U, x, num_swaps




def _to_float(v):
    if isinstance(v, Expression):
        if any(k != Expression.BIAS for k in v.mp):
            raise ValueError("Symbolic expression")
        return float(v.mp.get(Expression.BIAS, 0.0))
    return float(v)

def _to_np(mat):
    if mat is None: raise ValueError
    if isinstance(mat, np.ndarray): return mat.astype(float)
    if not mat: return np.empty((0, 0), dtype=float)
    if isinstance(mat[0], (list, tuple)):
        return np.array([[_to_float(v) for v in row] for row in mat], dtype=float)
    return np.array([_to_float(v) for v in mat], dtype=float)

def verify_solution(A, x, b):
    """Verify determinant, inverse, rank, and gaussian_eliminate against NumPy."""
    from determinant import determinant
    from inverse import inverse
    from rank_basis import rank_and_basis

    A_np = _to_np(A)
    n, m = A_np.shape
    results = {}

    # Check determinant & inverse (square only)
    if n == m:
        try:
            results["det_ok"] = np.isclose(determinant(A), np.linalg.det(A_np), atol=1e-8, rtol=1e-6)
        except: results["det_ok"] = False
        try:
            inv = inverse(A)
            results["inv_ok"] = (np.linalg.matrix_rank(A_np) < n) if inv is None else np.allclose(_to_np(inv), np.linalg.inv(A_np), atol=1e-8)
        except: results["inv_ok"] = False

    # Check rank
    try:
        r, _, _, _ = rank_and_basis(A)
        results["rank_ok"] = (r == np.linalg.matrix_rank(A_np))
    except: results["rank_ok"] = False

    # Check gaussian_eliminate
    try:
        _, x_calc, _ = gaussian_eliminate(A, b)
        x_np = _to_np(x_calc).reshape(-1, 1) if _to_np(x_calc).ndim == 1 else _to_np(x_calc)
        b_np = _to_np(b).reshape(-1, 1) if _to_np(b).ndim == 1 else _to_np(b)
        results["gauss_ok"] = np.allclose(A_np @ x_np, b_np, atol=1e-8)
    except: results["gauss_ok"] = None

    return results


def print_matrix(mat):
    for row in mat:
        print(["{:.4f}".format(v) for v in row])


def gaussian_eliminate_formatter(U, x, num_swaps):
    """
    Formats the gaussian_eliminate() result
    """
    
    # print upper triangle matrix
    print("\nUpper Triangle Matrix U:")
    print("-" * 40)
    if U:
        for i, row in enumerate(U):
            row_str = "["
            for j, val in enumerate(row):
                if isinstance(val, float):
                    row_str += f"{val:10.4f}"
                else:
                    row_str += f"{str(val):>10}"
                if j < len(row) - 1:
                    row_str += ", "
            row_str += "]"
            print(row_str)
    else:
        print("Empty matrix")
    
    # print solution vector
    print("\nSolution Vector x:")
    print("-" * 40)
    if x:
        for i, val in enumerate(x):
            print(f"x[{i}] = {val}")
    else:
        print("No solution")
    
    # print number of swaps
    print(f"\nNumber of Row Swaps: {num_swaps}")

def main():
    A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    U, x, num_swaps = gaussian_eliminate(A, [0, 0, 0])
    gaussian_eliminate_formatter(U, x, num_swaps)
    
if __name__ == "__main__":
    main()
