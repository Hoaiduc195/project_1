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

        tex = Text("TỔNG QUAN VỀ SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        self.wait(2)

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



# Scene 2 - TONG QUAN VE SVD

class SVDedvan(Scene):
    def construct(self):
        tex = Text("TỔNG QUAN VỀ SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        Title = Text("Điểm mạnh của SVD",font="Arial", font_size=36)
        self.play(Title.animate.to_edge(UP, buff = 1.0))

        matrices = [
            MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}").next_to(Title, DOWN, buff=2.0),
            MathTex(r"\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9\end{bmatrix}").next_to(Title, DOWN, buff=2.0),
            MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 0 & 0\end{bmatrix}").next_to(Title, DOWN, buff=2.0),
            MathTex(r"\begin{bmatrix} 1 & 2 & 3\\ 4 & 5 & 6\end{bmatrix}").next_to(Title, DOWN, buff=2.0)
        ]
        tex = Text("Mọi ma trận bất kể rank, không gian và tính đối xứng để có thể phân rã thành SVD",font="Arial", font_size=20)
        tex.next_to(matrices[0], DOWN, buff=1.5)
        current = matrices[0]
        self.play(Write(current))
        self.play(Write(tex))
        self.wait()
        for next_matrix in matrices[1:]:
            self.play(Transform(current, next_matrix))
            self.wait()


# Scene 3 - TONG QUAN VE SVD
class SVDConceptFlow(Scene):
    def construct(self):
        tex = Text("TỔNG QUAN VỀ SVD", font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))

        tex2 = Text("CÁC KIẾN THỨC CẦN THIẾT", font="Arial", font_size=15)
        tex2.to_corner(UL, buff=0.25)
        self.play(Transform(tex, tex2))
        self.wait(2)

        plane = NumberPlane()
        self.play(Create(plane))

        v1 = Arrow(plane.c2p(0, 0), plane.c2p(2, 1), buff=0, color=BLUE)
        v2 = Arrow(plane.c2p(0, 0), plane.c2p(1, 2), buff=0, color=GREEN)

        label = Text("Không gian vector và bao tuyến tính", font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Write(label), GrowArrow(v1), GrowArrow(v2))
        self.wait(2)

        v1_ortho = Arrow(plane.c2p(0, 0), plane.c2p(2, 0), buff=0, color=BLUE)
        v2_ortho = Arrow(plane.c2p(0, 0), plane.c2p(0, 2), buff=0, color=GREEN)

        new_label = Text("Trực giao",font="Arial").scale(0.4).to_edge(DOWN)

        self.play(
            Transform(v1, v1_ortho),
            Transform(v2, v2_ortho),
            Transform(label, new_label)
        )

        right_angle = RightAngle(v1, v2, length=0.3)
        self.play(Create(right_angle))
        self.wait(2)

        square = Square(color=YELLOW)
        self.play(FadeOut(v1, v2, right_angle), Create(square))

        new_label = Text("Ma trận trực giao = phép quay",font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Transform(label, new_label))

        self.play(square.animate.rotate(PI / 4))
        self.wait(2)

        vector = Arrow(plane.c2p(0, 0), plane.c2p(2, 1), buff=0, color=RED)
        self.play(FadeOut(square), GrowArrow(vector))

        new_label = Text("Vector riêng: hướng không đổi",font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Transform(label, new_label))

        matrix = Arrow(plane.c2p(0, 0), plane.c2p(4, 1), buff=0, color=RED)
        self.play(Transform(vector, matrix))
        self.wait(2)
        new_label = Text("Đổi cơ sở",font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Transform(label, new_label))

        self.play(plane.animate.rotate(PI / 6))
        self.wait(2)
        self.play(plane.animate.rotate(-PI / 6))

        square = Square(color=BLUE)
        self.play(FadeOut(vector), Create(square))

        new_label = Text("Hạng = số chiều sau biến đổi", font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Transform(label, new_label))

        collapse_matrix = [[1, 0], [0, 0]]
        self.play(square.animate.apply_matrix(collapse_matrix))
        self.wait(2)
        self.play(FadeOut(square))

        vec = Arrow(plane.c2p(0, 0), plane.c2p(2, 1), buff=0, color=BLUE)
        axis = Line(plane.c2p(0, 0), plane.c2p(3, 0), color=YELLOW)
        proj = Arrow(plane.c2p(0, 0), plane.c2p(2, 0), buff=0, color=GREEN)

        orthvec = Arrow(plane.c2p(2, 1), plane.c2p(2, 0), buff=0, color=YELLOW)
        dashed_vec = DashedVMobject(orthvec, num_dashes=20)

        self.play(GrowArrow(vec), Create(axis))

        new_label = Text("Phép chiếu", font="Arial").scale(0.4).to_edge(DOWN)
        self.play(Transform(label, new_label))

        self.play(Create(dashed_vec))
        self.wait(1)
        self.play(GrowArrow(proj))
        self.wait(2)

        self.play(FadeOut(vec, axis, proj, dashed_vec, plane))

        psd_text = MathTex("x^T A^T A x \\ge 0")
        new_label = Text("Ma trận bán xác định dương", font="Arial").scale(0.4).to_edge(DOWN)

        self.play(Transform(label, new_label), Write(psd_text))
        self.wait(2)

        self.play(FadeOut(psd_text))

        flow = Text("Quá trình hình thành SVD", font="Arial", font_size=36)
        flow.to_edge(UP, buff=2.0)

        new_label = Text("SVD = Phép quay → Phép co giãn → Phép quay", font="Arial", font_size=30).next_to(flow, DOWN, buff=1.5)

        self.play(Transform(label, new_label))
        self.play(Write(flow))
        self.wait(3)

        self.play(FadeOut(flow, label))
        self.wait()

