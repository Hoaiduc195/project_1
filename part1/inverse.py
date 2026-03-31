from gaussian import build_augmented_matrix, swap_row, add_row, mul_row

def inverse(A):
    n = len(A)
    if n == 0 or n != len(A[0]): return None
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    aug = build_augmented_matrix(A, I)
    nr = len(aug)
    nc = len(aug[0])
    
    for k in range(n):
        max_idx = k
        while max_idx < nr and aug[max_idx][k] == 0:
            max_idx += 1
        if max_idx == nr:
            return None # singular
        for u in range(max_idx, nr):
            if abs(aug[u][k]) > abs(aug[max_idx][k]):
                max_idx = u
        if k != max_idx:
            swap_row(aug, k, max_idx)
        
        q = 1.0 / aug[k][k]
        mul_row(aug, k, q)
        for u in range(k+1, nr):
            q_val = float(aug[u][k])
            add_row(aug, -q_val, k, u)
    
    for k in range(n-1, -1, -1):
        for u in range(k-1, -1, -1):
            q_val = float(aug[u][k])
            add_row(aug, -q_val, k, u)
            
    return [row[n:] for row in aug]
