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

def expr_to_numeric(x):
    """
    Convert an Expression, list of Expressions, or nested list of
    Expressions into numeric values.

    If an Expression contains symbolic variables, a ValueError is raised.
    """
    if isinstance(x, Expression):
        variables = [k for k in x.mp if k != Expression.BIAS]
        if variables:
            raise ValueError(
                f"Cannot convert symbolic Expression to numeric: {variables}"
            )
        return float(x.mp.get(Expression.BIAS, 0.0))

    if isinstance(x, list):
        return [expr_to_numeric(item) for item in x]

    return float(x)