import math
from part1 import gaussian, back_substitution
from part2 import decomposition as dc

# 1. Gaussian elimination solver
def solve_gaussian(A, b):
	_, x, _ = gaussian.gaussian_eliminate(A, b)
	return x

# 3. Gauss-Seidel iterative solver
def solve_gauss_seidel(A, b, x0=None, tol=1e-10, max_iters=1000, omega=0.7):
	if not A or not A[0]:
		raise ValueError("A must be a non-empty matrix")
	n = len(A)
	if any(len(row) != n for row in A):
		raise ValueError("Gauss-Seidel requires a square matrix A")
	if len(b) != n:
		raise ValueError("b must have the same number of rows as A")
	if not (0.0 < omega <= 1.0):
		raise ValueError("omega must satisfy 0 < omega <= 1")

	# Init solution vector
	if x0 is None:
		x = [0.0] * n
	else:
		if len(x0) != n:
			raise ValueError("x0 must have the same length as b")
		x = [float(v) for v in x0]

	for it in range(max_iters):
		x_old = list(x)

		for i in range(n):
			if abs(A[i][i]) < 1e-15:
				raise ValueError(f"Zero pivot detected at row {i}. Gauss-Seidel requires non-zero diagonal entries.")

			sigma = 0.0
			for j in range(i):
				sigma += A[i][j] * x[j]
			for j in range(i + 1, n):
				sigma += A[i][j] * x_old[j]

			gs_value = (b[i] - sigma) / A[i][i]
			x[i] = (1.0 - omega) * x_old[i] + omega * gs_value

			if not math.isfinite(x[i]):
				# raise OverflowError(
				# 	"Gauss-Seidel diverged (non-finite iterate). "
				# 	"Try a diagonally dominant matrix, lower omega, or a direct solver."
				# )
				return None  # Indicate failure to converge due to divergence

		# Infinity norm avoids squaring very large values.
		diff_inf = max(abs(x[i] - x_old[i]) for i in range(n))
		if diff_inf < tol:
			# print(f"Convergence achieved after {it + 1} iterations.")
			return x

		if diff_inf > 1e100:
			# raise OverflowError(
			# 	"Gauss-Seidel appears to diverge (update norm became extremely large). "
			# 	"Try a diagonally dominant matrix, lower omega, or a direct solver."
			# )
			return None  # Indicate failure to converge due to divergence

	print("Warning: No convergence after maximum iterations.")
	return x

# 2. SVD decomposition solver
def solve_svd(A, b):
	# 1. Normalize b to a column vector.
    if b is None: return None
    b_mat = [[float(val)] for val in (b if isinstance(b[0], (list, tuple)) else b)]
    m, n = len(A), len(A[0])

	# 2. Compute SVD.
    U, S, Vt = dc.do_svd_primitive(A)
    V = dc.transpose(Vt)
    
	# 3. Estimate numerical rank and filter tiny singular values.
    singular_values = dc.get_diag(S)
    max_s = max(singular_values) if singular_values else 0
    tol = max_s * n * 1e-12 
    
    actual_rank = 0
    for s in singular_values:
        if s > tol: actual_rank += 1
    actual_rank = min(actual_rank, m)

	# 4. Compute xp (minimum-norm particular solution).
    Ut = dc.transpose(U)
    Utb = dc.mat_mul(Ut, b_mat)
    y = dc.zeros(n, 1)
    for i in range(actual_rank):
        y[i][0] = Utb[i][0] / singular_values[i]
    
    xp = [row[0] for row in dc.mat_mul(V, y)]

	# 5. Build null-space basis and reduce it to RREF for cleaner parameters.
    null_basis = []
    for j in range(actual_rank, n):
        null_basis.append(dc.get_col(V, j))
    
    null_space_cleaned = rref(null_basis) if null_basis else []

    xp = [round(v, 10) for v in xp]
    for i in range(len(null_space_cleaned)):
        null_space_cleaned[i] = [round(v, 10) for v in null_space_cleaned[i]]

	# 6. Transform xp into a basic-form particular solution
	# by zeroing entries at null-space pivot positions.
    for basis_vec in null_space_cleaned:
		# Find pivot position (first value close to 1.0) in each basis vector.
        pivot_idx = -1
        for k in range(n):
            if abs(basis_vec[k] - 1.0) < 1e-9:
                pivot_idx = k
                break
        
        if pivot_idx != -1:
			# Eliminate xp at this pivot position.
            factor = xp[pivot_idx]
            for k in range(n):
                xp[k] = xp[k] - factor * basis_vec[k]

	# 7. Build final symbolic expressions.
    results = []
    for i in range(n):
		# Final rounding to clean residual floating-point noise.
        val_fixed = round(xp[i], 10)
        expr = back_substitution.Expression([val_fixed], [])
        
        for idx, basis_vec in enumerate(null_space_cleaned):
            coeff = round(basis_vec[i], 10)
            if abs(coeff) > 1e-9:
                expr = expr + back_substitution.Expression([coeff], [f"t{idx+1}"])
        results.append(expr)
        
    return results

