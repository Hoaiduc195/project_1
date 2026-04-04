class Expression:
    def __init__(self, nums=[], var = []):
        self.mp = {}
        if len(nums) > len(var) + 1 or len(nums) < len(var):
            return RuntimeError
    
        self.__bias = 'bias'
        for i in range(len(var)):
            self.mp[var[i]] = float(nums[i])
        
        # handle bias
        if len(nums) == len(var) + 1:
            self.mp[self.__bias] = nums[-1] 

    def __add__(self, other):
        new_expr = Expression()
        new_expr.mp = {}
        
        if isinstance(other, Expression):
            vars = set()
            for k in other.mp.keys(): vars.add(k)
            for k in self.mp.keys(): vars.add(k)

            for var in vars:
                new_expr.mp[var] = 0.0
                if var in self.mp:
                    new_expr.mp[var] += self.mp[var]
                if var in other.mp:
                    new_expr.mp[var] += other.mp[var]

            for k, v in list(new_expr.mp.items()):
                if v == 0:
                    del new_expr.mp[k]
        elif isinstance(other, (float, int)):
            new_expr.mp = self.mp.copy()
            if self.__bias not in new_expr.mp:
                new_expr.mp[self.__bias] = float(other)
            else: 
                new_expr.mp[self.__bias] += float(other)
        elif isinstance(other, str):
            new_expr.mp = self.mp.copy()
            if other in new_expr.mp:
                new_expr.mp[other] += 1.0
            else: 
                new_expr.mp[other] = 1.0
        
        return new_expr

    def __sub__(self, other):
        new_expr = Expression()
        new_expr.mp = {}
        
        if isinstance(other, Expression):
            vars = set()
            for k in other.mp.keys(): vars.add(k)
            for k in self.mp.keys(): vars.add(k)

            for var in vars:
                new_expr.mp[var] = 0.0
                if var in self.mp:
                    new_expr.mp[var] += self.mp[var]
                if var in other.mp:
                    new_expr.mp[var] -= other.mp[var]

            for k, v in list(new_expr.mp.items()):
                if v == 0:
                    del new_expr.mp[k]
        elif isinstance(other, (float, int)):
            new_expr.mp = self.mp.copy()
            if self.__bias not in new_expr.mp:
                new_expr.mp[self.__bias] = -float(other)
            else: 
                new_expr.mp[self.__bias] -= float(other)
        elif isinstance(other, str):
            new_expr.mp = self.mp.copy()
            if other in new_expr.mp:
                new_expr.mp[other] -= 1.0
            else: 
                new_expr.mp[other] = -1.0
        
        return new_expr

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            scalar = float(other)
            new_expr = Expression()
            new_expr.mp = {}
            for k in self.mp:
                new_expr.mp[k] = self.mp[k] * scalar
            return new_expr
        else:
            raise TypeError("Only scalar multiplication supported")

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            scalar = float(other)
            if scalar == 0:
                raise ValueError("Division by zero")
            # Create a new Expression to avoid modifying in-place
            new_expr = Expression()
            new_expr.mp = {}
            for k in self.mp:
                new_expr.mp[k] = self.mp[k] / scalar
            return new_expr
        else:
            raise TypeError("Only scalar division supported")
    
    def __str__(self):
        ans = ''
        tokens = []
        for k, v in self.mp.items():
            if k == self.__bias:
                continue
            if abs(v) != 1.0:
                tokens.append((v, str(abs(v)) + k)) 
            else:
                tokens.append((v, k))
        
        for i, (sign, term) in enumerate(tokens):
            if i == 0:
                if sign < 0:
                    ans += '- ' + term
                else:
                    ans += term
            else:
                if sign < 0:
                    ans += ' - ' + term
                else:
                    ans += ' + ' + term
            
        if self.__bias in self.mp:
            bias_val = self.mp[self.__bias]
            if bias_val >= 0 and ans:
                ans += ' + ' + str(bias_val)
            elif bias_val < 0 and ans:
                ans += ' - ' + str(abs(bias_val))
            else:
                ans += str(bias_val)
        elif not tokens:
            # No variables and no bias - this represents 0
            ans = '0'
        
        return ans


def back_substitution(U, c):
    if not U: 
        # Return empty matrix of Expressions
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
    pivot_cols = []
    pivot_row = {}
    for k in range(min(num_eqs, num_vars)):
        for j in range(num_vars):
            if abs(U[k][j]) > 1e-10:
                if j not in pivot_cols:
                    pivot_cols.append(j)
                    pivot_row[j] = k
                    break
    
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
            if abs(U[k][col]) > 1e-10:
                x[col][p] = r / U[k][col]
        
        # Check for inconsistency
        for k in range(num_eqs):
            all_zero = all(abs(U[k][j]) < 1e-10 for j in range(num_vars))
            if all_zero and abs(c[k][p]) > 1e-10:
                return None  # Inconsistent system
    
    if num_c == 1:
        return [x_row[0] for x_row in x]
    return x
