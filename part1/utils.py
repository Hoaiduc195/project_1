import numpy as np


# Helper functions for gaussian_eliminate()
###
def swap_row(A, i, j):
    """Swap rows ``i`` and ``j`` of matrix ``A`` in-place."""
    if i != j:
        A[i], A[j] = A[j], A[i]

def mul_row(A, i, c):
    """Multiply row ``i`` of matrix ``A`` by scalar ``c`` in-place."""
    for k in range(len(A[i])):
        A[i][k] *= c

def add_row(A, c, j, i):
    """Add ``c`` times row ``j`` to row ``i`` in matrix ``A`` in-place."""
    for k in range(len(A[i])):
        A[i][k] += A[j][k] * c

def build_augmented_matrix(A, b):
    """Return the augmented matrix [A|b] by extending each row of ``A``
    with the corresponding row from ``b``.
    """
    aug = [row[:] for row in A]
    for i in range(len(A)):
        aug[i].extend(b[i][:])
    return aug
###

# Verify Solution Function

def verify_solution(A, x, b, eps=1e-10):
    A = np.array(A, dtype=float)
    x = np.array(x, dtype=float)
    b = np.array(b, dtype=float)

    # reshape x nếu cần (vector cột)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    if b.ndim == 1:
        b = b.reshape(-1, 1)

    Ax = A @ x

    # kiểm tra gần đúng
    return np.allclose(Ax, b, atol=eps)