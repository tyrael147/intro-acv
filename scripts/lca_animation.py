from manim import *


class LCAMatrixExplainer(Scene):
    def construct(self):
        self.intro_to_multiplication()
        self.system_of_equations()
        self.inventory_calculation()
        self.impact_calculation()

    def create_labeled_matrix(self, matrix, col_names, row_names):
        """Helper method to attach row and column labels safely outside the matrix brackets."""
        col_labels = VGroup(
            *[Text(name, font_size=18, weight=BOLD) for name in col_names]
        )
        row_labels = VGroup(
            *[Text(name, font_size=18, weight=BOLD) for name in row_names]
        )

        # Position column labels
        for i, col in enumerate(col_labels):
            col.next_to(matrix, UP, buff=0.2)
            col.set_x(matrix.get_columns()[i].get_x())  # Align exactly with the column

        # Position row labels
        for i, row in enumerate(row_labels):
            row.next_to(matrix, LEFT, buff=0.2)
            row.set_y(matrix.get_rows()[i].get_y())  # Align exactly with the row

        return VGroup(matrix, col_labels, row_labels)

    def intro_to_multiplication(self):
        # Section Title
        title = Tex("1. Introducción: Formalización de Matrices").to_edge(UP)
        self.play(Write(title))

        # Formal Algebraic Matrices
        mat1 = Matrix([["A_{11}", "A_{12}"], ["A_{21}", "A_{22}"]])
        mat2 = Matrix([["x_1"], ["x_2"]])
        eq = MathTex("=")
        res = Matrix([["A_{11}x_1 + A_{12}x_2"], ["A_{21}x_1 + A_{22}x_2"]])

        # Group and position
        group = VGroup(mat1, mat2, eq, res).arrange(RIGHT).scale(0.8)

        self.play(Write(mat1), Write(mat2))
        self.wait(1)

        text_explainer = Text(
            "Multiplicación Fila por Columna", font_size=24, color=YELLOW
        ).next_to(group, DOWN, buff=1)
        self.play(Write(text_explainer))

        # Highlight Row 1, Col 1
        row1 = mat1.get_rows()[0]
        col1 = mat2.get_columns()[0]
        rect1 = SurroundingRectangle(row1, color=YELLOW)
        rect2 = SurroundingRectangle(col1, color=YELLOW)

        self.play(Create(rect1), Create(rect2))
        self.play(Write(eq), FadeIn(res.get_brackets()), Write(res.get_entries()[0]))
        self.wait(2)

        # Highlight Row 2, Col 1
        self.play(
            Transform(rect1, SurroundingRectangle(mat1.get_rows()[1], color=YELLOW))
        )
        self.play(Write(res.get_entries()[1]))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(title, group, rect1, rect2, text_explainer)))

    def system_of_equations(self):
        # Section Title
        title = Tex("2. Matriz Tecnológica ($A \cdot s = f$)").to_edge(UP)
        self.play(Write(title))

        # Step 1: Formalization / Algebraic Symbols
        sym_A = Matrix(
            [
                ["A_{11}", "A_{12}", "A_{13}"],
                ["A_{21}", "A_{22}", "A_{23}"],
                ["A_{31}", "A_{32}", "A_{33}"],
            ]
        )
        sym_s = Matrix([["s_E"], ["s_F"], ["s_P"]])
        sym_eq = MathTex("=")
        sym_f = Matrix([["f_1"], ["f_2"], ["f_3"]])

        sym_group = VGroup(sym_A, sym_s, sym_eq, sym_f).arrange(RIGHT).scale(0.8)

        sym_label = Text("Formalización Algebraica", font_size=24, color=BLUE).next_to(
            sym_group, UP, buff=0.5
        )
        self.play(Write(sym_label), Write(sym_group))
        self.wait(2)

        # Step 2: Transition to Example from Slides
        num_A = Matrix([["1000", "0", "0"], ["-200", "1", "0"], ["0", "-1.2", "1"]])
        labeled_A = self.create_labeled_matrix(
            num_A,
            col_names=["Prod. Elec.", "Prod. Comb.", "Extr. Petr."],
            row_names=["Prod. Elec. (kWh)", "Prod. Comb. (L)", "Extr. Petr. (L)"],
        )

        num_s = Matrix([["s_E"], ["s_F"], ["s_P"]])
        num_f = Matrix([["1"], ["0"], ["0"]])

        num_group = (
            VGroup(labeled_A, num_s, sym_eq.copy(), num_f)
            .arrange(RIGHT, buff=0.5)
            .scale(0.7)
        )
        num_group.shift(DOWN * 0.5)

        num_label = Text(
            "Ejemplo Práctico (Matriz Tecnológica)", font_size=24, color=GREEN
        ).next_to(num_group, UP, buff=0.8)

        self.play(
            FadeOut(sym_label),
            ReplacementTransform(sym_group, num_group),
            Write(num_label),
        )
        self.wait(2)

        # Step 3: Solve for S
        vec_s_sol = Matrix([["0.001"], ["0.2"], ["0.24"]])
        sol_group = (
            VGroup(MathTex(r"s = A^{-1} \cdot f = "), vec_s_sol)
            .arrange(RIGHT)
            .scale(0.7)
        )
        sol_group.next_to(num_group, DOWN, buff=0.5)

        self.play(Write(sol_group))
        self.wait(3)

        # Cleanup
        self.play(FadeOut(VGroup(title, num_group, num_label, sol_group)))

    def inventory_calculation(self):
        # Section Title
        title = Tex("3. Matriz de Intervención ($g = B \cdot s$)").to_edge(UP)
        self.play(Write(title))

        # Step 1: Formalization / Algebraic Symbols
        sym_g = Matrix([["g_{1}"], ["g_{2}"]])
        sym_eq = MathTex("=")
        sym_B = Matrix([["B_{11}", "B_{12}", "B_{13}"], ["B_{21}", "B_{22}", "B_{23}"]])
        sym_s = Matrix([["s_E"], ["s_F"], ["s_P"]])

        sym_group = VGroup(sym_g, sym_eq, sym_B, sym_s).arrange(RIGHT).scale(0.8)
        sym_label = Text("Formalización Algebraica", font_size=24, color=BLUE).next_to(
            sym_group, UP, buff=0.5
        )

        self.play(Write(sym_label), Write(sym_group))
        self.wait(2)

        # Step 2: Transition to Example from Slides
        num_g = Matrix([["15.3"], ["-0.24"]])

        num_B = Matrix([["500", "50", "20"], ["0", "0", "-1"]])
        labeled_B = self.create_labeled_matrix(
            num_B,
            col_names=["Prod. Elec.", "Prod. Comb.", "Extr. Petr."],
            row_names=["CO2 (kg)", "Petróleo Crudo (L)"],
        )

        num_s = Matrix([["0.001"], ["0.2"], ["0.24"]])

        calc_group = (
            VGroup(labeled_B, num_s, sym_eq.copy(), num_g)
            .arrange(RIGHT, buff=0.5)
            .scale(0.7)
        )
        calc_group.shift(DOWN * 0.5)

        num_label = Text(
            "Ejemplo Práctico (Matriz de Intervención)", font_size=24, color=GREEN
        ).next_to(calc_group, UP, buff=0.8)

        # We first hide the result entries to animate the calculation
        num_g.get_entries().set_opacity(0)

        self.play(
            FadeOut(sym_label),
            ReplacementTransform(sym_group, calc_group),
            Write(num_label),
        )
        self.wait(1)

        # Step 3: Highlight multiplications to calculate g
        r1 = SurroundingRectangle(num_B.get_rows()[0], color=GREEN)
        c1 = SurroundingRectangle(num_s.get_columns()[0], color=GREEN)

        self.play(Create(r1), Create(c1))

        step1 = (
            MathTex("g_{CO2} = 500(0.001) + 50(0.2) + 20(0.24) = 15.3")
            .scale(0.7)
            .next_to(calc_group, DOWN, buff=0.5)
        )
        self.play(Write(step1))
        self.play(num_g.get_entries()[0].animate.set_opacity(1))
        self.wait(2)

        self.play(Transform(r1, SurroundingRectangle(num_B.get_rows()[1], color=GREEN)))

        step2 = (
            MathTex("g_{Crude} = 0(0.001) + 0(0.2) - 1(0.24) = -0.24")
            .scale(0.7)
            .next_to(calc_group, DOWN, buff=0.5)
        )
        self.play(ReplacementTransform(step1, step2))
        self.play(num_g.get_entries()[1].animate.set_opacity(1))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(title, calc_group, num_label, r1, c1, step2)))

    def impact_calculation(self):
        # Section Title
        title = Tex("4. Matriz de Caracterización ($h = Q \cdot g$)").to_edge(UP)
        self.play(Write(title))

        # Step 1: Formalization / Algebraic Symbols
        sym_h = Matrix([["h_{1}"], ["h_{2}"], ["h_{3}"]])
        sym_eq = MathTex("=")
        sym_Q = Matrix(
            [["Q_{11}", "Q_{12}"], ["Q_{21}", "Q_{22}"], ["Q_{31}", "Q_{32}"]]
        )
        sym_g = Matrix([["g_{1}"], ["g_{2}"]])

        sym_group = VGroup(sym_h, sym_eq, sym_Q, sym_g).arrange(RIGHT).scale(0.8)
        sym_label = Text("Formalización Algebraica", font_size=24, color=BLUE).next_to(
            sym_group, UP, buff=0.5
        )

        self.play(Write(sym_label), Write(sym_group))
        self.wait(2)

        # Step 2: Transition to Example from Slides
        num_h = Matrix([["15.3"], ["-0.24"], ["0"]])

        num_Q = Matrix([["1", "0"], ["0", "1"], ["0", "0"]])
        labeled_Q = self.create_labeled_matrix(
            num_Q,
            col_names=["CO2", "Petróleo Crudo (L)"],
            row_names=["GWP", "Agot. de Rec.", "Estrés hídrico"],
        )

        num_g = Matrix([["15.3"], ["-0.24"]])

        impact_group = (
            VGroup(labeled_Q, num_g, sym_eq.copy(), num_h)
            .arrange(RIGHT, buff=0.5)
            .scale(0.7)
        )
        impact_group.shift(DOWN * 0.5)

        num_label = Text(
            "Ejemplo Práctico (Matriz de Caracterización)", font_size=24, color=GREEN
        ).next_to(impact_group, UP, buff=0.8)

        num_h.get_entries().set_opacity(0)

        self.play(
            FadeOut(sym_label),
            ReplacementTransform(sym_group, impact_group),
            Write(num_label),
        )
        self.wait(1)

        # Step 3: Calculation Walkthrough
        r1 = SurroundingRectangle(num_Q.get_rows()[0], color=BLUE)
        c1 = SurroundingRectangle(num_g.get_columns()[0], color=BLUE)

        self.play(Create(r1), Create(c1))
        self.play(num_h.get_entries()[0].animate.set_opacity(1))
        self.wait(1)

        self.play(Transform(r1, SurroundingRectangle(num_Q.get_rows()[1], color=BLUE)))
        self.play(num_h.get_entries()[1].animate.set_opacity(1))
        self.wait(1)

        self.play(Transform(r1, SurroundingRectangle(num_Q.get_rows()[2], color=BLUE)))
        self.play(num_h.get_entries()[2].animate.set_opacity(1))
        self.wait(1)

        self.play(FadeOut(r1), FadeOut(c1))

        # Final conclusion
        final_text = Text(
            "Vector de Impactos Final (h)", font_size=28, color=YELLOW
        ).next_to(impact_group, DOWN, buff=0.8)
        self.play(Write(final_text))
        self.wait(4)
