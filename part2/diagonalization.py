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

# --- Diagonalization Implementations ---

def do_diagonalization_primitive(A, num_iters=200):
    """
    Diagonalize a symmetric matrix using primitive operations (QR iteration).
    Returns P (eigenvectors) and eigenvalues.
    """
    n = len(A)
    A_k = copy_mat(A)
    P = eye(n)
    
    for _ in range(num_iters):
        Q, R = gram_schmidt(A_k)
        A_k = mat_mul(R, Q)
        P = mat_mul(P, Q)
        
    eigenvalues = get_diag(A_k)
    return P, eigenvalues

def do_diagonalization_numpy(A):
    """
    Diagonalize a symmetric matrix using numpy.
    Returns P (eigenvectors) and eigenvalues.
    """
    A_np = np.array(A)
    eigenvalues, eigenvectors = np.linalg.eig(A_np)
    return eigenvectors, eigenvalues

def fact_check():
    print("=" * 50)
    print("FACT CHECK: Diagonalization (Primitive vs NumPy)")
    print("=" * 50)
    
    random.seed(42)
    np.random.seed(42)
    
    # Generate a random symmetric 3x3 matrix
    B = [[random.random() for _ in range(3)] for _ in range(3)]
    A_sym = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            A_sym[i][j] = B[i][j] + B[j][i]
            
    print("Original Symmetric Matrix A:")
    print(np.round(np.array(A_sym), 4))
    
    # Primitive execution
    P_prim, evals_prim = do_diagonalization_primitive(A_sym)
    
    # NumPy execution
    P_np, evals_np = do_diagonalization_numpy(A_sym)
    
    # Verification and Output Checks
    P_prim_np = np.array(P_prim)
    evals_prim_np = np.array(evals_prim)
    
    # Compare Eigenvalues (sorted since order doesn't matter)
    evals_prim_sorted = np.sort(evals_prim_np)
    evals_np_sorted = np.sort(evals_np)
    
    print("\n--- Eigenvalues Comparison ---")
    print(f"Primitive (sorted): {np.round(evals_prim_sorted, 4)}")
    print(f"NumPy (sorted):     {np.round(evals_np_sorted, 4)}")
    
    evals_match = np.allclose(evals_prim_sorted, evals_np_sorted, atol=1e-4)
    print(f"Eigenvalues Match:  {'YES' if evals_match else 'NO'}")
    
    # Compare Reconstruction (A = P @ D @ P^T)
    A_rec_prim = P_prim_np @ np.diag(evals_prim_np) @ P_prim_np.T
    
    print("\n--- Reconstruction Comparison ---")
    rec_error = np.linalg.norm(np.array(A_sym) - A_rec_prim)
    print(f"Primitive Reconstruction Error: {rec_error:.2e}")
    if rec_error < 1e-5 and evals_match:
        print("\n=> SUCCESS: Primitive implementation perfectly matches NumPy's capabilities.")
    else:
        print("\n=> FAILURE: The results do not match.")

if __name__ == "__main__":
    fact_check()