def rref(B):
    if not B: return B
    res = [list(row) for row in B]
    rows, cols = len(res), len(res[0])
    pivot_row = 0
    for j in range(cols):
        if pivot_row >= rows: break
        max_idx = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(res[i][j]) > abs(res[max_idx][j]): max_idx = i
        if abs(res[max_idx][j]) < 1e-10: continue
        res[pivot_row], res[max_idx] = res[max_idx], res[pivot_row]
        lv = res[pivot_row][j]
        res[pivot_row] = [val / lv for val in res[pivot_row]]
        for i in range(rows):
            if i != pivot_row:
                factor = res[i][j]
                for k in range(j, cols): res[i][k] -= factor * res[pivot_row][k]
        pivot_row += 1
    return res

if __name__ == "__main__":
	import numpy as np
	A = np.random.rand(3, 3).tolist()
	b = np.random.rand(3).tolist()
	A = [[1, 1],[2,2]]
	b = [3, 6]
	print("Solving Ax = b using Gaussian elimination:")
	x = solve_gaussian(A, b)
	# print solution vector
	print("Solution Vector x (Gaussian elimination):")
	print("-" * 40)
	if x:
		for i, val in enumerate(x):
			print(f"x[{i}] = {val}")
	else:
		print("No solution")
	
	print("\nSolving Ax = b using SVD decomposition:")
	x_svd = solve_svd(A, b)
	print("Solution Vector x (SVD):")
	print("-" * 40)
	if x_svd:
		for i, val in enumerate(x_svd):
			print(f"x[{i}] = {val}")
	else:
		print("No solution or SVD solver failed to converge")

	print("\nSolving Ax = b using Gauss-Seidel iterative method:")
	x_gs = solve_gauss_seidel(A, b)
	print("Solution Vector x (Gauss-Seidel):")
	print("-" * 40)
	if x_gs:
		for i, val in enumerate(x_gs):
			print(f"x[{i}] = {val}")
	else:
		print("No solution or Gauss-Seidel solver failed to converge")

	def gauss_seidel(A, b, max_iter=1000, tol=1e-10):
		n = len(b)
		x = np.zeros(n)
		for _ in range(max_iter):
			x_old = x.copy()
			for i in range(n):
				sigma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
				x[i] = (b[i] - sigma) / A[i, i]
			
			if np.linalg.norm(x - x_old, ord=np.inf) < tol:
				break
		return x

	x_gs_numpy = gauss_seidel(np.array(A), np.array(b))
	print("\nSolution Vector x (Gauss-Seidel with NumPy):")
	print("-" * 40)
	if x_gs_numpy is not None:
		for i, val in enumerate(x_gs_numpy):
			print(f"x[{i}] = {val}")