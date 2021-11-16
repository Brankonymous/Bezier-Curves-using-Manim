from manim import *

import numpy as np

class DotToLine(Scene):
    def construct(self):
        # Hold na 2s
        self.wait(2)

        # Konstrukcija tacaka i linije
        dot1 = Dot()
        dot2 = Dot()
        print(dot1.width, dot2.width)

        mid_dot = Dot()
        mid_dot.set_fill(BLACK)
        mid_dot.set_stroke(BLUE, width=4)

        self.play(
                Create(dot1),
                Create(dot2)
                )
        
        self.wait()

        self.play(
                dot1.animate.shift(3 * LEFT + 2 * DOWN),
                dot2.animate.shift(3 * RIGHT + 2 * UP)
            )

        line = Line(start=dot1.get_center(), end=dot2.get_center(), color=GREY)
        self.play(
                Create(line),
                Create(mid_dot),
            )

        self.wait()

        # 2 tacke

        mid_dot_x = ValueTracker(0)
        mid_dot_y = ValueTracker(0)
        mid_dot.add_updater(lambda z: z.set_x(mid_dot_x.get_value()))
        mid_dot.add_updater(lambda z: z.set_y(mid_dot_y.get_value()))

        t = 0.7
        self.play(
            mid_dot_x.animate.set_value(t * dot1.get_center()[0] + (1-t) * dot2.get_center()[0]),
            mid_dot_y.animate.set_value(t * dot1.get_center()[1] + (1-t) * dot2.get_center()[1]),
            run_time=1.5,
            rate_func=there_and_back
        )

        t = 0.35
        self.play(
            mid_dot_x.animate.set_value(t * dot1.get_center()[0] + (1-t) * dot2.get_center()[0]),
            mid_dot_y.animate.set_value(t * dot1.get_center()[1] + (1-t) * dot2.get_center()[1]),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(3)




