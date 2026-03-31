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
        if isinstance(other, Expression):
            newmp = {}
            vars = set()
            for k in other.mp.keys(): vars.add(k)
            for k in self.mp.keys(): vars.add(k)

            for var in vars:
                newmp[var] = 0.0
                if var in self.mp:
                    newmp[var] += self.mp[var]
                if var in other.mp:
                    newmp[var] += other.mp[var]

            for k, v in list(newmp.items()):
                if v == 0:
                    del newmp[k]
            self.mp = newmp
        elif isinstance(other, (float, int)):
            if self.__bias not in self.mp:
                self.mp[self.__bias] = float(other)
            else: self.mp[self.__bias] += float(other)
        elif isinstance(other, str):  # consider string as a new var
            if other in self.mp:
                self.mp[other] += 1.0
            else: self.mp[other] = 1.0
        
        return self

    def __sub__(self, other):
        if isinstance(other, Expression):
            newmp = {}
            vars = set()
            for k in other.mp.keys(): vars.add(k)
            for k in self.mp.keys(): vars.add(k)

            for var in vars:
                newmp[var] = 0.0
                if var in self.mp:
                    newmp[var] += self.mp[var]
                if var in other.mp:
                    newmp[var] -= other.mp[var]

            for k, v in list(newmp.items()):
                if v == 0:
                    del newmp[k]
            self.mp = newmp
        elif isinstance(other, (float, int)):
            if self.__bias not in self.mp:
                self.mp[self.__bias] = -float(other)
            else: self.mp[self.__bias] -= float(other)
        elif isinstance(other, str):
            if other in self.mp:
                self.mp[other] -= 1.0
            else: self.mp[other] = -1.0
        
        return self

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            scalar = float(other)
            for k in self.mp:
                self.mp[k] *= scalar
        else:
            raise TypeError("Only scalar multiplication supported")
        
        return self

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            scalar = float(other)
            if scalar == 0:
                raise ValueError("Division by zero")
            for k in self.mp:
                self.mp[k] /= scalar
        else:
            raise TypeError("Only scalar division supported")
        
        return self
    
    def __str__(self):
        ans = ''
        tokens = []
        for k, v in self.mp.items():
            if k == self.__bias:
                continue
            if abs(v) != 1.0:
                tokens.append(str(v) + k) 
            else:
                if v == -1.0:
                    tokens.append('-' + k)
                else: tokens.append(k)
        
        
        for i in range(len(tokens)): 
            if i == 0:
                ans += tokens[i]
            else:
                if tokens[i][0] == '-':
                    ans += tokens[i]
                else: 
                    ans += ' + ' + tokens[i]
            
        if self.__bias in self.mp:
            bias_val = self.mp[self.__bias]
            if bias_val >= 0 and ans:
                ans += ' + ' + str(bias_val)
            else:
                ans += str(bias_val)

        return ans


def back_substitution(U, c):
    if not U: 
        # Return empty matrix of Expressions
        if not c or len(c[0]) == 0:
            return []
        return [[Expression() for _ in range(len(c[0]))] for _ in range(len(U))]
    
    n = len(U)
    if not c or len(c[0]) == 0:
        return []
    
    num_c = len(c[0])
    x = [[Expression() for _ in range(num_c)] for _ in range(n)]
    
    for p in range(num_c):
        for k in range(n-1, -1, -1):
            r = Expression(c[k][p:p+1], []) if isinstance(c[k][p], (int, float)) else c[k][p]
            for u in range(k+1, n):
                r = r - (x[u][p] * U[k][u])
            if U[k][k] == 0:
                if isinstance(r, Expression) and not r.mp:
                    continue
                else: 
                    return None
            x[k][p] = r / U[k][k]
            
    if num_c == 1:
        return [x_row[0] for x_row in x]
    return x