# Scene 1 - TINH TOAN SVD
class ComputeSVD(Scene):
    def construct(self):
        tex = Text("TÍNH TOÁN SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        expr = MathTex("A", "=", "U", r"\Sigma", "V^T")
        expr.scale(1.0)
        expr_cop = expr.copy()

        self.play(Write(expr))

        U = expr[2]
        Sigma = expr[3]
        VT = expr[4]
        A = expr[0]

        self.wait(2)
        self.play(expr.animate.to_edge(UP, buff=2.0))

        label_S = Text("Chéo chữ nhật", font="Arial", font_size=40).scale(0.5).next_to(Sigma, DOWN, buff=1.0)
        label_U = Text("Trực giao", font="Arial", font_size=40).scale(0.5).next_to(label_S, LEFT, buff=2.0)
        label_V = Text("Trực giao", font="Arial", font_size=40).scale(0.5).next_to(label_S, RIGHT, buff=2.0)

        arrow_U = Arrow(label_U.get_top(), U.get_bottom())
        arrow_S = Arrow(label_S.get_top(), Sigma.get_bottom())
        arrow_V = Arrow(label_V.get_top(), VT.get_bottom())

        self.play(FadeIn(label_S))
        self.play(Create(arrow_S))
        self.wait(2)

        self.play(FadeIn(label_U, label_V))
        self.play(Create(arrow_U), Create(arrow_V))

        self.play(FadeOut(VGroup(label_U, label_S, label_V, arrow_U, arrow_S, arrow_V)))

        sigma_copy = Sigma.copy()
        A_copy = A.copy()

        rows, cols = 2, 3

        gridA = VGroup()
        for i in range(rows):
            for j in range(cols):
                box = Dot()
                box.move_to([j - cols/2, rows/2 - i, 0])
                gridA.add(box)

        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                box = Dot(radius=0.01)  # small invisible anchor
                box.move_to([j - cols / 2, rows / 2 - i, 0])
                grid.add(box)

        grid.set_stroke(width=2)

        left_bracket1 = MathTex(r"\left[").scale(2.5)
        right_bracket1 = MathTex(r"\right]").scale(2.5)
        left_bracket2 = left_bracket1.copy()
        right_bracket2 = right_bracket1.copy()

        left_bracket2.next_to(gridA, LEFT)
        right_bracket2.next_to(gridA, RIGHT)
        left_bracket1.next_to(grid, LEFT)
        right_bracket1.next_to(grid, RIGHT)

        matrix_frame = VGroup(left_bracket1, grid, right_bracket1)
        matrix_frame.to_edge(DOWN, buff=1.0)

        left_bracket2=left_bracket1.copy()
        right_bracket2=right_bracket1.copy()

        left_bracket2.next_to(gridA, LEFT)
        right_bracket2.next_to(gridA, RIGHT)

        matrix_frame2 = VGroup(left_bracket2, gridA, right_bracket2)
        matrix_frame2.next_to(matrix_frame, LEFT, buff=1.0)

        self.wait(1)

        self.play(Create(matrix_frame), Create(matrix_frame2))

        self.play(
            Transform(sigma_copy, matrix_frame),
            Transform(A_copy, matrix_frame2),
        )
        size_text1 = Text("2 x 3", font="Arial").scale(0.5).next_to(matrix_frame, DOWN)
        size_text2 = Text("2 x 3", font="Arial").scale(0.5).next_to(matrix_frame2, DOWN)
        eq = MathTex(r"\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_k \ge 0")
        eq.next_to(matrix_frame, RIGHT, buff=1.0)
        self.play(Write(eq))
        self.play(Write(size_text1), Write(size_text2))

        self.wait(2)
        arrow1 = Arrow(A.get_bottom(), matrix_frame2.get_top())
        arrow2 = Arrow(Sigma.get_bottom(), matrix_frame.get_top())
        self.play(Create(arrow1), Create(arrow2))
        rows, cols = 2, 3
        grid2 = VGroup()

        for i in range(rows):
            for j in range(cols):
                if i == j:
                    val = MathTex(rf"\sigma_{{{i + 1}}}").scale(0.6)
                    val.move_to(grid[i * cols + j].get_center())
                    grid2.add(val)

        self.wait(2)

        self.play(LaggedStart(*[FadeIn(x) for x in grid2], lag_ratio=0.3))

        self.wait(7)
        self.play(FadeOut(arrow1, arrow2, sigma_copy, matrix_frame, matrix_frame2, A_copy, grid2, size_text1, size_text2, eq))
        self.play(Transform(expr, expr_cop))

        break1 = MathTex("A^T A = U \\Sigma V^T")
        self.play(Transform(expr, break1))
        self.wait(2)

        break2 = MathTex("A^T A = (U \\Sigma V^T)^T U \\Sigma V^T")
        self.play(Transform(expr, break2))
        self.wait(2)

        break3 = MathTex("A^T A = V \\Sigma^T U^T U \\Sigma V^T")

        self.play(Transform(expr, break3))
        self.wait(2)
        step2 = MathTex(
            r"A^T A", " = ", "V",  r"\Sigma^T \Sigma", r"V^T"
        )
        self.play(ReplacementTransform(expr, step2))
        self.wait(2)
        self.play(step2.animate.to_edge(UP, buff=2.0))
        second_eq = MathTex(r"A^T A", " = ", "P", "D", r"P^T")
        second_eq.next_to(step2, DOWN, buff=2.0)
        arrow3=Arrow(second_eq[2].get_top(), step2[2].get_bottom())
        arrow4 = Arrow(second_eq[3].get_top(), step2[3].get_bottom())
        self.play(Write(second_eq))
        self.play(Create(arrow4), Create(arrow3))
        self.wait(2)
        self.play(FadeOut(step2, arrow3, arrow4, second_eq))

        identity = MathTex(
            r"\Sigma^T \Sigma = D"
        ).scale(1)

        self.play((identity.animate.to_edge(UP, buff=1.0)))
        self.wait(2)
        sigma_prod = MathTex(
            r"\begin{bmatrix}",
            r"\sigma_1^2 & 0 & 0 \\",
            r"0 & \sigma_2^2 & 0 \\",
            r"0 & 0 & \cdots",
            r"\end{bmatrix}"
        ).scale(0.9)
        self.play(Write(sigma_prod.to_edge(LEFT, buff=4)))
        self.wait(2)
        D_matrix = MathTex(
            r"=",
            r"\begin{bmatrix}",
            r"\lambda_1 & 0 & 0 \\",
            r"0 & \lambda_2 & 0 \\",
            r"0 & 0 & \cdots",
            r"\end{bmatrix}"
        ).scale(0.9)

        D_matrix.next_to(sigma_prod, RIGHT)

        self.play(Write(D_matrix))
        self.wait(2)
        self.play(FadeOut(sigma_prod, D_matrix, identity))
        title = Text("U =", font="Arial", font_size=28).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        step1 = MathTex(r"u_i = \frac{1}{\sigma_i} A v_i")
        self.play(Write(step1))
        self.wait(2)

        step2 = MathTex(
            r"u_i = \frac{A v_i}{\|A v_i\|}"
        )
        self.play(ReplacementTransform(step1, step2))
        self.wait(2)

        step3 = MathTex(
            r"U = [u_1 \; u_2 \; \cdots \; u_k]"
        )
        self.play(ReplacementTransform(step2, step3))
        self.wait(2)

        step4 = MathTex(
            r"U = A V \Sigma^{-1}"
        )
        self.play(ReplacementTransform(step3, step4))
        self.wait(2)

        note = MathTex(
            r"\sigma_i \neq 0"
        ).scale(0.8)
        note.next_to(step4, DOWN)

        self.play(FadeIn(note))
        self.wait(2)

        self.play(FadeOut(step4, note, title))


# Scene 2 - TINH TOAN SVD
class SVDExample(Scene):
    def construct(self):
        tex = Text("TÍNH TOÁN SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        A = MathTex(r"A = \begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix}")
        A_saved = MathTex(r"\begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix} = ")
        self.play(Write(A))
        self.wait(2)

        self.play(FadeOut(A))

        ATA_step = MathTex(
            r"A^T A =",
            r"\begin{bmatrix} 1 & -2 \\ 0 & 1 \\ 1 & 0 \end{bmatrix}",
            r"\begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix}"
        ).scale(0.9)

        self.play(Write(ATA_step))
        self.wait(2)

        ATA_result = MathTex(
            r"A^T A = \begin{bmatrix} 5 & -2 & 1 \\ -2 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}"
        )

        self.play(ReplacementTransform(ATA_step, ATA_result))
        self.wait(2)

        self.play(FadeOut(ATA_result))

        det1 = MathTex(
            r"\det(A^T A - \lambda I) = 0"
        )
        self.play(Write(det1))
        self.wait(1)

        det2 = MathTex(
            r"\det \begin{bmatrix}"
            r"5-\lambda & -2 & 1 \\"
            r"-2 & 1-\lambda & 0 \\"
            r"1 & 0 & 1-\lambda"
            r"\end{bmatrix} = 0"
        ).scale(0.9)

        self.play(ReplacementTransform(det1, det2))
        self.wait(2)

        det3 = MathTex(
            r"(5-\lambda)"
            r"\begin{vmatrix} 1-\lambda & 0 \\ 0 & 1-\lambda \end{vmatrix}"
            r" - (-2)"
            r"\begin{vmatrix} -2 & 0 \\ 1 & 1-\lambda \end{vmatrix}"
            r" + 1"
            r"\begin{vmatrix} -2 & 1-\lambda \\ 1 & 0 \end{vmatrix}"
        ).scale(0.8)

        self.play(ReplacementTransform(det2, det3))
        self.wait(3)

        det4 = MathTex(
            r"(5-\lambda)(1-\lambda)^2"
            r" - (-2)\big((-2)(1-\lambda)\big)"
            r" + 1\big((-2)\cdot0 - 1(1-\lambda)\big)"
        ).scale(0.8)

        self.play(ReplacementTransform(det3, det4))
        self.wait(3)

        det5 = MathTex(
            r"(5-\lambda)(1-\lambda)^2"
            r" - 4(1-\lambda)"
            r" - (1-\lambda)"
        ).scale(0.8)

        self.play(ReplacementTransform(det4, det5))
        self.wait(2)

        det6 = MathTex(
            r"(1-\lambda)\big[(5-\lambda)(1-\lambda) - 5\big]"
        ).scale(0.9)

        self.play(ReplacementTransform(det5, det6))
        self.wait(2)

        det7 = MathTex(
            r"(1-\lambda)(\lambda^2 -6\lambda +5)"
        ).scale(0.9)

        self.play(ReplacementTransform(det6, det7))
        self.wait(2)

        det8 = MathTex(
            r"(1-\lambda)(\lambda-1)(\lambda-6) = 0"
        ).scale(1)

        self.play(ReplacementTransform(det7, det8))
        self.wait(2)

        eigvals_result = MathTex(
            r"\lambda_1 = 6,\quad \lambda_2 = 1,\quad \lambda_3 = 0"
        )

        self.play(ReplacementTransform(det8, eigvals_result))
        self.wait(2)

        self.play(FadeOut(eigvals_result))

        lambda1 = MathTex(r"\lambda = 6")
        self.play(Write(lambda1))
        self.wait(2)
        eq1 = MathTex(
            r"(A^T A - 6I)v = 0"
        )
        self.play(Transform(lambda1, eq1))
        self.wait(1)

        matrix1 = MathTex(
            r"\begin{bmatrix}"
            r"-1 & -2 & 1 \\"
            r"-2 & -5 & 0 \\"
            r"1 & 0 & -5"
            r"\end{bmatrix} v = 0"
        ).scale(0.9)

        self.play(Transform(lambda1, matrix1))
        self.wait(2)

        v1 = MathTex(
            r"v_1 = \begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}"
        )
        self.play(Transform(lambda1, v1))
        self.wait(2)

        v1_norm = MathTex(
            r"v_1 = \frac{1}{\sqrt{30}} \begin{bmatrix} 5 \\ -2 \\ 1 \end{bmatrix}"
        )
        self.play(Transform(lambda1, v1_norm))
        self.wait(2)

        self.play(FadeOut(lambda1))

        lambda2 = MathTex(r"\lambda = 1")
        self.play(Write(lambda2))
        self.wait(2)

        matrix2 = MathTex(
            r"\begin{bmatrix}"
            r"4 & -2 & 1 \\"
            r"-2 & 0 & 0 \\"
            r"1 & 0 & 0"
            r"\end{bmatrix} v = 0"
        ).scale(0.9)

        self.play(Transform(lambda2, matrix2))
        self.wait(2)

        v2 = MathTex(
            r"v_2 = \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix}"
        )
        self.play(Transform(lambda2, v2))
        self.wait(2)

        v2_norm = MathTex(
            r"v_2 = \frac{1}{\sqrt{5}} \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix}"
        )
        self.play(Transform(lambda2, v2_norm))
        self.wait(2)

        self.play(FadeOut(lambda2))

        lambda3 = MathTex(r"\lambda = 0")
        self.play(Write(lambda3))
        self.wait(2)

        matrix3 = MathTex(
            r"A^T A v = 0"
        )
        self.play(Transform(lambda3, matrix3))
        self.wait(2)

        v3 = MathTex(
            r"v_3 = \begin{bmatrix} -1 \\ -2 \\ 1 \end{bmatrix}"
        )
        self.play(Transform(lambda3, v3))
        self.wait(2)

        v3_norm = MathTex(
            r"v_3 = \frac{1}{\sqrt{6}} \begin{bmatrix} -1 \\ -2 \\ 1 \end{bmatrix}"
        )
        self.play(Transform(lambda3, v3_norm))
        self.wait(2)

        self.play(FadeOut(lambda3))

        P = MathTex(
            r"P = \begin{bmatrix}"
            r"\frac{5}{\sqrt{30}} & 0 & -\frac{1}{\sqrt{6}} \\"
            r"\frac{-2}{\sqrt{30}} & \frac{1}{\sqrt{5}} & \frac{-2}{\sqrt{6}} \\"
            r"\frac{1}{\sqrt{30}} & \frac{2}{\sqrt{5}} & \frac{1}{\sqrt{6}}"
            r"\end{bmatrix}"
        ).scale(0.9)

        self.play(Write(P))
        self.wait(3)

        V = MathTex(r"V = P")
        V.next_to(P, DOWN, buff=2.0)

        self.play(Write(V))
        self.wait(2)
        self.play(FadeOut(P))
        self.play(V.animate.to_edge(UP, buff=2.0))


        vt_text = MathTex(r"V^T = P^T")
        vt_text.next_to(V, DOWN)

        self.play(Write(vt_text))
        self.wait(2)

        VT = MathTex(
            r"V^T = \begin{bmatrix}"
            r"\frac{5}{\sqrt{30}} & \frac{-2}{\sqrt{30}} & \frac{1}{\sqrt{30}} \\"
            r"0 & \frac{1}{\sqrt{5}} & \frac{2}{\sqrt{5}} \\"
            r"\frac{-1}{\sqrt{6}} & \frac{-2}{\sqrt{6}} & \frac{1}{\sqrt{6}}"
            r"\end{bmatrix}"
        ).scale(0.9)
        VT_saved= MathTex(
            r"\begin{bmatrix}"
            r"\frac{5}{\sqrt{30}} & \frac{-2}{\sqrt{30}} & \frac{1}{\sqrt{30}} \\"
            r"0 & \frac{1}{\sqrt{5}} & \frac{2}{\sqrt{5}} \\"
            r"\frac{-1}{\sqrt{6}} & \frac{-2}{\sqrt{6}} & \frac{1}{\sqrt{6}}"
            r"\end{bmatrix}"
        ).scale(0.9)
        VT.next_to(vt_text, DOWN)

        self.play(Write(VT))
        self.wait(3)
        self.play(FadeOut(VT, vt_text, V))

        diag1 = MathTex(r"A^T A = P D P^T")
        self.play(Write(diag1))
        self.wait(2)

        step1 = MathTex(r"A^T A = V D V^T")
        self.play(ReplacementTransform(diag1, step1))
        self.wait(2)

        step2 = MathTex(r"A^T A = V \Sigma^T \Sigma V^T")
        self.play(ReplacementTransform(step1, step2))
        self.wait(2)

        step3 = MathTex(r"D = \Sigma^T \Sigma")
        self.play(ReplacementTransform(step2, step3))
        self.wait(2)

        self.play(step3.animate.to_edge(UP, buff=1.0))
        sigma_sq = MathTex(
            r"\Sigma^T \Sigma = \begin{bmatrix}"
            r"\sigma_1^2 & 0 & 0 \\"
            r"0 & \sigma_2^2 & 0 \\"
            r"0 & 0 & 0"
            r"\end{bmatrix}"
        )
        self.play(Write(sigma_sq.next_to(step3, DOWN, 1.5)))
        self.wait(2)

        D = MathTex(
            r"D = \begin{bmatrix} 6 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}"
        )

        D.next_to(sigma_sq, DOWN)

        self.play(Write(D))
        self.wait(2)
        self.play(FadeOut(sigma_sq, D, step3))

        match = MathTex(
            r"\sigma_1^2 = 6,\quad \sigma_2^2 = 1"
        )
        self.play(Write(match))
        self.wait(2)

        sigma_final = MathTex(
            r"\sigma_i = \sqrt{\lambda_i}"
        ).scale(1.2)

        self.play(ReplacementTransform(match, sigma_final))
        self.wait(3)

        Sigma = MathTex(
            r"\Sigma = \begin{bmatrix} \sqrt{6} & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}"
        )
        Sigma_saved = MathTex(
            r"\begin{bmatrix} \sqrt{6} & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}"
        )
        self.play(ReplacementTransform(sigma_final, Sigma))
        self.wait(2)
        self.play(FadeOut(Sigma))


        U_rule = MathTex(r"u_i = \frac{1}{\sigma_i} A v_i")
        self.play(Write(U_rule))
        self.wait(2)


        step1 = MathTex(
            r"u_1 = \frac{1}{\sqrt{6}} A v_1"
        )
        self.play(ReplacementTransform(U_rule, step1))
        self.wait(2)

        step2 = MathTex(
            r"= \frac{1}{\sqrt{6}} "
            r"\begin{bmatrix} 1 & 0 & 1 \\ -2 & 1 & 0 \end{bmatrix}"
            r"\begin{bmatrix} \frac{5}{\sqrt{30}} \\ \frac{-2}{\sqrt{30}} \\ \frac{1}{\sqrt{30}} \end{bmatrix}"
        ).scale(0.8)

        self.play(ReplacementTransform(step1, step2))
        self.wait(3)

        step3 = MathTex(
            r"= \frac{1}{\sqrt{6}} \cdot \frac{1}{\sqrt{30}} "
            r"\begin{bmatrix} 6 \\ -12 \end{bmatrix}"
        ).scale(0.8)

        self.play(ReplacementTransform(step2, step3))
        self.wait(3)

        step4 = MathTex(
            r"= \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -2 \end{bmatrix}"
        )

        self.play(ReplacementTransform(step3, step4))
        self.wait(3)

        u1 = step4.copy()

        step5 = MathTex(
            r"u_2 = \frac{1}{1} A v_2"
        )
        self.play(ReplacementTransform(step4, step5))
        self.wait(2)

        step6 = MathTex(
            r"= \frac{1}{\sqrt{5}} \begin{bmatrix} 2 \\ 1 \end{bmatrix}"
        )

        self.play(ReplacementTransform(step5, step6))
        self.wait(2)

        u2 = step6.copy()

        U = MathTex(
            r"U = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & 2 \\ -2 & 1 \end{bmatrix}"
        )

        self.play(ReplacementTransform(step6, U))
        self.wait(3)

        self.play(FadeOut(U))
        U_saved = MathTex(
            r"\frac{1}{\sqrt{5}} \begin{bmatrix} 1 & 2 \\ -2 & 1 \end{bmatrix}"
        )

        final = MathTex(r"A = U \Sigma V^T").scale(1.5)
        self.play(Write(final))
        self.wait(1)

        self.play(final.animate.to_edge(UP, buff=2.0))


        A_saved.scale(0.9).next_to(final, DOWN, buff=1.5).to_edge(LEFT)
        self.wait(2)

        product = VGroup(
            U_saved.copy(),
            Sigma_saved.copy(),
            VT_saved.copy()
        ).arrange(RIGHT, buff=0.5)

        product.next_to(A_saved, RIGHT)

        self.play(Write(A_saved), FadeIn(product))

        self.wait(3)

# Scene 1 - TRUC QUAN HOA SVD
class SVDVisualization(ThreeDScene):
    def construct(self):
        tex = Text("TRỰC QUAN HÓA SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.add_fixed_in_frame_mobjects(tex)
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

        axes = ThreeDAxes()
        self.play(Create(axes))
        n_r = 12
        n_theta = 32
        radius = 2

        dots = VGroup()
        for i in range(n_r):
            r = radius * np.sqrt((i + 1) / n_r)

            for j in range(n_theta):
                theta = 2 * PI * j / n_theta

                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = 0

                t = (x + radius) / (2 * radius)

                t = np.clip(t, 0, 1)

                color = interpolate_color(BLUE, YELLOW, t)

                dot = Dot(point=[x, y, z], radius=0.035, color=color)
                dot.set_opacity(0.85)

                dots.add(dot)

        center_dot = Dot(point=[0, 0, 0], radius=0.04,
                         color=interpolate_color(BLUE, YELLOW, 0.5))
        dots.add(center_dot)

        self.play(FadeIn(dots))
        self.wait(1)

        theta_v = PI / 6
        Vt = np.array([
            [np.cos(theta_v), np.sin(theta_v), 0],
            [-np.sin(theta_v), np.cos(theta_v), 0],
            [0, 0, 1]
        ])

        Sigma = np.array([
            [2, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])

        theta_u = PI / 4
        U = np.array([
            [np.cos(theta_u), -np.sin(theta_u), 0],
            [np.sin(theta_u), np.cos(theta_u), 0],
            [0, 0, 1]
        ])

        label1 = VGroup(
            Text("Áp dụng", font="Arial", font_size=30),
            MathTex(r"V^T"),
            Text("(phép xoay)", font="Arial", font_size=30)
        ).arrange(RIGHT).to_edge(UP)
        self.add_fixed_in_frame_mobjects(label1)

        self.play(ApplyMatrix(Vt, dots), run_time=2)
        self.wait(1)

        label2 = VGroup(
            Text("Áp dụng", font="Arial", font_size=30),
            MathTex(r"\Sigma"),
            Text("(phép co giãn)", font="Arial", font_size=30)
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        self.add_fixed_in_frame_mobjects(label2)
        self.remove(label1)

        self.play(ApplyMatrix(Sigma, dots), run_time=2)
        self.wait(1)

        label3 = VGroup(
            Text("Áp dụng", font="Arial", font_size=30),
            MathTex(r"U"),
            Text("(phép xoay)", font="Arial", font_size=30)
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        self.add_fixed_in_frame_mobjects(label3)
        self.remove(label2)

        self.play(ApplyMatrix(U, dots), run_time=2)
        self.wait(1)

        final = MathTex(r"A = U \Sigma V^T").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final)

        self.play(Write(final))
        self.wait(2)

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)

# Scene 1 - UNG DUNG CUA SVD
class SVDReconstruction(Scene):
    def construct(self):
        tex = Text("CÁC ỨNG DỤNG CỦA SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        title = Text("Áp dụng trong ước lượng hình ảnh", font="Arial", font_size=20)
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

# Scene 2 - UNG DUNG CUA SVD
class PCA(MovingCameraScene):
    def construct(self):
        tex = Text("CÁC ỨNG DỤNG CỦA SVD",font="Arial", font_size=15)
        tex.to_corner(UL, buff=0.25)
        self.play(Write(tex))
        title = Text("Áp dụng trong PCA", font="Arial", font_size=36)
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
            element_to_mobject=lambda x: Text(x, font="Arial")
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
            x_label=Text("Cân nặng (kg)", font="Arial", font_size=14),
            y_label=Text("Chiều cao (cm)", font="Arial", font_size=14)
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
            x_label=Text("Cân nặng (kg)", font="Arial", font_size=14),
            y_label=Text("Chiều cao (cm)", font="Arial", font_size=14)
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





