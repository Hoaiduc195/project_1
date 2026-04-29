from manim import *
from PIL import Image
import numpy as np

# Intro - Scene 1 - TONG QUAN VE SVD
class SVDOverview(Scene):
    def construct(self):
        title = MathTex(" S ", " V ", " D ", font_size=80)

        self.play(Write(title))
        self.wait()

        self.play(Write(title))
        self.play(title.animate.to_edge(UP, buff=2.0))
        self.wait()

        Title = Text("Singular Value Decomposition", font_size=36)
        box2 = SurroundingRectangle(
            Title,
            buff=0.4
        )
        Title.to_edge(UP, buff=2.0)
        self.play(Transform(title, Title))
        self.play(Create(box2.to_edge(UP, buff=1.6)))
        self.wait()

        rk2methods = ["Jordan decomposition", "Spectral decomposition", "QR decomposition"]
        methods = [
            "LU decomposition", "Cholesky decomposition", "Schur decomposition",
            "Polar decomposition", "Block LU decomposition", "Algebraic polar decomposition",
            "Mostow's decomposition", "Real Schur decomposition", "Interpolative decomposition"
        ]
        texts = VGroup(*[Text(m, font_size=28) for m in rk2methods])
        texts.arrange(RIGHT, buff=0.4)
        boxes = VGroup(*[
            SurroundingRectangle(text, color=BLUE, buff=0.1)
            for text in texts
        ]).next_to(Title, DOWN, buff=0.9)
        text_group2 = VGroup(*[Text(m) for m in methods]).scale(0.3).arrange_in_grid(rows=3, cols=3)

        texts.next_to(Title, DOWN, buff=1.0)
        text_group2.next_to(Title, DOWN, buff=2.0)
        self.play(Write(texts))
        self.play(Create(boxes))
        self.play(Write(text_group2))
        self.wait(10)

# Scene 2 - Problem Definition
class SVDProblemDefinition(ThreeDScene):
    def construct(self):
        # 0. Thiết lập Camera ban đầu
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        # CÁC PHẦN TỬ CỐ ĐỊNH XUYÊN SUỐT (Góc trái / Trên cùng)
        tex_label = Text("ĐẶT VẤN ĐỀ", font="Times New Roman", font_size=15, color=GREY).to_corner(UL, buff=0.25)
        self.add_fixed_in_frame_mobjects(tex_label)
        
        title = Text("Có cách nào phân tách một ma trận biến đổi phức tạp?", font="Times New Roman", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        self.play(Write(tex_label), Write(title))

        # ===== Khởi tạo dữ liệu Toán học =====
        A_matrix = np.array([
            [1.5, 0.5, 0.0],
            [0.0, 1.0, 1.0],
            [0.5, 0.0, 1.0]
        ])
        U_mat, S_values, VT_mat = np.linalg.svd(A_matrix)
        Sigma_mat = np.diag(S_values)

        # =================================================================
        # SCENE 1: CHỈ HIỆN CHỮ (Giới thiệu ma trận A)
        # =================================================================
        A_tex = MathTex(r"A = \begin{bmatrix} 1.5 & 0.5 & 0 \\ 0 & 1 & 1 \\ 0.5 & 0 & 1 \end{bmatrix}")
        self.add_fixed_in_frame_mobjects(A_tex)
        self.play(Write(A_tex))
        self.wait(1.5)
        
        # Ẩn chữ đi để chuẩn bị nhường chỗ cho khối 3D
        self.play(FadeOut(A_tex))

        # =================================================================
        # SCENE 2: CHỈ HIỆN 3D (Minh hoạ biến đổi bởi A)
        # =================================================================
        axes = ThreeDAxes()
        sphere = Sphere(radius=1.5, resolution=(20, 20))
        sphere.set_style(fill_opacity=0.2, fill_color=BLUE, stroke_width=0.5, stroke_color=BLUE_A)
        cube_wireframe = Cube(side_length=3, fill_opacity=0, stroke_width=1, stroke_color=GREY)
        
        moving_space = VGroup(sphere, cube_wireframe)

        # Nhãn nhỏ ở dưới cùng, không che mất hình
        label_direct = Text("Áp dụng trực tiếp ma trận A", font="Times New Roman", font_size=24).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(label_direct)

        self.play(Create(axes), Create(moving_space), FadeIn(label_direct))
        self.wait(0.5)

        # Hoạt ảnh biến đổi 3D
        self.play(ApplyMatrix(A_matrix, moving_space), run_time=2.5)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)
        self.stop_ambient_camera_rotation()

        # Dọn dẹp không gian 3D để quay lại phần lý thuyết
        self.play(FadeOut(axes), FadeOut(moving_space), FadeOut(label_direct))
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES) # Reset góc camera

        # =================================================================
        # SCENE 3: CHỈ HIỆN CHỮ (Công thức SVD thu nhỏ)
        # =================================================================
        svd_formula = MathTex(r"A = U \Sigma V^T")
        self.add_fixed_in_frame_mobjects(svd_formula)
        self.play(Write(svd_formula))

        # Hàm chuyển ma trận sang Tex
        def mat_to_tex(mat):
            rows = []
            for row in mat:
                rows.append(" & ".join([f"{val:.2f}" for val in row]))
            return r"\begin{bmatrix} " + r" \\ ".join(rows) + r" \end{bmatrix}"

        U_tex_part = mat_to_tex(U_mat)
        S_tex_part = mat_to_tex(Sigma_mat)
        VT_tex_part = mat_to_tex(VT_mat)

        # THU NHỎ MA TRẬN BẰNG .scale(0.55) ĐỂ KHÔNG BỊ TRÀN
        svd_matrices = MathTex(
            r"=", U_tex_part, S_tex_part, VT_tex_part
        ).scale(0.55).next_to(svd_formula, DOWN, buff=0.5)
        
        labels_svd = VGroup(
            Text("(Xoay)", font_size=16, color=YELLOW),
            Text("(Co giãn)", font_size=16, color=YELLOW),
            Text("(Xoay)", font_size=16, color=YELLOW)
        ).arrange(RIGHT, buff=2).next_to(svd_matrices, DOWN, buff=0.2)

        self.add_fixed_in_frame_mobjects(svd_matrices, labels_svd)
        self.play(Write(svd_matrices), Write(labels_svd))
        self.wait(3)

        # Ẩn toàn bộ công thức SVD đi để lấy lại không gian
        self.play(FadeOut(svd_formula), FadeOut(svd_matrices), FadeOut(labels_svd))

        # =================================================================
        # SCENE 4: CHỈ HIỆN 3D (Từng bước SVD)
        # =================================================================
        # Reset lại không gian 3D ban đầu
        axes_2 = ThreeDAxes()
        sphere_2 = Sphere(radius=1.5, resolution=(20, 20))
        sphere_2.set_style(fill_opacity=0.2, fill_color=BLUE, stroke_width=0.5, stroke_color=BLUE_A)
        cube_wireframe_2 = Cube(side_length=3, fill_opacity=0, stroke_width=1, stroke_color=GREY)
        moving_space_2 = VGroup(sphere_2, cube_wireframe_2)

        step_label = Text("1. Xoay hệ trục đầu vào ($V^T$)", font="Times New Roman", font_size=24, t2c={'$V^T$': YELLOW}).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(step_label)

        self.play(Create(axes_2), Create(moving_space_2), FadeIn(step_label))
        self.wait(0.5)

        # BƯỚC 1: Xoay (V^T)
        self.play(ApplyMatrix(VT_mat, moving_space_2), run_time=2)
        self.wait(1)

        # BƯỚC 2: Co giãn (Sigma)
        step2_text = Text("2. Co giãn theo trục ($\Sigma$)", font="Times New Roman", font_size=24, t2c={'$\Sigma$': YELLOW}).to_edge(DOWN)
        self.play(Transform(step_label, step2_text))
        self.play(ApplyMatrix(Sigma_mat, moving_space_2), run_time=2)
        
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

        # BƯỚC 3: Xoay (U)
        step3_text = Text("3. Xoay kết quả đầu ra ($U$)", font="Times New Roman", font_size=24, t2c={'$U$': YELLOW}).to_edge(DOWN)
        self.play(Transform(step_label, step3_text))
        self.play(ApplyMatrix(U_mat, moving_space_2), run_time=2)
        self.wait(1)

        # Kết luận
        final_text = Text("SVD = Xoay → Co giãn → Xoay", font="Times New Roman", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Transform(step_label, final_text))
        
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()        
        
