
class Expression:
    def __init__(self, nums=[], var = []):
        self.mp = {}
        if len(nums) > len(var) + 1 or len(nums) < len(var):
            return RuntimeError
    
        self.__bias = 'bias'
        for i in range(len(var)):
            self.mp[var[i]] = float(nums[i])
        
        # handle the only number
        if len(nums) == len(var) + 1:
            self.mp[self.__bias] = nums[-1] 

    def __add__(self, other):
        if isinstance(other, Expression):
            newmp = {}
            vars = set()
            for k in other.mp.keys(): vars.add(k)
            for k in self.mp.keys(): vars.add(k)

            for var in vars:
                if var in other.mp:
                    newmp[var] += other.mp[var]
                if var in other.mp:
                    newmp[var] += other.mp[var]

            for k, v in newmp.items():
                if v == 0:
                    del newmp[k]
            self.mp = newmp
        elif isinstance(other, float):
            if self.__bias not in self.mp:
                self.mp[self.__bias] = other
            else: self.mp[self.__bias] += other
        elif isinstance(other, str): # consider str as one var
            if other in self.mp:
                self.mp[other] += 1.0
            else: self.mp[other] = 1.0
        
        return self
    
    def __str__(self):
        ans = ''
        for k, v in self.mp.items():
            if k == self.__bias:
                continue
            if abs(v) != 1.0:
                ans += v + '*' + k
            else:
                if v == -1.0:
                    ans += '-' + k
                else: ans += '+' if ans == '' else '' + k
                
        if self.__bias in self.mp:
            ans += self.mp[self.__bias]

        return ans
    

def swap_row(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]

def mul_row(A, i, c):
    for k in range(len(A[i])):
        A[i][k] *= c

def add_row(A, c, j, i):
    for k in range(len(A[i])):
        A[i][k] += A[j][k] * c

def build_augmented_matrix(A, b):
    aug = [row[:] for row in A]
    for i in range(len(A)):
        aug[i].extend(b[i][:])
    return aug

def back_substitution(U, c):
    if not U: return []
    n = len(U)
    if not c or len(c[0]) == 0:
        return []
    
    num_c = len(c[0])
    x = [[0.0] * num_c for _ in range(n)]
    
    for p in range(num_c):
        for k in range(n-1, -1, -1):
            r = c[k][p]
            for u in range(k+1, n):
                r -= x[u][p] * U[k][u]
            if U[k][k] == 0:
                if r == 0: continue
                else: return None
            x[k][p] = float(r) / U[k][k]
            
    if num_c == 1:
        return [x_row[0] for x_row in x]
    return x




def gaussian_eliminate(A, b=None):
    if not A: return [], [], 0
    nr = len(A)
    nc = len(A[0])
    if b is None or not b or len(b[0]) == 0:
        b = [[] for _ in range(nr)]
        
    aug = build_augmented_matrix(A, b)
    a_cols = nc
    num_swaps = 0
    
    for k in range(min(nr, a_cols)):
        max_idx = k
        while max_idx < nr and aug[max_idx][k] == 0:
            max_idx += 1
        if max_idx == nr:
            continue
        for u in range(max_idx, nr):
            if abs(aug[u][k]) > abs(aug[max_idx][k]):
                max_idx = u
        if k != max_idx:
            swap_row(aug, k, max_idx)
            num_swaps += 1
        for u in range(k+1, nr):
            if aug[k][k] != 0:
                q = float(aug[u][k]) / aug[k][k]
                add_row(aug, -q, k, u)
                
    U = [row[:a_cols] for row in aug]
    c_part = [row[a_cols:] for row in aug]
    x = back_substitution(U, c_part) if len(c_part[0]) > 0 else []
    
    return U, x, num_swaps

def print_matrix(mat):
    for row in mat:
        print(["{:.4f}".format(v) for v in row])

def main():
    # A = [[1.0, 2.0, 3.0], [1.0, 2.0, 4.0], [1.0, 5.0, 6.0]]
    a = Expression([1,2,3, 4], ['a', 'b', 'c'])
    
    print(a)
if __name__ == "__main__":
    main()
