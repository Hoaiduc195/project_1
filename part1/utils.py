import numpy as np

class Expression:
    """Represents a linear expression mapping variable names to coefficients
    and an optional constant bias.\n
    Supports arithmetic operations used to
    build symbolic solutions during back substitution.
    """
    
    BIAS = "__const__"
    EPS = 1e-10

    def __init__(self, nums=None, var=None):
        nums = nums or []
        var = var or []

        if len(nums) not in (len(var), len(var) + 1):
            raise ValueError("Invalid number of coefficients")

        self.mp = {}

        for i, v in enumerate(var):
            self.mp[v] = float(nums[i])

        if len(nums) == len(var) + 1:
            self.mp[self.BIAS] = float(nums[-1])

    def _combine(self, other, sign=1):
        result = Expression()
        result.mp = self.mp.copy()

        for k, v in other.mp.items():
            result.mp[k] = result.mp.get(k, 0.0) + sign * v

        # remove near-zero terms
        result.mp = {k: v for k, v in result.mp.items() if abs(v) > self.EPS}
        return result

    def __add__(self, other):
        if isinstance(other, Expression):
            return self._combine(other, +1)
        elif isinstance(other, (int, float)):
            return self._combine(Expression([other], []), +1)
        elif isinstance(other, str):
            return self._combine(Expression([1], [other]), +1)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Expression):
            return self._combine(other, -1)
        elif isinstance(other, (int, float)):
            return self._combine(Expression([other], []), -1)
        elif isinstance(other, str):
            return self._combine(Expression([1], [other]), -1)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = Expression()
            result.mp = {k: v * other for k, v in self.mp.items()}
            return result
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if abs(other) < self.EPS:
                raise ValueError("Division by zero")
            return self * (1.0 / other)
        return NotImplemented

    def __str__(self):
        terms = []
        for k in sorted(self.mp.keys()):
            if k == self.BIAS:
                continue
            v = self.mp[k]
            coef = "" if abs(v) == 1 else str(abs(v))
            term = coef + k

            if not terms:
                terms.append(term if v > 0 else "- " + term)
            else:
                terms.append((" + " if v > 0 else " - ") + term)

        if self.BIAS in self.mp:
            v = self.mp[self.BIAS]
            if terms:
                terms.append((" + " if v >= 0 else " - ") + str(abs(v)))
            else:
                terms.append(str(v))

        return "".join(terms) if terms else "0"


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
    """Quickly validate a solution from `gaussian_eliminate`.\n
    Returns: (is_valid, status) where status in
    {"no_solution", "unique_solution", "infinite_solutions", "invalid_general_solution"}.
    """
    
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1)

    # x is a vector of numbers 
    if not isinstance(x[0], Expression):
        x_vec = np.array(x, dtype=float).reshape(-1)
        Ax = A @ x_vec

        is_valid = np.allclose(Ax, b, atol=eps)
        
        rank_A = np.linalg.matrix_rank(A)
        rank_aug = np.linalg.matrix_rank(np.c_[A, b])
        n = A.shape[1]

        if rank_A < rank_aug:
            return False, "no_solution"
        elif rank_A == n:
            return is_valid, "unique_solution"
        else:
            return is_valid, "infinite_solutions"

    # x is a vector of Expression
    m, n = A.shape
    Ax = []

    for i in range(m):
        expr = Expression()
        for j in range(n):
            expr += x[j] * A[i, j]
        Ax.append(expr)

    for i in range(m):
        expr = Ax[i]

        const = expr.mp.get(Expression.BIAS, 0.0)
        
        # check variables
        for k, v in expr.mp.items():
            if k != Expression.BIAS and abs(v) > eps:
                return False, "invalid_general_solution"

        # check constanst
        if abs(const - b[i]) > eps:
            return False, "invalid_general_solution"

    # classify result
    rank_A = np.linalg.matrix_rank(A)
    rank_aug = np.linalg.matrix_rank(np.c_[A, b])
    n = A.shape[1]

    if rank_A < rank_aug:
        return False, "no_solution"
    elif rank_A == n:
        return True, "unique_solution"
    else:
        return True, "infinite_solutions"