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
    
    # Handle b parameter: convert 1D to 2D if needed
    if b is None:
        b = [[] for _ in range(nr)]
    elif b and isinstance(b[0], (int, float)):
        # b is 1D array like [0, 0, 0], convert to [[0], [0], [0]]
        b = [[val] for val in b]
    elif not b or len(b[0]) == 0:
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
    
    # Remove redundant rows (rows that are all zero in coefficient part)
    # and check for inconsistency
    filtered_aug = []
    used_pivots = set()  # Track pivot columns already used
    
    for row in aug:
        coeff_part = row[:a_cols]
        rhs_part = row[a_cols:]
        
        # Check if all coefficients are zero
        all_zero_coeff = all(abs(v) < 1e-10 for v in coeff_part)
        
        if all_zero_coeff:
            # Check consistency: if RHS is non-zero, system is inconsistent
            if any(abs(v) > 1e-10 for v in rhs_part):
                return None, None, num_swaps  # Inconsistent system
            # If RHS is also zero, skip this redundant row
            continue
        
        # Find pivot column for this row
        pivot_col = -1
        for j in range(len(coeff_part)):
            if abs(coeff_part[j]) > 1e-10:
                pivot_col = j
                break
        
        # If this row has a pivot column already used, skip it (redundant)
        if pivot_col >= 0 and pivot_col in used_pivots:
            continue
        
        if pivot_col >= 0:
            used_pivots.add(pivot_col)
        
        filtered_aug.append(row)
    
    # Extract U and c_part from filtered augmented matrix
    U = [row[:a_cols] for row in filtered_aug]
    c_part = [row[a_cols:] for row in filtered_aug]
    
    x = back_substitution(U, c_part) if (c_part and len(c_part[0]) > 0) else []
    
    return U, x, num_swaps

def print_matrix(mat):
    for row in mat:
        print(["{:.4f}".format(v) for v in row])


def gaussian_eliminate_formatter(U, x, num_swaps):
    
    # Print upper triangle matrix
    print("\nUpper Triangle Matrix U:")
    print("-" * 40)
    if U:
        for i, row in enumerate(U):
            row_str = "["
            for j, val in enumerate(row):
                if isinstance(val, float):
                    row_str += f"{val:10.4f}"
                else:
                    row_str += f"{str(val):>10}"
                if j < len(row) - 1:
                    row_str += ", "
            row_str += "]"
            print(row_str)
    else:
        print("Empty matrix")
    
    # Print solution vector
    print("\nSolution Vector x:")
    print("-" * 40)
    if x:
        for i, val in enumerate(x):
            if hasattr(val, 'mp'):  # Expression object
                print(f"x[{i}] = {val}")
            else:  # Float or other type
                print(f"x[{i}] = {val}")
    else:
        print("No solution")
    
    # Print number of swaps
    print(f"\nNumber of Row Swaps: {num_swaps}")
    print("=" * 60)


def main():
    A = [[1.0, 2.0, 3.0], [1.0, 2.0, 4.0], [1.0, 2.0, 4.0]]
    U, x, num_swaps = gaussian_eliminate(A, [1, 2, 2])
    gaussian_eliminate_formatter(U, x, num_swaps)
    
if __name__ == "__main__":
    main()
