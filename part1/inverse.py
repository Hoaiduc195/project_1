from gaussian import build_augmented_matrix, swap_row, add_row, mul_row

EPS = 1e-10

def inverse(A):
    """
    Compute the inverse of a square matrix A using Gauss-Jordan elimination.
    Returns None if the matrix is singular.
    """
    n = len(A)
    
    # check if matrix is square
    if n == 0 or any(len(row) != n for row in A):
        return None

    # create augmented matrix
    aug = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(n)]
           for i, row in enumerate(A)]

    for k in range(n):
        max_row = max(range(k, n), key=lambda i: abs(aug[i][k]))        
        
        # check if matrix is singular
        if abs(aug[max_row][k]) < EPS:
            return None
        
        # swap rows if needed
        if max_row != k:
            aug[k], aug[max_row] = aug[max_row], aug[k]

        pivot = aug[k][k]
        aug[k] = [x / pivot for x in aug[k]]

        for i in range(n):
            if i != k:
                factor = aug[i][k]
                aug[i] = [aug[i][j] - factor * aug[k][j] for j in range(2 * n)]
    
    return [row[n:] for row in aug]
