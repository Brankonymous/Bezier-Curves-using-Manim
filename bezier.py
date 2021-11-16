from manimlib import *
import numpy as np

class DotToLine(Scene):
    def construct(self):

        # Konstrukcija tacaka i linije
        dot1 = Dot()
        dot2 = Dot()

        mid_dot = Dot()
        mid_dot.set_fill(BLACK)
        mid_dot.set_stroke(BLUE, width=4)

        self.play(
                ShowCreation(dot1),
                ShowCreation(dot2)
                )
        
        self.wait()

        self.play(
                dot1.animate.shift(3 * LEFT + 2 * DOWN),
                dot2.animate.shift(3 * RIGHT + 2 * UP)
            )

        line = Line(start=dot1, end=dot2, color=GREY)
        mid_line = Line(start=dot1, end=mid_dot, color=GREY)
        self.play(
                ShowCreation(line),
                ShowCreation(mid_dot),
            )

        self.wait()

        # 2 tacke
        brace = always_redraw(Brace, mid_dot, UP)
        brace.rotate(np.arctan(2/3))

        text, number = label = VGroup(
            Text("t = "),
            DecimalNumber(
                0.50,
                show_ellipsis=True,
                num_decimal_places=2
            )
        )
        label.arrange(RIGHT)

        always(label.next_to, brace, UP)
        f_always(number.set_value, mid_line.get_width)

        self.add(mid_line, brace, label)

        dot1_x = dot1.get_width()
        dot1_y = dot1.get_y()
        dot2_x = dot2.get_width()
        dot2_y = dot2.get_y()
        print(dot1_x, dot1_y)


        self.play(
            mid_dot.animate.shift(0.3 * dot1 + 0.7 * dot2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.play(
            mid_dot.animate.shift(0.6 * dot1 + 0.4 * dot2),
            rate_func=there_and_back,
            run_time=1.5,
        )
        self.wait()




