from .gaussian import gaussian_eliminate

def determinant(A):
    """Compute the determinant of a square matrix ``A`` using Gaussian
    elimination. Returns the determinant as a float, or ``None`` for
    non-square input.
    """
    n = len(A)
    # only square matrices have det
    if n == 0 or n != len(A[0]): return None
    
    b = [[] for _ in range(n)]
    
    res, _, num_swaps = gaussian_eliminate([row[:] for row in A], b)

    # If elimination returned None (inconsistent) or fewer than n pivot rows,
    # the matrix is singular and its determinant is 0.
    if res is None:
        return 0.0
    if len(res) < n:
        return 0.0

    det = 1.0
    for i in range(n):
        # ensure diagonal entry exists
        if i >= len(res[i]):
            return 0.0
        det *= res[i][i]

    if num_swaps % 2 == 1:
        det = -det
    return det
