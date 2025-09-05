from manim import *

# The example expansion
# It's a matrix
class CofactorExpansion(Scene):
    def construct(self):
        matrix = Matrix([
            [3, 5, 2],
            [4, 3, 0],
            [1, 2, 3]
        ])
        # Now the row we're going to expand
        row = matrix.get_rows()[1]

        # Defining this for later
        columns = matrix.get_columns()
        column1 = columns[0]
        column2 = columns[1]
        column3 = columns[2]
        e1 = column1[0]
        e2 = column2[0]
        e3 = column3[0]
        e4 = column1[1]
        e5 = column2[1]
        e6 = column3[1]
        e7 = column1[2]
        e8 = column2[2]
        e9 = column3[2]

        # Saves typing
        def copy_group(*items):
            return VGroup(*[m.copy() for m in items])


        # The ones that disappear
        first_expansion_leavers = VGroup(e1, e5, e6, e7)
        second_expansion_leavers = VGroup(e2, e4, e6, e8)
        third_expansion_leavers = VGroup(e3, e4, e5, e9)
        # Ones that stay (1st one is always the expanded element)
        first_exp_stay = VGroup(e4, e2, e3, e8, e9)
        second_exp_stay = VGroup(e5, e1, e3, e7, e9)
        third_exp_stay = VGroup(e6, e1, e2, e7, e8)
        submatrix1 = Matrix([
            [e2, e3],
            [e8, e9]
        ], element_to_mobject=lambda e: e.copy()).to_corner(UR)
        submatrix2 = Matrix([
            [e1, e3],
            [e7, e9]
        ], element_to_mobject=lambda e: e.copy())
        submatrix3 = Matrix([
            [e1, e2],
            [e7, e8]
        ], element_to_mobject=lambda e: e.copy())

        # Calculating the determinant Mobjects
        det1 = MathTex(r"4\cdot\det\left(\begin{bmatrix}5 & 2 \\ 2 & 3\end{bmatrix} \right)")
        # det1.to_corner(UR).get_parts_by_tex
        # self.add(det1)

        ################
        ### ANIMATION ##
        ################
        
        # Introduce matrix
        self.play(FadeIn(matrix))
        self.play(Circumscribe(row, buff=0.15, time_width=2))
        
        # Expanding the 2nd row 1st column
        self.play(Indicate(row[0], 1.5))
        self.play(
            Circumscribe(row, buff=0.15, time_width=2),
            Circumscribe(column1, buff=0.15, time_width=2)
        )
        self.play(FadeOut(first_expansion_leavers))
        # Introduce submatrix and move main matrix to the left
        # first_expansion_leavers.set_opacity(0)
        matrix.get_entries().set_opacity(0)
        self.play(
            TransformFromCopy(first_exp_stay[1:], submatrix1.get_entries()),
            FadeIn(submatrix1.get_brackets()),
            matrix.animate.to_edge(LEFT),
            # matrix.get_entries().animate.set_opacity(0),
            first_exp_stay[0].copy().animate.to_edge(UP),
            )
        self.play(Transform(submatrix1, det1))

# Only uncomment this to render a square
# config.pixel_width = 400
# config.pixel_height = 400

# Still image of cofactor sign grid
class CofactorGrid(MovingCameraScene):
    def construct(self):
        # Define the colours
        minus_sign_colour = color.GOLD
        plus_sign_colour = color.BLUE

        # Get plus and minus signs, and colour them
        minus = Line(LEFT, RIGHT).set_color(minus_sign_colour).scale(0.5)
        plus = VGroup(
            Line(DOWN, UP),
            Line(LEFT, RIGHT)
        ).set_color(plus_sign_colour).scale(0.5)

        # Put them into the table
        table = MobjectTable([
            [plus.copy(), minus.copy(), plus.copy()],
            [minus.copy(), plus.copy(), minus.copy()],
            [plus.copy(), minus.copy(), plus.copy()]
        ], include_outer_lines=False, v_buff=1, h_buff=1)

        self.add(table)

        # Resize the camera frame to fit the table exactly
        self.camera.auto_zoom([table], margin=1, animate=False)
        # self.camera.frame.scale_to_fit_width(table.width)
        # self.camera.frame.scale_to_fit_height(table.height)
        # self.camera.frame.move_to(table)
