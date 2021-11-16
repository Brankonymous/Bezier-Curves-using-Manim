from manim import *

import numpy as np

class DotToLine(Scene):
    def construct(self):
        # Hold na 2s
        self.wait(1)

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
        mid_line = Line(start=dot1.get_center(), end=mid_dot.get_center(), color=GREY)
        self.play(
                Create(line),
                Create(mid_dot),
            )

        self.wait()

        # 2 dots
        mid_dot_brace = BraceBetweenPoints(dot1.get_center(), mid_dot.get_center(), [-2., 3., 0])
        mid_dot_brace.add_updater(lambda z: z.become(BraceBetweenPoints(dot1.get_center(), mid_dot.get_center(), [-2., 3., 0])))

        mid_text, t = label = VGroup(
            Text("t = "),
            DecimalNumber(
                0.50,
                show_ellipsis=True,
                num_decimal_places=2
            )
        )
        always(label.next_to, mid_dot_brace)

        self.add(label)
        self.play(
            Create(mid_dot_brace)
        )

        mid_dot_x = ValueTracker(0)
        mid_dot_y = ValueTracker(0)
        mid_dot.add_updater(lambda z: z.set_x(mid_dot_x.get_value()))
        mid_dot.add_updater(lambda z: z.set_y(mid_dot_y.get_value()))

        t = 0.7
        self.play(
            mid_dot_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=1.5,
            rate_func=there_and_back
        )

        t = 0.35
        self.play(
            mid_dot_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(3)




