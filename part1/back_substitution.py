from utils import Expression

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
