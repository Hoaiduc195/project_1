import numpy as np

print("\n" + "="*50)
print("PHẦN: PHÂN RÃ CHOLESKY (CHOLESKY DECOMPOSITION)")
print("="*50)

def custom_cholesky(A):
    """
    Cài đặt thuật toán phân rã Cholesky cho ma trận đối xứng xác định dương.
    Định dạng: A = L * L^T  (với L là ma trận tam giác dưới)
    """
    n = A.shape[0]
    # Khởi tạo L toàn số 0
    L = np.zeros_like(A, dtype=float)
    
    for i in range(n):
        for j in range(i + 1):
            # Tính tổng phần bị trừ: sum(L_{i, k} * L_{j, k}) từ k=0 tới j-1
            sum_val = sum(L[i, k] * L[j, k] for k in range(j))
            
            if i == j: # Nếu đang xét đường chéo chính (i == j)
                val = A[i, i] - sum_val
                if val <= 0:
                    raise ValueError(f"Ma trận không phải là xác định dương tại i={i}!")
                L[i, j] = np.sqrt(val)
                
            else:      # Các phần tử dưới đường chéo chính (i > j)
                L[i, j] = (A[i, j] - sum_val) / L[j, j]
                
    return L

# 1. KHỞI TẠO DỮ LIỆU
# Thuật toán Cholesky yêu cầu ma trận phải 'Đối xứng' và 'Xác định dương' (Symmetric Positive Definite)
# Ta tạo ra nó bằng cách lấy B nhân B^T, cộng với đường chéo để đảm bảo xác định dương
B = np.array([[2, 1, 0], 
              [1, 3, 1], 
              [0, 1, 2]])
A_chol = B @ B.T 

print("Tạo ma trận đối xứng xác định dương A:\n", A_chol)

# 2. CHẠY HÀM TỰ CÀI ĐẶT
try:
    L_custom = custom_cholesky(A_chol)
    print("\n[Tự code] Ma trận tam giác dưới L:\n", L_custom)
    
    A_reconstructed_chol = L_custom @ L_custom.T
    print("\n[Tự code] Phục hồi A (L * L^T):\n", A_reconstructed_chol)

except ValueError as e:
    print("Lỗi tính toán Cholesky:", e)

# 3. KIỂM TRÁ BẰNG NUMPY
try:
    L_np = np.linalg.cholesky(A_chol)
    print("\n" + "-"*30)
    print("[NumPy] Ma trận tam giác dưới L:\n", L_np)
    
    # 4. KẾT LUẬN KIỂM CHỨNG
    is_correct = np.allclose(A_chol, A_reconstructed_chol)
    print("\nKết luận: L_custom * L_custom^T == A là", is_correct)
    
except np.linalg.LinAlgError:
    print("Mã lỗi NumPy: Ma trận không phải là Matrix Positive Definite.")
