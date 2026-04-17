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

def back_substitution(U, c):
    """Perform back substitution on an upper-triangular matrix ``U`` with
    right-hand side ``c``.\n 
    Returns a list (or list-of-lists) of
    :class:`Expression` objects representing the solution(s), or ``None``
    if the system is inconsistent.
    """
    
    if not U: 
        # return empty matrix of Expresssion
        if not c or len(c[0]) == 0:
            return []
        return [[Expression() for _ in range(len(c[0]))] for _ in range(len(U))]
    
    n = len(U)  # number of rows (equations)
    if not c or len(c[0]) == 0:
        return []
    
    m = len(U[0]) if U else 0  # number of columns (variables)
    num_c = len(c[0])
    
    num_vars = m
    num_eqs = n
    x = [[Expression() for _ in range(num_c)] for _ in range(num_vars)]
    
    # Find pivot columns (columns with leading non-zero in row k)
    tol = Expression.EPS
    pivot_cols = []
    pivot_row = {}

    for k in range(num_eqs):
        pivot_col = None
        
        for j in range(num_vars):
            if abs(U[k][j]) > tol:
                pivot_col = j
                break
        
        if pivot_col is None:
            continue  # skip zero row

        pivot_cols.append(pivot_col)
        pivot_row[pivot_col] = k
    
    # Free variables are those not in pivot_cols
    free_vars = [j for j in range(num_vars) if j not in pivot_cols]
    
    for p in range(num_c):
        # Initialize free variables as symbols
        for j in free_vars:
            var_name = f"t{j}"  # Parameter for free variable
            x[j][p] = Expression([1.0], [var_name])
        
        # Back substitution for pivot variables
        for col in reversed(pivot_cols):
            k = pivot_row[col]
            
            # Create RHS
            if isinstance(c[k][p], (int, float)):
                r = Expression([float(c[k][p])], [])  
            else:
                r = c[k][p]  
            
            # Subtract all other terms (both pivot and free variables)
            for j in range(num_vars):
                if j != col:
                    r = r - (x[j][p] * U[k][j])
            
            # Solve for pivot variable
            if abs(U[k][col]) > tol:
                x[col][p] = r / U[k][col]
        
        # Check for inconsistency
        for k in range(num_eqs):
            all_zero = all(abs(U[k][j]) < tol for j in range(num_vars))
            if all_zero and abs(c[k][p]) > tol:
                return None  # Inconsistent system
    
    if num_c == 1:
        return [x_row[0] for x_row in x]
    return x


def main():
    pass


if __name__ == "__main__":
    main()