# Scene 3 - SVD Advantage
class SVDAdvan(Scene):
    def construct(self):
        # corner
        tex = Text("ĐIỂM MẠNH CỦA SVD", font="Times New Roman", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        self.wait(2)
        
         # Title
        title = Text("Mọi ma trận có thể phân rã với phương pháp SVD", font="Times New Roman", font_size=36)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP, buff=1.0))

        # ===== CASE 1: vuông =====
        expr1 = MathTex(
            r"A = U \Sigma V^T = "
            r"\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}"
            r"\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}"
            r"\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}"
        )
        expr1.next_to(title, DOWN, buff=2)

        desc1 = Text("Ma trận vuông", font="Times New Roman", font_size=20)
        desc1.next_to(expr1, DOWN, buff=1.3)

        self.play(Write(expr1), Write(desc1))
        self.wait(2)

        # ===== CASE 2: m > n =====
        expr2 = MathTex(
            r"A = U \Sigma V^T = "
            r"\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 1\end{bmatrix}"
            r"\begin{bmatrix}3 & 0\\0 & 2\\0 & 0\end{bmatrix}"
            r"\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}"
        )
        expr2.move_to(expr1)

        desc2 = Text("Ma trận không vuông", font="Times New Roman", font_size=20)
        desc2.move_to(desc1)

        self.play(
            Transform(expr1, expr2),
            Transform(desc1, desc2)
        )
        self.wait(2)

        # ===== CASE 3: m < n =====
        expr3 = MathTex(
            r"A = U \Sigma V^T = "
            r"\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}"
            r"\begin{bmatrix}3 & 0 & 0\\0 & 2 & 0\end{bmatrix}"
            r"\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 1\end{bmatrix}"
        )
        expr3.move_to(expr1)

        desc3 = Text("Ma trận không vuông", font="Times New Roman", font_size=20)
        desc3.move_to(desc1)

        self.play(
            Transform(expr1, expr3),
            Transform(desc1, desc3)
        )
        self.wait(2)

# Scene 4 - Prerequisities
class SVDConceptFlow(Scene):
    def construct(self):
        def get_label(text_str):
            return Text(text_str, font="Times New Roman", font_size=24).to_edge(DOWN, buff=0.5)

        # =========================================================
        # 0. MỞ ĐẦU (Đọc kịch bản: ~7 giây)
        # =========================================================
        title = Text("CÁC KIẾN THỨC CẦN THIẾT", font="Times New Roman", font_size=15, color=GREY)
        self.play(Write(title))
        self.play(title.animate.to_corner(UL, buff=0.5))

        plane = NumberPlane()
        self.play(Create(plane), run_time=1.5)
        self.wait(3) # Chờ kết thúc câu mở đầu

        # =========================================================
        # 1. KHÔNG GIAN VECTOR (Đọc: ~8 giây)
        # =========================================================
        v1 = Vector([2, 1], color=BLUE)
        v2 = Vector([1, 2], color=GREEN)

        label = get_label("1. Không gian vector & Bao tuyến tính")
        self.play(Write(label), GrowArrow(v1), GrowArrow(v2))
        self.wait(6) # Cho người xem ngấm kiến thức và khớp giọng đọc

        # =========================================================
        # 2. TRỰC GIAO (Đọc: ~7 giây)
        # =========================================================
        v1_ortho = Vector([2, 0], color=BLUE)
        v2_ortho = Vector([0, 2], color=GREEN)

        new_label = get_label("2. Trực giao (Tích vô hướng = 0)")

        self.play(
            Transform(v1, v1_ortho),
            Transform(v2, v2_ortho),
            Transform(label, new_label),
            run_time=1
        )
        right_angle = RightAngle(v1, v2, length=0.3, color=YELLOW)
        self.play(Create(right_angle))
        
        self.wait(5) # Khớp giọng đọc

        # =========================================================
        # 3. MA TRẬN TRỰC GIAO (Đọc: ~12 giây)
        # =========================================================
        new_label = get_label("3. Ma trận trực giao: Xoay / Phản xạ (bảo toàn độ dài & góc)")
        ortho_group = VGroup(v1, v2, right_angle)

        self.play(Transform(label, new_label))
        self.play(ortho_group.animate.rotate(PI / 4, about_point=ORIGIN), run_time=1.5)
        self.wait(3) # "Điều tuyệt vời là nó luôn bảo toàn hình dáng..."
        self.play(ortho_group.animate.rotate(-PI / 4, about_point=ORIGIN), run_time=1.5)
        self.wait(3)
        
        self.play(FadeOut(ortho_group))

        # =========================================================
        # 4. VECTOR RIÊNG (Đọc: ~12 giây)
        # =========================================================
        new_label = get_label("4. Vector riêng: Giữ nguyên hướng khi bị biến đổi")
        eigen_vec = Vector([2, 1], color=RED)
        eigen_span = Line(ORIGIN, [6, 3, 0], color=GRAY).set_opacity(0.5)

        self.play(Transform(label, new_label))
        self.play(Create(eigen_span), GrowArrow(eigen_vec))
        self.wait(3) # "Hầu hết các vector đều bị lệch hướng..."

        # Biến đổi: Chỉ co giãn, không đổi hướng
        scaled_eigen = Vector([4, 2], color=RED)
        self.play(Transform(eigen_vec, scaled_eigen), run_time=1.5)
        self.wait(5) # "...Nhưng vector riêng thì khác"

        self.play(FadeOut(eigen_vec, eigen_span))

        # =========================================================
        # 5. XOAY HỆ TỌA ĐỘ (Đọc: ~8 giây)
        # =========================================================
        new_label = get_label("5. Xoay hệ tọa độ (Thay đổi cơ sở)")
        self.play(Transform(label, new_label))

        self.play(plane.animate.rotate(PI / 6, about_point=ORIGIN), run_time=1.5)
        self.wait(2)
        self.play(plane.animate.rotate(-PI / 6, about_point=ORIGIN), run_time=1.5)
        self.wait(2)

        # =========================================================
        # 6. HẠNG - RANK (Đọc: ~12 giây)
        # =========================================================
        new_label = get_label("6. Hạng (Rank): Số chiều của không gian sau biến đổi")
        square = Square(side_length=2, color=BLUE).set_fill(BLUE, opacity=0.3).move_to([1, 1, 0])
        
        self.play(Transform(label, new_label), Create(square))
        self.wait(2)

        collapse_matrix = [[1, 1], [1, 1]]
        self.play(square.animate.apply_matrix(collapse_matrix), run_time=2)
        self.wait(5) # "ép xẹp toàn bộ mặt phẳng 2D thành 1D..."
        
        self.play(FadeOut(square))

        # =========================================================
        # 7. PHÉP CHIẾU (Đọc: ~10 giây)
        # =========================================================
        new_label = get_label("7. Phép chiếu trực giao lên không gian con")
        vec = Vector([2, 2], color=BLUE)
        axis = Line([-1, 0, 0], [4, 0, 0], color=WHITE)
        proj = Vector([2, 0], color=GREEN)
        dashed_line = DashedLine(vec.get_end(), proj.get_end(), color=YELLOW)

        self.play(Transform(label, new_label))
        self.play(Create(axis), GrowArrow(vec))
        self.wait(2) # "Tưởng tượng bạn rọi một ánh đèn..."
        self.play(Create(dashed_line))
        self.play(GrowArrow(proj))
        
        self.wait(4)
        self.play(FadeOut(VGroup(vec, axis, proj, dashed_line, plane)))

        # =========================================================
        # 8. MA TRẬN PSD (Đọc: ~12 giây)
        # =========================================================
        new_label = get_label("8. Ma trận đối xứng bán xác định dương")
        psd_text = MathTex(r"x^T (A^T A) x = \|Ax\|^2 \ge 0", font_size=48)

        self.play(Transform(label, new_label), Write(psd_text))
        self.wait(9) # Đọc câu thoại về PSD

        self.play(FadeOut(psd_text))

        # =========================================================
        # 9. KẾT NỐI SVD (Đọc: ~12 giây)
        # =========================================================
        flow = Text("Tất cả hội tụ lại thành phân rã SVD", font="Times New Roman", font_size=36, color=YELLOW)
        final_formula = MathTex(r"A = U \Sigma V^T", font_size=60)
        final_label = get_label("SVD = Xoay → Co giãn → Xoay")

        flow.to_edge(UP, buff=1.5)
        final_formula.next_to(flow, DOWN, buff=1)

        self.play(Transform(label, final_label))
        self.play(Write(flow))
        self.play(Write(final_formula))

        # Để dư thời gian đoạn cuối cho người xem nhìn lại công thức
        self.wait(8)

