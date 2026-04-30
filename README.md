# Ứng dụng Giải Tích Ma Trận & Biểu Diễn Hình Ảnh

## 👤 Người thực hiện
- Họ tên: [Điền tên bạn tại đây]
- MSSV: [Điền MSSV]
- Email: [Điền email]

---

## 📖 Mô tả đồ án

Đồ án xây dựng các thuật toán giải hệ phương trình tuyến tính, phân tích ma trận (SVD, chéo hóa, ...), và trực quan hóa bằng Manim. Ứng dụng hỗ trợ kiểm chứng, benchmark hiệu năng, và sinh báo cáo tự động.

Các chức năng chính:
- Cài đặt các thuật toán cơ bản: khử Gauss, thế lùi, tính định thức, nghịch đảo, hạng và cơ sở.
- Phân tích ma trận: phân rã SVD, chéo hóa, các phép biến đổi ma trận.
- Trực quan hóa các thuật toán bằng hoạt hình Manim.
- Đánh giá hiệu năng, độ ổn định các thuật toán.
- Sinh báo cáo LaTeX tự động.

---

## 🗂️ Kiến trúc thư mục

```
.
├── part1/         # Thuật toán cơ bản: khử Gauss, thế lùi, định thức, nghịch đảo, hạng, cơ sở
│   ├── gaussian.py
│   ├── back_substitution.py
│   ├── determinant.py
│   ├── inverse.py
│   ├── rank_basis.py
│   ├── utils.py
│   └── part1_demo.ipynb
│
├── part2/         # Phân rã, chéo hóa, hoạt hình Manim, kiểm thử SVD
│   ├── decomposition.py
│   ├── diagonalization.py
│   ├── manim_scene.py
│   ├── manim_scripts.md
│   ├── test_SVD_and_diagonalization.py
│   └── media/
│       └── images/, Tex/, texts/, videos/
│
├── part3/         # Phân tích, benchmark, so sánh hiệu năng
│   ├── analysis.ipynb
│   ├── benchmark.py
│   └── solvers.py
│
├── report/        # Báo cáo LaTeX
│   ├── report.tex
│   └── report.pdf
│
├── skills/        # Bộ kỹ năng hỗ trợ Manim, review, học máy
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Techstack

- **Python 3.x**
- **Manim Community Edition**: trực quan hóa toán học
- **NumPy, Pandas, Matplotlib**: xử lý số liệu, vẽ biểu đồ
- **Jupyter Notebook**: kiểm thử, trình bày kết quả
- **LaTeX**: viết báo cáo

---

## 💡 Hướng dẫn sử dụng

1. **Cài đặt thư viện**  
	```
	pip install -r requirements.txt
	```

2. **Chạy notebook kiểm thử**  
	- part1: `part1/part1_demo.ipynb`
	- part3: `part3/analysis.ipynb`

3. **Biên dịch code Manim**  
	```
	# Compile tất cả các scene trong file manim_scene.py
	manim part2/manim_scene.py -ql -p
	# Hoặc chỉ compile một scene cụ thể (ví dụ SVDOverview)
	manim part2/manim_scene.py SVDOverview -ql -p
	```
	Lưu ý: yêu cầu file `img.png` để code có thể biên dịch

4. **Báo cáo**  
	- Biên dịch file `report/report.tex` bằng LaTeX.

---

## 🌟 Đóng góp & Liên hệ

- Đóng góp ý kiến, báo lỗi hoặc đề xuất tại [GitHub Issues](https://github.com/Hoaiduc195/project_1/issues)
- Liên hệ: [24120040@student.hcmus.edu.vn]

---
