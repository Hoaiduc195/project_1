import numpy as np
import math
from decomposition import do_svd_primitive, do_svd_numpy
from diagonalization import do_diagonalization_primitive, do_diagonalization_numpy

def print_result(name, passed, error=None):
    status = "[PASS]" if passed else "[FAIL]"
    error_str = f" (Error: {error:.2e})" if error is not None else ""
    print(f"{status} {name}{error_str}")

# Test cases have 2 tags: svd and diag
# Each tag perform each test using primitive and numpy

# SVD: Multiply U, Sigma, transpose(V) to see if it equals A
# or compare singular value against np.linalg.svd 

# Diagonalization: Multiply P, D, transpose(P) to see if it equals A
# or compare eigenvalues against np.linalg.eigh
def test_SVD_and_diagonalization():
    print("=" * 60)
    print("TESTING SVD AND DIAGONALIZATION")
    print("=" * 60)

    # Test cases
    test_cases = [
        {
            "name": "Small square (2x2)",
            "matrix": [[1.0, 2.0], [3.0, 4.0]],
            "types": ["svd"] # Diagonalization requires symmetric
        },
        {
            "name": "Small symmetric (2x2)",
            "matrix": [[2.0, 1.0], [1.0, 2.0]],
            "types": ["svd", "diag"]
        },
        {
            "name": "Identity (3x3)",
            "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "types": ["svd", "diag"]
        },
        {
            "name": "Zero (3x3)",
            "matrix": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            "types": ["svd", "diag"]
        },
        {
            "name": "Diagonal (3x3)",
            "matrix": [[5.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, -1.0]],
            "types": ["svd", "diag"]
        },
        {
            "name": "Singular (3x3)",
            "matrix": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
            "types": ["svd", "diag"] # This is not symmetric to check SVD 
        },
        {
            "name": "Rectangular (5x2)",
            "matrix": [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]],
            "types": ["svd"]
        },
        {
            "name": "Rank-1 (3x3)",
            "matrix": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            "types": ["svd", "diag"]
        }
    ]

    # Additional symmetric cases for diagonalization
    symmetric_case = {
        "name": "Symmetric with Negative",
        "matrix": [[2, -1, 0], [-1, 2, -1], [0, -1, 2]],
        "types": ["svd", "diag"]
    }
    test_cases.append(symmetric_case)

    # epsilon
    tolerance = 1e-4

    for case in test_cases:
        name = case["name"]
        A = case["matrix"]
        A_np = np.array(A)
        
        print(f"\n--- Testing Case: {name} ---")

        if "svd" in case["types"]:
            try:
                # Primitive SVD
                U_p, S_p, Vt_p = do_svd_primitive(A)
                A_rec_p = np.array(U_p) @ np.array(S_p) @ np.array(Vt_p)
                error_p = np.linalg.norm(A_np - A_rec_p)
                
                # NumPy SVD
                U_n, S_n, Vt_n = do_svd_numpy(A)
                
                s_p = np.diag(np.array(S_p))
                s_n = np.diag(S_n)
                
                s_match = np.allclose(np.sort(s_p), np.sort(s_n), atol=tolerance)
                
                print_result(f"{name} (SVD reconstruction)", error_p < tolerance, error_p)
                print_result(f"{name} (SVD singular values match)", s_match)
                
            except Exception as e:
                print(f"[ERROR] SVD failed for {name}: {e}")

        if "diag" in case["types"]:
            is_symmetric = np.allclose(A_np, A_np.T, atol=1e-10)
            if not is_symmetric:
                print(f"[SKIP] Diagonalization skipped for {name} (Not symmetric)")
                continue

            try:
                # Primitive diagonalization
                P_p, evals_p = do_diagonalization_primitive(A)
                P_p_np = np.array(P_p)
                A_rec_p = P_p_np @ np.diag(evals_p) @ P_p_np.T
                error_p = np.linalg.norm(A_np - A_rec_p)
                
                # NumPy diagonalization
                P_n, evals_n = do_diagonalization_numpy(A)
                
                # Compare eigenvalues
                evals_p_sorted = np.sort(evals_p)
                evals_n_sorted = np.sort(evals_n)
                evals_match = np.allclose(evals_p_sorted, evals_n_sorted, atol=tolerance)
                
                print_result(f"{name} (Diag reconstruction)", error_p < tolerance, error_p)
                print_result(f"{name} (Diag eigenvalues match)", evals_match)
                
            except Exception as e:
                print(f"[ERROR] Diagonalization failed for {name}: {e}")

if __name__ == "__main__":
    test_SVD_and_diagonalization()