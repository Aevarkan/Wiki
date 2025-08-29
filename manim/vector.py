from manim import *

class VectorGrid(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        x_coord = ValueTracker(1)
        y_coord = ValueTracker(-3)
        x_offset = ValueTracker(1)
        y_offset = ValueTracker(0)

        vec = Vector([x_coord.get_value(), y_coord.get_value()])
        vec.add_updater(lambda vec: vec.put_start_and_end_on(ORIGIN, [x_coord.get_value(), y_coord.get_value(), 0]))

        label = always_redraw(lambda: vec.coordinate_label().move_to(vec.get_end() + RIGHT * x_offset.get_value() + UP * y_offset.get_value()))
        self.add(plane, vec, label)

        self.wait(2)
        self.play(
            x_coord.animate.set_value(-2),
            y_coord.animate.set_value(1),
            x_offset.animate.set_value(1.1),
            y_offset.animate.set_value(0.9),
            run_time=1.5
            )

        self.wait(1.5)
        self.play(
            x_coord.animate.set_value(1),
            y_coord.animate.set_value(2),
            x_offset.animate.set_value(1),
            y_offset.animate.set_value(0),
            run_time=1.5
            )
        self.wait(1.5)
        self.play(
            x_coord.animate.set_value(1),
            y_coord.animate.set_value(-3),
            run_time=1.5
            )
        self.wait(2)

    # This can be made SO much shorter, see above
    # def construct(self):
    #     plane = NumberPlane()
    #     self.add(plane)

    #     # Now we want an arrow that moves around
    #     x_coord = ValueTracker(1)
    #     y_coord = ValueTracker(-3)

    #     # The arrow itself
    #     arrow = Arrow(ORIGIN, [x_coord.get_value(), y_coord.get_value(), 0], buff=0)
    #     arrow.add_updater(lambda arrow: arrow.put_start_and_end_on(ORIGIN, [x_coord.get_value(), y_coord.get_value(), 0]))

    #     self.add(arrow)


    #     self.wait(2)
    #     self.play(
    #         x_coord.animate.set_value(-2),
    #         y_coord.animate.set_value(1),
    #         run_time=1.5
    #         )

    #     self.wait(1.5)
    #     self.play(
    #         x_coord.animate.set_value(1),
    #         y_coord.animate.set_value(2),
    #         run_time=1.5
    #         )
    #     self.wait(2)