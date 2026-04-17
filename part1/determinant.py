from gaussian import gaussian_eliminate

def determinant(A):
    """Compute the determinant of a square matrix ``A`` using Gaussian
    elimination. Returns the determinant as a float, or ``None`` for
    non-square input.
    """
    n = len(A)
    # only square matrices have det
    if n == 0 or n != len(A[0]): return None
    
    b = [[] for _ in range(n)]
    
    res, _, num_swaps = gaussian_eliminate(A, b)
    det = 1.0
    
    for i in range(min(n, len(res[0]))):
        det *= res[i][i]
    if num_swaps % 2 == 1:
        det = -det
    return det


def main():
    pass

if __name__ == "__main__":
    main()