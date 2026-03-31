import numpy as np

print("\n" + "="*50)
print("PHẦN: PHÂN RÃ SVD (SINGULAR VALUE DECOMPOSITION)")
print("="*50)

def custom_svd(A):
    """
    Cài đặt thuật toán phân rã SVD cơ bản (A = U * Sigma * V^T)
    Dựa trên việc tìm giá trị riêng của A^T*A và A*A^T.
    Lưu ý: Cách tính này tốt cho việc mô phỏng lý thuyết, thực tế hàm của Numpy 
    sẽ sử dụng phân rã ngẫu nhiên / thuật toán Jacobi để ổn định số học hơn.
    """
    m, n = A.shape
    
    # 1. Tìm V và giá trị kỳ dị (Sigma) từ ma trận A^T * A
    AtA = A.T @ A
    eigenvalues_V, eigenvectors_V = np.linalg.eigh(AtA)
    
    # Sắp xếp giảm dần các giá trị riêng để lấy các kỳ dị trị (singular values)
    sorted_indices = np.argsort(eigenvalues_V)[::-1]
    eigenvalues_V = eigenvalues_V[sorted_indices]
    V = eigenvectors_V[:, sorted_indices]
    
    # Tính các giá trị kỳ dị (sigma = sqrt(lambda))
    singular_values = np.sqrt(np.maximum(eigenvalues_V, 0)) # maximum(..., 0) để triệt sai số âm siêu nhỏ
    
    # 2. Xây dựng ma trận đường chéo Sigma (kích thước m x n)
    Sigma = np.zeros((m, n))
    k = min(m, n)
    Sigma[:k, :k] = np.diag(singular_values[:k])
    
    # 3. Tìm U từ ma trận A * A^T
    AAt = A @ A.T
    eigenvalues_U, eigenvectors_U = np.linalg.eigh(AAt)
    
    # Sắp xếp giảm dần tương tự để mapping với Sigma
    sorted_indices_U = np.argsort(eigenvalues_U)[::-1]
    U = eigenvectors_U[:, sorted_indices_U]
    
    # 4. Hiệu chỉnh dấu của mảng U thông qua mối quan hệ A*V = U*Sigma
    # Vì vector riêng có thể ngược dấu (-1) nên phải chỉnh lại cho đồng bộ
    for i in range(k):
        if singular_values[i] > 1e-10: 
            # Vector dự kiến u_expected = (A * v_i) / sigma_i
            u_expected = (A @ V[:, i]) / singular_values[i]
            # Nếu vector bị ngược hướng, đổi dấu toàn bộ cột i của U
            if np.sign(u_expected[0]) != np.sign(U[0, i]) and u_expected[0] != 0:
                U[:, i] = -U[:, i]
                
    return U, Sigma, V.T

# Khởi tạo ma trận A tuỳ ý (không cần vuông)
A_svd = np.array([[3, 1, 1],
                  [-1, 3, 1]])

print("Ma trận A:\n", A_svd)

# 1. CHẠY HÀM TỰ CÀI ĐẶT
U_custom, Sigma_custom, Vt_custom = custom_svd(A_svd)
print("\n[Tự code] Ma trận trực giao U:\n", U_custom)
print("\n[Tự code] Ma trận kỳ dị trị Sigma:\n", Sigma_custom)
print("\n[Tự code] Ma trận trực giao V^T:\n", Vt_custom)

# Phục hồi
A_reconstructed_svd = U_custom @ Sigma_custom @ Vt_custom
print("\n[Tự code] Phục hồi A (U * Sigma * V^T):\n", A_reconstructed_svd)


# 2. KIỂM CHỨNG BẰNG NUMPY
U_np, s_np, Vt_np = np.linalg.svd(A_svd, full_matrices=True)

# Linalg.svd trả về mảng 1D s_np (chứa các sigma trên đường chéo)
# Ta chuyển nó thành ma trận m x n để có thể nhân 3 ma trận
Sigma_np = np.zeros((A_svd.shape[0], A_svd.shape[1]))
k = min(A_svd.shape[0], A_svd.shape[1])
Sigma_np[:k, :k] = np.diag(s_np)

print("\n" + "-"*30)
print("[NumPy] Ma trận U:\n", U_np)
print("[NumPy] Ma trận Sigma:\n", Sigma_np)
print("[NumPy] Ma trận V^T:\n", Vt_np)

# 3. KỂT LUẬN
is_correct = np.allclose(A_svd, A_reconstructed_svd)
print("\nKết luận: U_custom * Sigma_custom * Vt_custom == A là", is_correct)
