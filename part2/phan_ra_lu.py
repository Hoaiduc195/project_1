import numpy as np
import scipy.linalg

print("\n" + "="*50)
print("PHẦN 2.2: PHÂN RÃ LU (LU DECOMPOSITION)")
print("="*50)

def custom_lu_decomposition(A):
    """Cài đặt phân rã LU sử dụng thuật toán Doolittle"""
    n = A.shape[0]
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    
    for i in range(n):
        # Tính các phần tử hàng thứ i của U
        for k in range(i, n):
            sum_val = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_val
            
        # Tính các phần tử cột thứ i của L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0  # Đường chéo chính của L luôn bằng 1
            else:
                sum_val = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (A[k][i] - sum_val) / U[i][i]
                
    return L, U

# Ma trận vuông mẫu
A_lu = np.array([[2, -1, -2], 
                 [-4, 6, 3], 
                 [-4, -2, 8]], dtype=float)

print("Ma trận A cần phân rã:\n", A_lu)

# 1. CHẠY HÀM TỰ CÀI ĐẶT
L_custom, U_custom = custom_lu_decomposition(A_lu)
print("\n[Tự code] Ma trận L:\n", L_custom)
print("\n[Tự code] Ma trận U:\n", U_custom)
print("\n[Tự code] Phục hồi A (L * U):\n", L_custom @ U_custom)

# 2. KIỂM TRÁ BẰNG THƯ VIỆN CHUẨN (SciPy/Numpy)
# Lưu ý: Thư viện chuẩn dùng ma trận hoán vị Pivot (P) nên phân rã có dạng A = P * L * U
P_scipy, L_scipy, U_scipy = scipy.linalg.lu(A_lu)

print("\n[Linalg] Kiểm chứng bằng SciPy.linalg.lu:")
print("Ma trận L (SciPy):\n", L_scipy)
print("Ma trận U (SciPy):\n", U_scipy)

# 3. KỂT LUẬN KIỂM CHỨNG
is_lu_correct = np.allclose(A_lu, L_custom @ U_custom)
print("\n[Trạng thái] L_custom * U_custom có chính xác bằng A không?", is_lu_correct)
