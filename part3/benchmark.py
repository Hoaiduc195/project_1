import time
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
from .solvers import solve_gaussian, solve_svd, solve_gauss_seidel
from part2.decomposition import transpose, mat_mul, vec_sub

def mat_vec_mul(A, x):
    if x is None: return None
    res = []
    for row in A:
        val = 0.0
        for i, v in enumerate(row):
            # Chuyển đổi từ Expression sang float nếu cần
            x_i = float(x[i].mp.get("__const__", 0.0)) if hasattr(x[i], 'mp') else float(x[i])
            val += v * x_i
        res.append(val)
    return res

def vec_norm(v):
    if v is None: return float('inf')
    return math.sqrt(sum(float(x)**2 for x in v))

def create_spd_matrix(n):
    # A = M*M^T + n*I
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    Mt = transpose(M)
    A = mat_mul(M, Mt)
    for i in range(n):
        A[i][i] += n
    return A

def create_hilbert_matrix(n):
    # Hilbert H_ij = 1 / (i + j + 1)
    return [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    
# sizes = [50, 100, 200, 500, 1000]

def benchmark(sizes):
    results = []

    for n in sizes:
        s = time.time()
        A = create_spd_matrix(n)
        x_true = [random.random() for _ in range(n)]
        b = mat_vec_mul(A, x_true)
        e = time.time() - s
        print(f"Generated SPD matrix of size {n} in {e:.4f} seconds.")
        
        methods = {
            "Gauss": solve_gaussian,
            "SVD": solve_svd,
            "Gauss-Seidel": solve_gauss_seidel
        }
        
        for name, method in methods.items():
            times = []
            for _ in range(3):
                start = time.time()
                x_pred = method(A, b)
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            
            # Relative error: ||Ax - b|| / ||b||
            s = time.time()
            Ax_p = mat_vec_mul(A, x_pred)
            if Ax_p:
                rel_error = vec_norm(vec_sub(Ax_p, b)) / (vec_norm(b) + 1e-15)
            else:
                rel_error = float('nan')
            e = time.time() - s
            results.append({"n": n, "Method": name, "Time": avg_time, "Error time": e, "Error": rel_error})

    df = pd.DataFrame(results)
    return df

def plot_results(df, sizes):
    plt.figure(figsize=(10, 6))

    for name in df["Method"].unique():
        subset = df[df["Method"] == name]
        if not subset.empty:
            plt.loglog(subset["n"], subset["Time"], label=f'{name}', marker='o')

    # O(n^3) theoretical line based on the first data point of Gauss method
    if not df[df["Method"] == "Gauss"].empty:
        first_time = df[df["Method"] == "Gauss"]["Time"].iloc[0]
        first_n = df[df["Method"] == "Gauss"]["n"].iloc[0]
        y_theory = [first_time * (n / first_n)**3 for n in sizes]
        plt.loglog(sizes, y_theory, '--', label='O(n^3) Theoretical', color='gray')

    plt.xlabel('Size of Matrix (log scale)')
    plt.ylabel('Execution Time (s) (log scale)')
    plt.title('Comparison of Execution Time: Experimental (Pure Python) vs Theoretical')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()

def stability_analysis(n_stable=10):
    print(f"\nStability Analysis (n={n_stable}):")

    A_hilbert = create_hilbert_matrix(n_stable)
    b_hilbert = [1.0] * n_stable

    A_spd = create_spd_matrix(n_stable)
    b_spd = [1.0] * n_stable

    stability_results = []
    for name, method in [("Gauss", solve_gaussian), ("SVD", solve_svd)]:
        x_h = method(A_hilbert, b_hilbert)
        Ax_h = mat_vec_mul(A_hilbert, x_h)
        err_h = vec_norm(vec_sub(Ax_h, b_hilbert)) / vec_norm(b_hilbert) if Ax_h else float('nan')
        
        x_s = method(A_spd, b_spd)
        Ax_s = mat_vec_mul(A_spd, x_s)
        err_s = vec_norm(vec_sub(Ax_s, b_spd)) / vec_norm(b_spd) if Ax_s else float('nan')
        
        stability_results.append({"Method": name, "Error Hilbert": err_h, "Error SPD": err_s})

    return pd.DataFrame(stability_results)