# Scene 5 - Diagonalization instruction
class Diagonalization(Scene):
    def construct(self):
        # Đặt text ở góc trên bên trái (UL)
        title = Text("CHÉO HOÁ MA TRẬN", font_size=15, color=GREY).to_corner(UL, buff=0.25)
        self.play(Write(title))

        # --- PHẦN MỞ ĐẦU: Giới thiệu ma trận A ---
        A_mat = MathTex(r"A = \begin{bmatrix} 1 & 1 & 1 \\ 0 & 2 & 1 \\ 0 & 0 & 3 \end{bmatrix}")
        self.play(FadeIn(A_mat))
        self.wait(1)
        
        # Di chuyển ma trận A sang góc trên bên phải (UR) để làm không gian tham chiếu
        self.play(A_mat.animate.to_corner(UR, buff=0.25).scale(0.8))

        # --- BƯỚC 1: TÌM TRỊ RIÊNG ---
        step1_title = Text("Bước 1: Giải phương trình đặc trưng tìm trị riêng", font_size=24, color=YELLOW)
        step1_title.next_to(title, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(step1_title))

        char_eq1 = MathTex(r"\det(A - \lambda I) = 0")
        char_eq2 = MathTex(r"(1-\lambda)(2-\lambda)(3-\lambda) = 0")
        eigenvalues = MathTex(r"\Rightarrow \lambda_1 = 1,\ \lambda_2 = 2,\ \lambda_3 = 3")

        step1_group = VGroup(char_eq1, char_eq2, eigenvalues).arrange(DOWN, buff=0.4).scale(0.8)
        step1_group.next_to(step1_title, DOWN, buff=0.8).set_x(0)

        self.play(Write(char_eq1))
        self.wait(0.5)
        self.play(TransformFromCopy(char_eq1, char_eq2))
        self.wait(0.5)
        self.play(Write(eigenvalues))
        self.wait(2)

        self.play(FadeOut(step1_group), FadeOut(step1_title))

        # --- BƯỚC 2: TÌM CƠ SỞ KHÔNG GIAN RIÊNG CHUYÊN SÂU ---
        step2_title = Text("Bước 2: Giải (A - λI)x = 0 tìm nghiệm tổng quát & cơ sở", font_size=24, color=YELLOW)
        step2_title.move_to(step1_title, aligned_edge=LEFT)
        self.play(Write(step2_title))

        # Nhóm lưu trữ kết quả ở dưới cùng màn hình
        step2_final_group = VGroup(
            MathTex(r"v_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}"),
            MathTex(r"v_2 = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}"),
            MathTex(r"v_3 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}")
        ).arrange(RIGHT, buff=1.2).scale(0.7).to_edge(DOWN, buff=0.5)

        # --- Giải chi tiết cho từng Lambda ---
        for i, (l_val, v_mat_str, sys_str, sol_str) in enumerate([
            (1, r"\begin{bmatrix} 0 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 2 \end{bmatrix}", r"\begin{cases} x_2 + x_3 = 0 \\ 2x_3 = 0 \end{cases}", r"t \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}"),
            (2, r"\begin{bmatrix} -1 & 1 & 1 \\ 0 & 0 & 1 \\ 0 & 0 & 1 \end{bmatrix}", r"\begin{cases} -x_1 + x_2 + x_3 = 0 \\ x_3 = 0 \end{cases}", r"t \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}"),
            (3, r"\begin{bmatrix} -2 & 1 & 1 \\ 0 & -1 & 1 \\ 0 & 0 & 0 \end{bmatrix}", r"\begin{cases} -2x_1 + x_2 + x_3 = 0 \\ -x_2 + x_3 = 0 \end{cases}", r"t \begin{bmatrix} t \\ t \\ t \end{bmatrix} = t \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}")
        ]):
            # Dùng ngoặc nhọn kép {{ }} cho các lệnh LaTeX trong f-string
            l_title = MathTex(fr"\lambda_{{{i+1}}} = {l_val} \Rightarrow (A - {l_val}I)x = 0").scale(0.8).next_to(step2_title, DOWN, buff=0.4, aligned_edge=LEFT)
            l_step1 = MathTex(fr"{v_mat_str} \begin{{bmatrix}} x_1 \\ x_2 \\ x_3 \end{{bmatrix}} = \begin{{bmatrix}} 0 \\ 0 \\ 0 \end{{bmatrix}} \Rightarrow {sys_str}").scale(0.7)
            
            l_step2_txt = Text("Nghiệm tổng quát: ", font_size=20)
            l_step2_math = MathTex(fr"x = {sol_str}").scale(0.7)
            l_step2 = VGroup(l_step2_txt, l_step2_math).arrange(RIGHT, buff=0.2)
            
            l_display = VGroup(l_step1, l_step2).arrange(DOWN, buff=0.4).next_to(l_title, DOWN, buff=0.4).set_x(0)
            
            self.play(Write(l_title))
            self.play(Write(l_step1))
            self.wait(0.5)
            self.play(Write(l_step2))
            self.wait(1)
            self.play(TransformFromCopy(l_step2_math, step2_final_group[i]))
            self.play(FadeOut(l_title), FadeOut(l_display))

        # Dời bộ 3 vectơ cơ sở lên phía trên
        self.play(step2_final_group.animate.next_to(step2_title, DOWN, buff=0.5).set_x(0))
        self.wait(0.5)

        # --- BƯỚC 3: XÂY DỰNG P, D VÀ P^-1 ---
        step3_title = Text("Bước 3: Xây dựng P, D và tính P nghịch đảo", font_size=24, color=YELLOW)
        step3_title.move_to(step2_title, aligned_edge=LEFT)
        self.play(FadeOut(step2_title), Write(step3_title))

        # 3.1 Xây dựng P
        P_mat = MathTex(
            r"P = [v_1 \quad v_2 \quad v_3] = ", 
            r"\begin{bmatrix} 1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{bmatrix}"
        ).scale(0.8).next_to(step2_final_group, DOWN, buff=0.6)
        
        self.play(Write(P_mat[0]))
        self.play(TransformFromCopy(step2_final_group, P_mat[1]))
        self.wait(1)

        # Xóa các vector v1, v2, v3 để dọn dẹp không gian, sau đó đẩy P_mat lên
        self.play(FadeOut(step2_final_group))
        self.play(P_mat.animate.next_to(step3_title, DOWN, buff=0.5).set_x(0))

        # 3.2 Xây dựng D (Thêm bước trung gian chứa lambda)
        D_sym = MathTex(
            r"D = \begin{bmatrix} \lambda_1 & 0 & 0 \\ 0 & \lambda_2 & 0 \\ 0 & 0 & \lambda_3 \end{bmatrix}",
        ).scale(0.8)
        
        D_val = MathTex(
            r"= \begin{bmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{bmatrix}"
        ).scale(0.8)

        D_group = VGroup(D_sym, D_val).arrange(RIGHT, buff=0.2).next_to(P_mat, DOWN, buff=0.5)

        self.play(Write(D_sym))
        self.wait(0.5)
        self.play(Write(D_val))
        self.wait(1)

        # 3.3 Tính P nghịch đảo
        P_inv_txt = Text("Tìm ma trận nghịch đảo: ", font_size=20)
        P_inv_math = MathTex(r"P^{-1} = \begin{bmatrix} 1 & -1 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1 \end{bmatrix}").scale(0.8)
        P_inv_group = VGroup(P_inv_txt, P_inv_math).arrange(RIGHT, buff=0.2).next_to(D_group, DOWN, buff=0.5)
        
        self.play(Write(P_inv_group))
        self.wait(2)

        # --- TỔNG KẾT ---
        self.play(
            FadeOut(P_mat), FadeOut(D_group), FadeOut(P_inv_group), 
            FadeOut(step3_title), FadeOut(A_mat)
        )

        final_title = Text("Kết luận", font_size=28, color=YELLOW).to_edge(UP, buff=1)
        self.play(Write(final_title))

        # Hiển thị phương trình tổng quát
        final_eq1 = MathTex(r"A = P D P^{-1}").scale(1.2)
        
        # Hiển thị 3 ma trận nhân với nhau
        final_eq2 = MathTex(
            r"= \begin{bmatrix} 1 & 1 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{bmatrix}",
            r"\begin{bmatrix} 1 & -1 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1 \end{bmatrix}"
        ).scale(0.9)
        
        # Hiển thị kết quả cuối cùng khớp với ma trận A
        final_eq3 = MathTex(
            r"= \begin{bmatrix} 1 & 1 & 1 \\ 0 & 2 & 1 \\ 0 & 0 & 3 \end{bmatrix}"
        ).scale(1.2)
        
        final_group = VGroup(final_eq1, final_eq2, final_eq3).arrange(DOWN, buff=0.6).next_to(final_title, DOWN, buff=0.5)
        
        self.play(Write(final_eq1))
        self.wait(1)
        self.play(Write(final_eq2))
        self.wait(1)
        self.play(Write(final_eq3))
        
        # Highlight kết quả cuối cùng để nhấn mạnh
        self.play(SurroundingRectangle(final_eq3, color=GREEN, buff=0.2).animate)
        self.wait(3)
                                                
