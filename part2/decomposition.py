import math
import random
import numpy as np

# --- Primitive Matrix Operations ---
def zeros(m, n):
    return [[0.0 for _ in range(n)] for _ in range(m)]

def copy_mat(A):
    return [[val for val in row] for row in A]

def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_mul(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = zeros(m, n)
    for i in range(m):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(p))
    return C

def get_col(A, j):
    return [row[j] for row in A]

def set_col(A, j, v):
    for i in range(len(A)):
        A[i][j] = v[i]

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def norm(v):
    return math.sqrt(dot(v, v))

def vec_sub(v1, v2):
    return [x - y for x, y in zip(v1, v2)]

def vec_mul(v, scalar):
    return [x * scalar for x in v]

def eye(n):
    I = zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I

def get_diag(A):
    n = min(len(A), len(A[0]))
    return [A[i][i] for i in range(n)]

def argsort_desc(seq):
    return sorted(range(len(seq)), key=seq.__getitem__, reverse=True)

def gram_schmidt(A):
    m = len(A)
    n = len(A[0])
    Q = zeros(m, n)
    R = zeros(n, n)
    v = copy_mat(A)
    
    for j in range(n):
        v_j = get_col(v, j)
        for i in range(j):
            Q_i = get_col(Q, i)
            R[i][j] = dot(Q_i, v_j)
            proj = vec_mul(Q_i, R[i][j])
            v_j = vec_sub(v_j, proj)
            
        R[j][j] = norm(v_j)
        if R[j][j] > 1e-14:
            q_j = vec_mul(v_j, 1.0 / R[j][j])
        else:
            q_j = [0.0] * m
        set_col(Q, j, q_j)
        set_col(v, j, v_j)
    return Q, R


# --- SVD Implementations ---

def do_svd_primitive(A, num_iters=200):
    """
    Compute Singular Value Decomposition (SVD) using primitive operations.
    Returns U, S (as diagonal matrix), and Vt.
    """
    m = len(A)
    n = len(A[0])
    
    At = transpose(A)
    AtA = mat_mul(At, A)
    
    A_k = copy_mat(AtA)
    V_k = eye(n)
    
    for _ in range(num_iters):
        Q, R = gram_schmidt(A_k)
        A_k = mat_mul(R, Q)
        V_k = mat_mul(V_k, Q)
        
    eigenvalues = get_diag(A_k)
    eigenvalues = [max(e, 0.0) for e in eigenvalues]
    singular_values = [math.sqrt(e) for e in eigenvalues]
    
    idx = argsort_desc(singular_values)
    singular_values_sorted = [singular_values[i] for i in idx]
    
    V_sorted = zeros(n, n)
    for j, index in enumerate(idx):
        set_col(V_sorted, j, get_col(V_k, index))
        
    Vt = transpose(V_sorted)
    
    U = zeros(m, n)
    S = zeros(n, n)
    for i in range(n):
        S[i][i] = singular_values_sorted[i]
        sigma = singular_values_sorted[i]
        if sigma > 1e-10:
            v_i = get_col(V_sorted, i)
            res = [0.0] * m
            for row in range(m):
                res[row] = dot(A[row], v_i)
            u_i = vec_mul(res, 1.0 / sigma)
            set_col(U, i, u_i)
            
    return U, S, Vt


def do_svd_numpy(A):
    """
    Compute SVD using numpy's built-in function.
    Returns restricted SVD (U is m x n, S is n x n diagonal, Vt is n x n)
    """
    A_np = np.array(A)
    U, S_diag, Vt = np.linalg.svd(A_np, full_matrices=False)
    S = np.diag(S_diag)
    return U, S, Vt


def fact_check():
    print("=" * 50)
    print("FACT CHECK: SVD Decomposition (Primitive vs NumPy)")
    print("=" * 50)
    
    random.seed(42)
    np.random.seed(42)
    
    # Generate a random 5x3 matrix
    A_rect = [[random.random() for _ in range(3)] for _ in range(5)]
    print("Original Matrix A (5x3):")
    print(np.round(np.array(A_rect), 4))
    
    # Primitive execution
    U_prim, S_prim, Vt_prim = do_svd_primitive(A_rect)
    
    # NumPy execution
    U_np, S_np, Vt_np = do_svd_numpy(A_rect)
    
    # Verification and Output Checks 
    S_prim_diag = np.diag(np.array(S_prim))
    S_np_diag = np.diag(S_np)
    
    print("\n--- Singular Values Comparison ---")
    print(f"Primitive: {np.round(S_prim_diag, 4)}")
    print(f"NumPy:     {np.round(S_np_diag, 4)}")
    
    s_match = np.allclose(S_prim_diag, S_np_diag, atol=1e-4)
    print(f"Singular Values Match: {'YES' if s_match else 'NO'}")
    
    # Check Reconstruction (A = U @ S @ V^T)
    A_rec_prim = np.array(U_prim) @ np.array(S_prim) @ np.array(Vt_prim)
    
    print("\n--- Reconstruction Comparison ---")
    rec_error = np.linalg.norm(np.array(A_rect) - A_rec_prim)
    print(f"Primitive Reconstruction Error: {rec_error:.2e}")
    if rec_error < 1e-5 and s_match:
        print("\n=> SUCCESS: Primitive implementation perfectly matches NumPy's capabilities.")
    else:
        print("\n=> FAILURE: The results do not match.")

if __name__ == "__main__":
    fact_check()
