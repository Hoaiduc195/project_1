import numpy as np

print("="*50)
print("PHẦN 2.1: CHÉO HÓA MA TRẬN")
print("="*50)

# Khởi tạo ma trận A
A = np.array([[4, 1], 
              [2, 3]])
print("Ma trận A ban đầu:\n", A)

# 1. Tính giá trị riêng (eigenvalues) và vector riêng (eigenvectors)
eigenvalues, eigenvectors = np.linalg.eig(A)

# 2. Xây dựng ma trận P, D và P^-1
P = eigenvectors
D = np.diag(eigenvalues)
P_inv = np.linalg.inv(P)

print("\nMa trận đường chéo D (Giá trị riêng):\n", D)
print("Ma trận P (Các vector riêng nằm trên các cột):\n", P)

# 3. Phục hồi ma trận (Chéo hóa)
A_reconstructed = P @ D @ P_inv
print("\nKiểm tra phương trình A = P * D * P^-1:\n", A_reconstructed)

# So sánh 2 ma trận với sai số nhỏ của máy tính
is_correct = np.allclose(A, A_reconstructed)
print("\nKết luận: Cài đặt chéo hóa chính xác?", is_correct)