# Scene 6 - SVD instruction
class ComputeSVD(Scene):
    def construct(self):
        # ===== Tiêu đề =====
        tex = Text("TÍNH TOÁN SVD", font="Times New Roman", font_size=15, color=GRAY)
        tex.to_corner(UL, buff=0.5)
        self.play(Write(tex))

        # ===== 1. Khởi tạo công thức gốc =====
        expr = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=60)
        
        # Đặt màu chuẩn để người xem dễ bám sát
        expr[2].set_color(BLUE)    # U
        expr[3].set_color(YELLOW)  # Sigma
        expr[4].set_color(GREEN)   # V^T

        self.play(Write(expr))
        self.wait(1)
        self.play(expr.animate.to_edge(UP, buff=1.5))

        # Khai báo lại các thành phần để trỏ Arrow
        A, eq, U, Sigma, VT = expr

        # Label cho từng ma trận (Đã được tản ra 2 bên và căn chỉnh khoảng cách)
        label_U = Text("Trực giao", font="Times New Roman", font_size=24).next_to(U, DOWN, buff=1.5).shift(LEFT * 1.5)
        label_S = Text("Chéo chữ nhật", font="Times New Roman", font_size=24).next_to(Sigma, DOWN, buff=2)
        label_V = Text("Trực giao", font="Times New Roman", font_size=24).next_to(VT, DOWN, buff=1.5).shift(RIGHT * 1.5)

        # Mũi tên tự động nối nghiêng
        arrow_U = Arrow(label_U.get_top(), U.get_bottom(), buff=0.1, color=BLUE)
        arrow_S = Arrow(label_S.get_top(), Sigma.get_bottom(), buff=0.1, color=YELLOW)
        arrow_V = Arrow(label_V.get_top(), VT.get_bottom(), buff=0.1, color=GREEN)

        self.play(FadeIn(label_S), Create(arrow_S))
        self.wait(1)
        self.play(FadeIn(label_U, label_V), Create(arrow_U), Create(arrow_V))
        self.wait(2)

        self.play(FadeOut(VGroup(label_U, label_S, label_V, arrow_U, arrow_S, arrow_V)))

        # ===== 2. Minh họa ma trận Sigma và A =====
        # Sử dụng dạng MobjectTable cho gọn và chuẩn thay vì tạo vòng lặp Dot thủ công
        grid_S = MobjectTable(
            [[Dot(radius=0.05, color=YELLOW) for _ in range(3)] for _ in range(2)],
            include_outer_lines=True
        ).scale(0.5)
        
        grid_A = MobjectTable(
            [[Dot(radius=0.05, color=WHITE) for _ in range(3)] for _ in range(2)],
            include_outer_lines=True
        ).scale(0.5)

        # Định dạng bracket
        matrix_Sigma = VGroup(MathTex(r"\left[", font_size=80), grid_S, MathTex(r"\right]", font_size=80)).arrange(RIGHT, buff=0.1)
        matrix_A = VGroup(MathTex(r"\left[", font_size=80), grid_A, MathTex(r"\right]", font_size=80)).arrange(RIGHT, buff=0.1)

        # Đẩy 2 ma trận lên trên một chút (chỉ shift DOWN * 0.5 thay vì 1) để lấy chỗ phía dưới
        matrices_group = VGroup(matrix_A, matrix_Sigma).arrange(RIGHT, buff=2).shift(DOWN * 0.5)
        
        size_text_A = Text("2 x 3", font="Times New Roman", font_size=20).next_to(matrix_A, DOWN)
        size_text_S = Text("2 x 3", font="Times New Roman", font_size=20).next_to(matrix_Sigma, DOWN)
        
        # SỬA LỖI Ở ĐÂY: Dời eq_condition xuống phía dưới cụm ma trận và căn giữa
        eq_condition = MathTex(r"\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_k \ge 0", font_size=36)
        eq_condition.next_to(matrices_group, DOWN, buff=1.2).set_x(0)
        self.wait(2)
        
        # Animation nối Sigma và A xuống mô hình lưới
        arrow_from_A = Arrow(A.get_bottom(), matrix_A.get_top(), color=WHITE)
        arrow_from_S = Arrow(Sigma.get_bottom(), matrix_Sigma.get_top(), color=YELLOW)

        self.play(Create(arrow_from_A), Create(arrow_from_S))
        self.play(FadeIn(matrix_A), FadeIn(matrix_Sigma))
        self.play(Write(size_text_A), Write(size_text_S))
        self.wait(0.5)
        
        # Hiện điều kiện các sigma một cách riêng biệt cho dễ theo dõi
        self.play(Write(eq_condition))
        self.wait(3)

        self.play(FadeOut(VGroup(arrow_from_A, arrow_from_S, matrix_A, matrix_Sigma, size_text_A, size_text_S, eq_condition)))

        # ===== 3. Chứng minh A^T A (Tìm V và Sigma) =====
        self.play(expr.animate.move_to(ORIGIN))
        self.wait(1)

        # Sử dụng TransformMatchingTex để tự động map các biến giống nhau
        step1 = MathTex("A^T A", "=", "(", "U", r"\Sigma", "V^T", ")^T", "(", "U", r"\Sigma", "V^T", ")", font_size=48)
        step1.set_color_by_tex("U", BLUE).set_color_by_tex(r"\Sigma", YELLOW).set_color_by_tex("V^T", GREEN)
        
        self.play(ReplacementTransform(expr, step1))
        self.wait(1.5)

        step2 = MathTex("A^T A", "=", "V", r"\Sigma^T", "U^T", "U", r"\Sigma", "V^T", font_size=48)
        step2.set_color_by_tex("U", BLUE).set_color_by_tex("U^T", BLUE).set_color_by_tex(r"\Sigma", YELLOW).set_color_by_tex("V", GREEN).set_color_by_tex("V^T", GREEN)
        
        self.play(TransformMatchingTex(step1, step2))
        self.wait(1.5)

        # Ghi chú U^T U = I
        note_I = MathTex("U^T U = I", font_size=36, color=GRAY).next_to(step2, UP)
        self.play(Write(note_I))
        self.wait(1)

        step3 = MathTex("A^T A", "=", "V", r"(\Sigma^T \Sigma)", "V^T", font_size=48)
        step3.set_color_by_tex(r"\Sigma", YELLOW).set_color_by_tex("V", GREEN).set_color_by_tex("V^T", GREEN)
        
        self.play(TransformMatchingTex(step2, step3), FadeOut(note_I))
        self.wait(1.5)

        self.play(step3.animate.to_edge(UP, buff=1.5))

        # So sánh với Eigendecomposition
        eig_eq = MathTex("A^T A", "=", "P", "D", "P^T", font_size=48)
        eig_eq.next_to(step3, DOWN, buff=1.5)
        
        arrow_V_P = DoubleArrow(step3[2].get_bottom(), eig_eq[2].get_top(), buff=0.1, color=GREEN)
        arrow_S_D = DoubleArrow(step3[3].get_bottom(), eig_eq[3].get_top(), buff=0.1, color=YELLOW)

        self.play(Write(eig_eq))
        self.play(Create(arrow_V_P), Create(arrow_S_D))
        self.wait(3)

        self.play(FadeOut(VGroup(step3, eig_eq, arrow_V_P, arrow_S_D)))

        # ===== 4. Tính toán Sigma (D) =====
        identity = MathTex(r"\Sigma^T \Sigma = D", font_size=48).to_edge(UP, buff=1.5)
        self.play(Write(identity))

        sigma_matrix = MathTex(
            r"\begin{bmatrix} \sigma_1^2 & 0 & 0 \\ 0 & \sigma_2^2 & 0 \\ 0 & 0 & \cdots \end{bmatrix}",
            font_size=40
        )
        lambda_matrix = MathTex(
            r"= \begin{bmatrix} \lambda_1 & 0 & 0 \\ 0 & \lambda_2 & 0 \\ 0 & 0 & \cdots \end{bmatrix}",
            font_size=40
        )

        matrix_group = VGroup(sigma_matrix, lambda_matrix).arrange(RIGHT, buff=0.5)
        
        self.play(Write(sigma_matrix))
        self.play(Write(lambda_matrix))
        self.wait(3)

        self.play(FadeOut(VGroup(identity, matrix_group)))

        # ===== 5. Tìm U =====
        title_U = Text("Tìm U", font="Times New Roman", font_size=32, color=BLUE).to_edge(UP, buff=1.0)
        self.play(Write(title_U))

        u_step1 = MathTex(r"A V = U \Sigma \implies U = A V \Sigma^{-1}", font_size=48)
        self.play(Write(u_step1))
        self.wait(2)

        u_step2 = MathTex(r"u_i = \frac{1}{\sigma_i} A v_i", font_size=48)
        self.play(ReplacementTransform(u_step1, u_step2))
        self.wait(2)

        u_step3 = MathTex(r"u_i = \frac{A v_i}{\|A v_i\|}", font_size=48)
        self.play(ReplacementTransform(u_step2, u_step3))
        self.wait(2)

        u_step4 = MathTex(r"U = [u_1 \; u_2 \; \cdots \; u_k]", font_size=48)
        self.play(ReplacementTransform(u_step3, u_step4))
        self.wait(2)

        self.play(FadeOut(VGroup(u_step4, title_U, tex)))
        self.wait(1)
        
