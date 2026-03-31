from back_substitution import Expression, back_substitution

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

def gaussian_eliminate(A, b=None):
    if not A: 
        # Return matrix of Expression objects instead of empty lists
        return [], [[Expression()]], 0
    
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
    a = Expression([1,2,3,4], ['a', 'b', 'c'])
    b = Expression([-2, 3, 4, 6], ['a', 'b', 'c', 'd'])
    
    
    
if __name__ == "__main__":
    main()
