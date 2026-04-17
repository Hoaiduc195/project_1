import numpy as np
from back_substitution import Expression, back_substitution
from utils import swap_row, mul_row, add_row, build_augmented_matrix

EPS = 1e-10

def gaussian_eliminate(A, b=None):
    """
    Perform Gaussian elimination on matrix ``A`` with optional right-
    hand side ``b``.\n
    Returns a tuple ``(U, x, num_swaps)`` where ``U`` is
    the filtered upper-triangular matrix, ``x`` contains solved
    `Expression` objects (or empty), and ``num_swaps`` is the count of row
    swaps performed.\n
    If the system is inconsistent returns ``(None, None,
    swaps)``.
    """
    
    if not A: 
        # return matrix of Expression if A is empty
        return [], [[Expression()]], 0
    
    nr = len(A)
    nc = len(A[0])
    
    # convert b from 1D to 2D if needed
    if b is None:
        b = [[] for _ in range(nr)]
    elif b and isinstance(b[0], (int, float)):
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
        while max_idx < nr and abs(aug[max_idx][k]) < EPS:
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
            if abs(aug[pivot_row][k]) > EPS:
                q = float(aug[u][k]) / aug[pivot_row][k]
                add_row(aug, -q, pivot_row, u)
        pivot_row += 1
    
    # check for inconsistency and collect non-zero rows
    filtered_aug = []
    for row in aug:
        coeff_part = row[:a_cols]
        rhs_part = row[a_cols:]
        
        if all(abs(v) < EPS for v in coeff_part):
            if any(abs(v) > EPS for v in rhs_part):
                return None, None, num_swaps  # inconsistent
            continue
        filtered_aug.append(row)
    
    # extract upper triangle matrix and c from filtered augmented matrix
    U = [row[:a_cols] for row in filtered_aug]
    c_part = [row[a_cols:] for row in filtered_aug]
    
    x = back_substitution(U, c_part) if (c_part and len(c_part[0]) > 0) else []
    
    return U, x, num_swaps