# Scene 7 - SVD Demonstration
class SVDExample(Scene):
    def construct(self):
        # ===== TIÊU ĐỀ =====
        title = Text("THỰC HÀNH PHÂN RÃ SVD", font_size=15, color=GREY).to_corner(UL, buff=0.25)
        self.play(Write(title))

        # Giới thiệu ma trận A
        A_mat = MathTex(r"A = \begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix}")
        self.play(FadeIn(A_mat))
        self.wait(1)
        
        # Đưa A lên góc phải để làm tham chiếu
        self.play(A_mat.animate.to_corner(UR, buff=0.25).scale(0.8))

        # ===== BƯỚC 1: TÍNH A^T A VÀ TRỊ RIÊNG =====
        # Sửa lỗi hiển thị mũ bằng cách ghép Text và MathTex
        step1_title = VGroup(
            Text("Bước 1: Tính", font_size=22, color=YELLOW),
            MathTex(r"A^T A", color=YELLOW).scale(0.8),
            Text("và tìm các trị riêng", font_size=22, color=YELLOW)
        ).arrange(RIGHT, buff=0.1).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        self.play(Write(step1_title))

        ATA = MathTex(r"A^T A = \begin{bmatrix} 1 & -2 \\ 0 & 1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix} = \begin{bmatrix} 5 & -2 & 1 \\ -2 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}").scale(0.8)
        ATA.next_to(step1_title, DOWN, buff=0.5).set_x(0)
        
        self.play(Write(ATA))
        self.wait(1.5)

        # Tính định thức nhanh
        det1 = MathTex(r"\det(A^T A - \lambda I) = 0").scale(0.8)
        det2 = MathTex(r"\Rightarrow (1-\lambda)\cdot\lambda\cdot(\lambda-6) = 0").scale(0.8)
        eigvals = MathTex(r"\Rightarrow \lambda_1 = 6,\ \lambda_2 = 1,\ \lambda_3 = 0").scale(0.8)

        det_group = VGroup(det1, det2, eigvals).arrange(DOWN, buff=0.4).next_to(ATA, DOWN, buff=0.5).set_x(0)

        self.play(Write(det1))
        self.wait(0.5)
        self.play(TransformFromCopy(det1, det2))
        self.wait(0.5)
        self.play(Write(eigvals))
        self.wait(2)

        self.play(FadeOut(ATA), FadeOut(det_group), FadeOut(step1_title))

        # ===== BƯỚC 2: TÌM MA TRẬN V^T TỪ VECTƠ RIÊNG =====
        step2_title = VGroup(
            Text("Bước 2: Tìm vectơ riêng của", font_size=22, color=YELLOW),
            MathTex(r"A^T A", color=YELLOW).scale(0.8),
            Text("để xây dựng", font_size=22, color=YELLOW),
            MathTex(r"V^T", color=YELLOW).scale(0.8)
        ).arrange(RIGHT, buff=0.1).move_to(step1_title, aligned_edge=LEFT)
        
        self.play(Write(step2_title))

        # Nơi lưu 3 vectơ riêng ở góc dưới
        v_final_group = VGroup(
            MathTex(r"v_1 = \frac{1}{\sqrt{30}} \begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}"),
            MathTex(r"v_2 = \frac{1}{\sqrt{5}} \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix}"),
            MathTex(r"v_3 = \frac{1}{\sqrt{6}} \begin{bmatrix} -1 \\ -2 \\ 1 \end{bmatrix}")
        ).arrange(RIGHT, buff=0.8).scale(0.65).to_edge(DOWN, buff=0.5)

        # Trình diễn giải hệ phương trình
        for i, (l_val, v_mat_str, sol_str) in enumerate([
            (6, r"\begin{bmatrix} -1 & -2 & 1 \\ -2 & -5 & 0 \\ 1 & 0 & -5 \end{bmatrix}", r"\frac{1}{\sqrt{30}} \begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}"),
            (1, r"\begin{bmatrix} 4 & -2 & 1 \\ -2 & 0 & 0 \\ 1 & 0 & 0 \end{bmatrix}", r"\frac{1}{\sqrt{5}} \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix}"),
            (0, r"\begin{bmatrix} 5 & -2 & 1 \\ -2 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}", r"\frac{1}{\sqrt{6}} \begin{bmatrix} -1 \\ -2 \\ 1 \end{bmatrix}")
        ]):
            l_title = MathTex(fr"\lambda_{{{i+1}}} = {l_val} \Rightarrow (A^T A - {l_val}I)v = 0").scale(0.8).next_to(step2_title, DOWN, buff=0.4, aligned_edge=LEFT)
            l_eq = MathTex(fr"{v_mat_str} v = 0").scale(0.7)
            
            l_sol_txt = Text("Chuẩn hoá: ", font_size=20)
            l_sol_math = MathTex(fr"v_{{{i+1}}} = {sol_str}").scale(0.7)
            l_sol = VGroup(l_sol_txt, l_sol_math).arrange(RIGHT, buff=0.2)
            
            l_display = VGroup(l_eq, l_sol).arrange(DOWN, buff=0.4).next_to(l_title, DOWN, buff=0.4).set_x(0)
            
            self.play(Write(l_title))
            self.play(Write(l_eq))
            self.wait(0.5)
            self.play(Write(l_sol))
            self.wait(1)
            self.play(TransformFromCopy(l_sol_math, v_final_group[i]))
            self.play(FadeOut(l_title), FadeOut(l_display))

        # Kéo các vectơ v lên giữa màn hình để gộp thành V^T
        self.play(v_final_group.animate.next_to(step2_title, DOWN, buff=0.5).set_x(0))
        self.wait(1)

        VT_mat = MathTex(
            r"V^T = \begin{bmatrix} v_1^T \\ v_2^T \\ v_3^T \end{bmatrix} = \begin{bmatrix} \frac{5}{\sqrt{30}} & \frac{-2}{\sqrt{30}} & \frac{1}{\sqrt{30}} \\ 0 & \frac{1}{\sqrt{5}} & \frac{2}{\sqrt{5}} \\ \frac{-1}{\sqrt{6}} & \frac{-2}{\sqrt{6}} & \frac{1}{\sqrt{6}} \end{bmatrix}"
        ).scale(0.7).next_to(v_final_group, DOWN, buff=0.6)

        self.play(Write(VT_mat))
        self.wait(2)
        
        # Xóa sạch V^T và title đi để giải phóng không gian cho bước sau
        self.play(FadeOut(v_final_group), FadeOut(step2_title), FadeOut(VT_mat))

        # ===== BƯỚC 3: XÂY DỰNG SIGMA =====
        step3_title = VGroup(
            Text("Bước 3: Xây dựng ma trận", font_size=22, color=YELLOW),
            MathTex(r"\Sigma", color=YELLOW).scale(0.8)
        ).arrange(RIGHT, buff=0.1).move_to(step1_title, aligned_edge=LEFT)
        
        self.play(Write(step3_title))

        sigma_eq = MathTex(r"\sigma_i = \sqrt{\lambda_i} \Rightarrow \sigma_1 = \sqrt{6}, \quad \sigma_2 = 1").scale(0.8)
        sigma_eq.next_to(step3_title, DOWN, buff=0.6).set_x(0)
        
        Sigma_mat = MathTex(r"\Sigma = \begin{bmatrix} \sqrt{6} & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}").scale(0.8)
        Sigma_mat.next_to(sigma_eq, DOWN, buff=0.6)

        self.play(Write(sigma_eq))
        self.wait(1)
        self.play(Write(Sigma_mat))
        self.wait(2)
        
        # Xóa sạch bảng
        self.play(FadeOut(step3_title), FadeOut(sigma_eq), FadeOut(Sigma_mat))

        # ===== BƯỚC 4: TÌM U =====
        step4_title = VGroup(
            Text("Bước 4: Tính U bằng công thức", font_size=22, color=YELLOW),
            MathTex(r"u_i = \frac{1}{\sigma_i} A v_i", color=YELLOW).scale(0.8)
        ).arrange(RIGHT, buff=0.1).move_to(step1_title, aligned_edge=LEFT)
        
        self.play(Write(step4_title))

        u1_calc = MathTex(
            r"u_1", r"=", r"\frac{1}{\sqrt{6}} \begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix} \left( \frac{1}{\sqrt{30}} \begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix} \right)", r"=", r"\frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -2 \end{bmatrix}"
        ).scale(0.7).next_to(step4_title, DOWN, buff=0.5).set_x(0)

        u2_calc = MathTex(
            r"u_2", r"=", r"\frac{1}{1} \begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix} \left( \frac{1}{\sqrt{5}} \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix} \right)", r"=", r"\frac{1}{\sqrt{5}} \begin{bmatrix} 2 \\ 1 \end{bmatrix}"
        ).scale(0.7).next_to(u1_calc, DOWN, buff=0.5).set_x(0)

        self.play(Write(u1_calc[0:3]))
        self.wait(1)
        self.play(Write(u1_calc[3:]))
        
        self.play(Write(u2_calc[0:3]))
        self.wait(1)
        self.play(Write(u2_calc[3:]))
        self.wait(1)

        U_mat = MathTex(r"U = [u_1 \quad u_2] = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & 2 \\ -2 & 1 \end{bmatrix}").scale(0.8)
        U_mat.next_to(u2_calc, DOWN, buff=0.6).set_x(0)
        
        self.play(Write(U_mat))
        self.wait(2)

        # Xóa sạch bảng để chuẩn bị kết luận
        self.play(FadeOut(step4_title), FadeOut(u1_calc), FadeOut(u2_calc), FadeOut(U_mat))

        # ===== BƯỚC 5: TỔNG KẾT A = U \Sigma V^T =====
        final_title = VGroup(
            Text("Kết luận:", font_size=28, color=YELLOW),
            MathTex(r"A = U \Sigma V^T", color=YELLOW)
        ).arrange(RIGHT, buff=0.2).to_edge(UP, buff=1.0)
        
        self.play(Write(final_title))

        # Ẩn A tham chiếu cũ đi
        self.play(FadeOut(A_mat))

        # Hiển thị biểu thức cuối cùng gom lại tất cả các ma trận đã tính
        final_eq = MathTex(
            r"A = ",
            r"\left( \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & 2 \\ -2 & 1 \end{bmatrix} \right)", 
            r"\begin{bmatrix} \sqrt{6} & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}",
            r"\begin{bmatrix} \frac{5}{\sqrt{30}} & \frac{-2}{\sqrt{30}} & \frac{1}{\sqrt{30}} \\ 0 & \frac{1}{\sqrt{5}} & \frac{2}{\sqrt{5}} \\ \frac{-1}{\sqrt{6}} & \frac{-2}{\sqrt{6}} & \frac{1}{\sqrt{6}} \end{bmatrix}"
        ).scale(0.65).next_to(final_title, DOWN, buff=1.0)

        # Chú thích nhỏ ở dưới để đánh dấu U, Sigma, V^T
        brace_U = Brace(final_eq[1], DOWN, color=BLUE)
        text_U = brace_U.get_tex("U").scale(0.8).set_color(BLUE)
        
        brace_S = Brace(final_eq[2], DOWN, color=YELLOW)
        text_S = brace_S.get_tex(r"\Sigma").scale(0.8).set_color(YELLOW)
        
        brace_VT = Brace(final_eq[3], DOWN, color=GREEN)
        text_VT = brace_VT.get_tex("V^T").scale(0.8).set_color(GREEN)

        self.play(Write(final_eq))
        self.wait(1)
        self.play(
            GrowFromCenter(brace_U), Write(text_U),
            GrowFromCenter(brace_S), Write(text_S),
            GrowFromCenter(brace_VT), Write(text_VT)
        )
        self.wait(3)
        
