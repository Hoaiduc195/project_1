import numpy as np
from back_substitution import Expression, back_substitution
from utils import swap_row, mul_row, add_row, build_augmented_matrix

EPS = 1e-10

def gaussian_eliminate(A, b=None):
    """
    Perform Gaussian elimination on matrix ``A`` with optional right-
    hand side ``b``.\n
    Returns a tuple ``(U, x, num_swaps)`` where ``U`` is
    the filtered upper-triangular matrix, ``x`` contains solved
    `Expression` objects (or empty), and ``num_swaps`` is the count of row
    swaps performed.\n
    If the system is inconsistent returns ``(None, None,
    swaps)``.
    """
    
    if not A: 
        # return matrix of Expression if A is empty
        return [], [[Expression()]], 0
    
    nr = len(A)
    nc = len(A[0])
    
    # convert b from 1D to 2D if needed
    if b is None:
        b = [[] for _ in range(nr)]
    elif b and isinstance(b[0], (int, float)):
        b = [[val] for val in b]
    elif not b or len(b[0]) == 0:
        b = [[] for _ in range(nr)]
          
    aug = build_augmented_matrix(A, b)
    a_cols = nc
    num_swaps = 0
    
    pivot_row = 0

    for k in range(a_cols):
        if pivot_row >= nr:
            break
        # find largest pivot in column k
        max_idx = pivot_row
        while max_idx < nr and abs(aug[max_idx][k]) < EPS:
            max_idx += 1

        if max_idx == nr:
            continue  # no pivot in this column, move to next column (same row)

        for u in range(max_idx, nr):
            if abs(aug[u][k]) > abs(aug[max_idx][k]):
                max_idx = u
        if pivot_row != max_idx:
            swap_row(aug, pivot_row, max_idx)
            num_swaps += 1
        # eliminate all rows below pivot_row
        for u in range(pivot_row + 1, nr):
            if abs(aug[pivot_row][k]) > EPS:
                q = float(aug[u][k]) / aug[pivot_row][k]
                add_row(aug, -q, pivot_row, u)
        pivot_row += 1
    
    # check for inconsistency and collect non-zero rows
    filtered_aug = []
    for row in aug:
        coeff_part = row[:a_cols]
        rhs_part = row[a_cols:]
        
        if all(abs(v) < EPS for v in coeff_part):
            if any(abs(v) > EPS for v in rhs_part):
                return None, None, num_swaps  # inconsistent
            continue
        filtered_aug.append(row)
    
    # extract upper triangle matrix and c from filtered augmented matrix
    U = [row[:a_cols] for row in filtered_aug]
    c_part = [row[a_cols:] for row in filtered_aug]
    
    x = back_substitution(U, c_part) if (c_part and len(c_part[0]) > 0) else []
    
    return U, x, num_swaps

def main():
    test_cases_A = [
    [[0, 2], [3, -1]],
    [[1, 1], [1, -1], [2, 1]],
    [[1, 2, 3], [2, -1, 1]],
    [[1e-4, 1], [1, 1]]
    ]

    test_cases_b = [
    [[4], [5]],
    [[2], [0], [5]],
    [[4], [5]],
    [[1], [2]]
    ]

    def expr_to_numeric(e):
        if not isinstance(e, Expression):
            return e
        keys = list(e.mp.keys())
        if not keys:
            return 0.0
        if len(keys) == 1 and Expression.BIAS in e.mp:
            return float(e.mp[Expression.BIAS])
        return None

    def run_list(cases, group_name):
        if not cases:
            print(f"No cases in {group_name}.")
            return
        for idx, case in enumerate(cases, start=1):
            if not isinstance(case, list) or not case or not isinstance(case[0], (list, tuple)):
                print(f"Skipping invalid test case at index {idx} in {group_name}: not a matrix")
                continue

            rows = len(case)
            cols = len(case[0])
            if any(len(r) != cols for r in case):
                print(f"Skipping invalid test case at index {idx} in {group_name}: ragged rows")
                continue

            # interpret matrix
            if cols == rows + 1:
                A = [list(r[:cols-1]) for r in case]
                b = [[r[-1]] for r in case]
            elif cols == rows:
                A = [list(r) for r in case]
                b = None
            elif cols >= 2:
                A = [list(r[:-1]) for r in case]
                b = [[r[-1]] for r in case]
            else:
                print(f"Skipping invalid test case at index {idx} in {group_name}: not enough columns")
                continue

            print(f"--- {group_name} {idx} ---")

            U, x_exprs, swaps = gaussian_eliminate(A, b)

            # numpy comparison
            numpy_result = None
            try:
                if b is not None:
                    A_np = np.array(A, dtype=float)
                    b_vec = np.array([row[0] for row in b], dtype=float)
                    try:
                        numpy_result = np.linalg.solve(A_np, b_vec)
                    except np.linalg.LinAlgError:
                        numpy_result, *_ = np.linalg.lstsq(A_np, b_vec, rcond=None)
            except Exception as e:
                numpy_result = f"numpy error: {e}"

            if U is None:
                print("Result: Inconsistent system")
            else:
                print("U (upper-triangular):")
                for row in U:
                    print(row)

                print("Code solution (Expressions):")
                if not x_exprs:
                    print("(no solution / empty)")
                else:
                    numeric_from_code = []
                    for e in x_exprs:
                        print(e)
                        numeric_from_code.append(expr_to_numeric(e))
                    print("Code solution (numeric when available):")
                    print(numeric_from_code)

                print(f"Row swaps: {swaps}")

            print("Numpy solution:", numpy_result)
            print()

    run_list(test_cases_A, "A")
    run_list(test_cases_b, "b")
    
if __name__ == "__main__":
    main()
