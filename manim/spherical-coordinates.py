from manim import *

# 2D Case first, then generalise to 3D
class PolarCoordinates(Scene):
    def construct(self):
        ax = Axes()
        self.add(ax)


        # Configuration
        point_initial_pos = [1, 2]
        point_final_pos = [4, -1]
        arc_radius = 2

        # Vertical Axis (Must be a line to get an angle)
        vertical = Line(ORIGIN, UP*3)

        # Add the point
        dot = Dot(ax.c2p(*point_initial_pos))
        
        # Add the line that tracks it
        line = Line(ORIGIN, dot.get_center(), color=BLUE)
        line.add_updater(lambda line: line.put_start_and_end_on(ORIGIN, dot.get_center()))

        # The polar angle
        angle = always_redraw(
            lambda: Angle(
                vertical,
                line,
                radius=1,
                other_angle=True
            )
        )
        def make_label():
            center = angle.get_center()                 # midpoint of the arc
            bisector_dir = normalize(center - ORIGIN)   # direction from origin
            radial_distance = arc_radius + 0.1          # push label outward
            return MathTex(r"\theta").move_to(bisector_dir * radial_distance)

        angle_label = always_redraw(make_label)

        # Play the animation
        self.play(DrawBorderThenFill(dot))
        self.play(Create(line))
        self.play(Create(angle), Write(angle_label))

        # Move the dot
        self.play(dot.animate.move_to(ax.c2p(*point_final_pos)))

        self.wait(2)


class SphericalCoordinates(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=0)

        # focus_point = Dot()
        # focus_point.move_to([10, 0, 0])

        # Reference Pointer
        point = Point()

        axes = ThreeDAxes()
        self.add(axes)

        sphere = Sphere()
        self.set_camera_orientation()
        self.play(
            Create(sphere)
        )

        # self.add(line)

        
        def get_line_to_point():
            return Line(ORIGIN, point)

        line = always_redraw(get_line_to_point)

        self.play(
            Create(line)
        )

        # Dot().add_updater()
        # t = ValueTracker(0)

        # Move the pointer
        def move_point(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))
            mob.move_to([t.get_value(), t.get_value(), t.get_value()])

        # # Make a movable dot
        # dot = Dot([2, 1, 0], color=YELLOW)

        # # Make a line that always connects (0,0,0) to the dot
        # line = Line(ORIGIN, dot.get_center(), color=BLUE)

        # # Add an updater so the line follows the dot
        # line.add_updater(lambda l: l.put_start_and_end_on(ORIGIN, dot.get_center()))

        # # Add to scene
        # self.add(dot, line)

        # # Animate the dot moving around
        # self.play(dot.animate.move_to([3, 2, 0]), run_time=2)
        # self.play(dot.animate.move_to([-2, 1, 0]), run_time=2)
        # self.play(dot.animate.move_to([1, -2, 0]), run_time=2)
        # self.wait()


        # point.add_updater(move_point)

        # self.play(t.animate.set_value(10))

        # self.play(
        #     point.animate.
        # )

        

        # self.move_camera(frame_center=focus_point)
        # self.move_camera(frame_center=[5, 5, 5])
        self.move_camera(phi=45 * DEGREES)
        # self.move_camera(theta= * DEGREES)
        self.wait(1)
        self.move_camera(theta=-45 * DEGREES)

        self.play(point.animate.move_to([2, 2, 2]))
        # self.wait(1)

        # pointer.move_to([2, 2, 2])
        # line.position_tip(pointer)

        self.wait(3)