# Scene 8 - Visualization
class SVDVisualization(Scene):
    def construct(self):
        # ===== TITLE =====
        title = Text("TRỰC QUAN HÓA SVD", font_size=24, color=GREY)
        title.to_corner(UL)
        self.add(title)

        # ===== TRỤC TỌA ĐỘ =====
        # Sử dụng NumberPlane cho 2D thay vì ThreeDAxes
        plane = NumberPlane()
        self.play(Create(plane), run_time=1)

        # ===== CIRCLE VÀ VECTORS =====
        # Thêm 2 vector vào trong hình tròn để thấy rõ sự xoay
        circle = Circle(radius=1.5)
        circle.set_fill(color=BLUE, opacity=0.5)
        circle.set_stroke(color=WHITE, width=2)
        
        vec_x = Vector(RIGHT * 1.5, color=RED)
        vec_y = Vector(UP * 1.5, color=GREEN)
        
        # Gộp tất cả lại thành một nhóm để áp dụng ma trận
        shape = VGroup(circle, vec_x, vec_y)

        self.play(FadeIn(shape), run_time=1)
        self.wait(0.5)

        # ===== MATRICES =====
        # Để an toàn cho Manim, ta vẫn khai báo ma trận 3x3 nhưng giữ trục Z cố định (z=1 và không có phép biến đổi nào trên Z).
        
        # V^T: Ma trận xoay 45 độ
        angle_v = 45 * DEGREES
        VT = np.array([
            [np.cos(angle_v), -np.sin(angle_v), 0],
            [np.sin(angle_v),  np.cos(angle_v), 0],
            [0,                0,               1]
        ])

        # Sigma: Ma trận co giãn (Kéo giãn trục X gấp đôi, trục Y giữ nguyên)
        Sigma = np.array([
            [2, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

        # U: Ma trận xoay 30 độ
        angle_u = 30 * DEGREES
        U = np.array([
            [np.cos(angle_u), -np.sin(angle_u), 0],
            [np.sin(angle_u),  np.cos(angle_u), 0],
            [0,                0,               1]
        ])

        # ===== LABEL FUNCTION =====
        def show_label(text1, math_tex, text2):
            label = VGroup(
                Text(text1, font_size=26, color=YELLOW),
                MathTex(math_tex, color=YELLOW).scale(1.2),
                Text(text2, font_size=26, color=YELLOW)
            ).arrange(RIGHT, buff=0.2).to_edge(UP)

            self.play(FadeIn(label), run_time=0.5)
            return label

        # ===== BƯỚC 1: Xoay bởi V^T =====
        l_vt = show_label("1. Áp dụng", r"V^T", "(Xoay 45 độ)")
        self.play(ApplyMatrix(VT, shape), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(l_vt, shift=RIGHT))

        # ===== BƯỚC 2: Co giãn bởi Sigma =====
        l_sigma = show_label("2. Áp dụng", r"\Sigma", "(Kéo giãn theo trục X)")
        self.play(ApplyMatrix(Sigma, shape), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(l_sigma, shift=RIGHT))

        # ===== BƯỚC 3: Xoay bởi U =====
        l_u = show_label("3. Áp dụng", r"U", "(Xoay 30 độ)")
        self.play(ApplyMatrix(U, shape), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(l_u, shift=RIGHT))

        # Giữ nguyên màn hình ở cuối
        self.wait(3)
        
# Scene 9 - SVD application 1
class SVDReconstruction(Scene):
    def construct(self):
        tex = Text("CÁC ỨNG DỤNG CỦA SVD", font="Times New Roman", font_size=15, color=GREY)
        tex.to_corner(UL, buff=0.25)
        title = Text("Áp dụng trong ước lượng hình ảnh", font="Times New Roman", font_size=20)
        title.to_edge(UP, buff=1.0)
        self.play(Write(tex))
        self.wait(2)
        self.play(Write(title))
        img = Image.open("img.png").convert("L").resize((64*3, 64*4))
        matrix = np.array(img) / 255.0  # Normalize for grayscale

        U, s, Vt = np.linalg.svd(matrix, full_matrices=False)

        display_img = ImageMobject(img).scale(2).to_edge(LEFT, buff=2.5)
        k_text = Variable(0, Text("k"), var_type=Integer).to_edge(RIGHT, buff=2.0).to_edge(UP, buff=2.5)

        self.add( k_text)

        ranks_to_show = [1, 2, 5, 10, 20, 50, 128]

        current_img_mobject = None
        eq = MathTex(r" A = \sum_{i=1}^{k} \sigma_i \, \mathbf{u}_i \mathbf{v}_i^T ")
        eq.next_to(k_text, DOWN, buff=1.5)
        self.play(Write(eq))
        for k in ranks_to_show:
            U_k = U[:, :k]
            S_k = np.diag(s[:k])
            Vt_k = Vt[:k, :]
            recon_matrix = np.dot(U_k, np.dot(S_k, Vt_k))

            recon_matrix = np.clip(recon_matrix, 0, 1) * 255
            new_img = ImageMobject(recon_matrix.astype(np.uint8)).scale(2).to_edge(LEFT, buff=2.0)

            if current_img_mobject is None:
                self.play(FadeIn(new_img), k_text.tracker.animate.set_value(k))
            else:
                self.play(
                    Transform(current_img_mobject, new_img),
                    k_text.tracker.animate.set_value(k),
                    run_time=2.0
                )

            current_img_mobject = new_img
            self.wait(1)

# Scene 10 - SVD application 2
class PCA(MovingCameraScene):
    def construct(self):
        tex = Text("CÁC ỨNG DỤNG CỦA SVD",font="Times New Roman", font_size=15, color=GREY)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        title = Text("Áp dụng trong PCA", font="Times New Roman", font_size=36)
        title.to_edge(UP, buff=2.0)
        matrix_data = [
            ["STT", "Chiều cao (cm)", "Cân nặng (kg)"],
            ["1", "160", "55"],
            ["2", "165", "60"],
            ["3", "170", "58"],
            ["4", "175", "70"],
            ["5", "168", "62"],
            ["...", "...", "..."]
        ]

        table = Table(
            matrix_data,
            element_to_mobject=lambda x: Text(x, font="Times New Roman")
        )

        table.scale(0.5)
        self.play(Create(table))
        self.wait(2)
        self.play(FadeOut(table))

        axes = Axes(
            x_range=[0, 100, 50],
            y_range=[0, 200, 50],
            axis_config={"include_numbers": True}
        )

        N = 50
        x = np.random.uniform(0, 100, N)
        y = np.random.uniform(0, 200, N)
        data = np.column_stack((x, y))

        dots = VGroup(*[
            Dot(axes.c2p(px, py), color=BLUE)
            for px, py in data
        ])

        labels = axes.get_axis_labels(
            x_label=Text("Cân nặng (kg)", font="Times New Roman", font_size=14),
            y_label=Text("Chiều cao (cm)", font="Times New Roman", font_size=14)
        )

        self.play(Create(axes), Write(labels))
        self.play(FadeIn(dots))
        self.wait(2)

        proj_x = VGroup(*[
            Dot(axes.c2p(px, 0), color=BLUE)
            for px, py in data
        ])

        self.play(Transform(dots, proj_x))
        self.wait(5)

        self.play(FadeOut(dots, labels, axes))  # ❗ removed proj_x duplicate fade

        N = 30

        cluster1 = np.column_stack((
            np.random.uniform(0, 40, N),
            np.random.uniform(130, 200, N)
        ))

        cluster2 = np.column_stack((
            np.random.uniform(50, 100, N),
            np.random.uniform(140, 200, N)
        ))

        cluster3 = np.column_stack((
            np.random.uniform(0, 30, N),
            np.random.uniform(0, 100, N)
        ))

        data3 = np.vstack([cluster1, cluster2, cluster3])

        colors = (
                [BLUE] * len(cluster1) +
                [GREEN] * len(cluster2) +
                [ORANGE] * len(cluster3)
        )

        limit = np.max(np.abs(data3)) * 1.2

        axes2 = Axes(
            x_range=[0, 150, 50],
            y_range=[0, 250, 50],
            axis_config={"include_numbers": True}
        )

        labels2 = axes2.get_axis_labels(
            x_label=Text("Cân nặng (kg)", font="Times New Roman", font_size=14),
            y_label=Text("Chiều cao (cm)", font="Times New Roman", font_size=14)
        )

        dots3 = VGroup(*[
            Dot(axes2.c2p(px, py), color=colors[i])
            for i, (px, py) in enumerate(data3)
        ])

        self.play(Create(axes2), Write(labels2))
        self.play(FadeIn(dots3))
        self.wait(2)

        original_dots = dots3.copy()

        proj_x = VGroup(*[
            Dot(axes2.c2p(px, 0), color=colors[i])
            for i, (px, py) in enumerate(data3)
        ])

        proj_y = VGroup(*[
            Dot(axes2.c2p(0, py), color=colors[i])
            for i, (px, py) in enumerate(data3)
        ])

        self.play(Transform(dots3, proj_x))
        self.wait(5)

        self.play(FadeOut(dots3))
        dots3 = original_dots.copy()
        self.play(FadeIn(dots3))
        self.wait(5)

        self.play(Transform(dots3, proj_y))
        self.wait(5)

        self.play(FadeOut(dots3, proj_y, proj_x))
        dots3 = original_dots.copy()

        mean3 = np.mean(data3, axis=0)
        centered3 = data3 - mean3

        U, S, VT = np.linalg.svd(centered3)
        pc1_3 = VT[0]

        arrow_pca = Arrow(
            axes2.c2p(mean3[0], mean3[1]),
            axes2.c2p(mean3[0] + pc1_3[0] * limit, mean3[1] + pc1_3[1] * limit),
            color=RED,
            buff=0
        )

        proj_pca = []
        for point in data3:
            proj_len = np.dot(point - mean3, pc1_3)
            proj_point = mean3 + proj_len * pc1_3
            proj_pca.append(proj_point)

        dots_pca = VGroup(*[
            Dot(axes2.c2p(px, py), color=colors[i])
            for i, (px, py) in enumerate(proj_pca)
        ])
        self.play(FadeIn(dots3))
        self.play(GrowArrow(arrow_pca))
        self.wait(2)
        new_axes = Axes(
            x_range=[0, 100, 50],
            y_range=[0, 200, 100],
            axis_config={"include_numbers": True}
        )
        self.play(Transform(dots3, dots_pca))
        self.wait(3)
        self.play(
            Transform(axes, new_axes),
            FadeOut(axes2),
            self.camera.frame.animate.scale(1.3)
        )
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])