from manim import *

import numpy as np

class BezierIntro(Scene):
    def construct(self):
        # Hold na 1s
        self.wait(0.5)

        # Ispis naslova
        text_intro = Text("Bézier-ove krive", t2c={"Bézier": RED, " krive": YELLOW})
        self.play(Create(text_intro))
        self.wait()

        self.play(
            text_intro.animate.scale(0.3),
            text_intro.animate.shift(3.5*LEFT + 2.6*UP)
        )

        # Konstrukcija tacaka
        dot1 = Dot()
        dot2 = Dot()

        # Label njihovih imena
        dot1_text = MathTex("P_1")
        dot1_text.scale(0.8)
        dot1_text.add_updater(
                lambda m: m.next_to(dot1, LEFT)
            )
        dot2_text = MathTex("P_2")
        dot2_text.scale(0.8)
        dot2_text.add_updater(
                lambda m: m.next_to(dot2, RIGHT)
            )

        # Podesavanje sredisnje tacke
        mid_dot = Dot()
        mid_dot.set_fill(BLACK)
        mid_dot.set_stroke(BLUE, width=4)
        mid_dot_tex = MathTex("P_{mid}")
        mid_dot_tex.scale(0.8)
        mid_dot_tex.add_updater(
                lambda m: m.next_to(mid_dot, DOWN)
            )

        # Pokretanje animacija
        self.play(
                Create(dot1),
                Create(dot2)
                )
        
        self.wait()

        self.play(
                dot1.animate.shift(3 * LEFT + 2 * DOWN),
                dot2.animate.shift(3 * RIGHT + 2 * UP)
            )

        # Definisanje linije i mid_line koja prati sredisnju tacku
        line = Line(start=dot1.get_center(), end=dot2.get_center(), color=GREY)
        mid_line = Line(start=dot1.get_center(), end=mid_dot.get_center(), color=GREY)

        # Jednacina sredisnje tacke
        mid_dot_equation = MathTex("P_{mid} = (1-t)*P_0 + t*P_1", color=BLUE)
        mid_dot_equation.scale(0.9),
        mid_dot_equation.shift(3.5*LEFT + 2.7*UP)
        mid_dot_eq_framebox = SurroundingRectangle(mid_dot_equation)

        self.play(
                Create(line),
                Create(mid_dot),
                Create(dot1_text),
                Create(dot2_text),
                Create(mid_dot_tex)
            )

        self.wait()
        self.play(
            Transform(text_intro, mid_dot_equation)
        )
        self.wait(2)

        # P_MID = (1 - t) * P[0] + t * P[1]
        t = 0.5

        # mid_label - prati sredisnju tacku i ispisuje vrednost
        mid_text, mid_number = mid_label = VGroup(
            Text("t = "),
            DecimalNumber(
                0.50,
                num_decimal_places=2
            )
        )
        mid_label.arrange(RIGHT)
        mid_label.scale(0.8)

        mid_label.add_updater(
                lambda m: m.next_to(mid_dot, UP + LEFT)
            )

        # Updater sredisnje tacke
        mid_number.add_updater(lambda m: m.set_value(
                (mid_dot.get_center()[0] - dot1.get_center()[0]) / (dot2.get_center()[0] - dot1.get_center()[0])
            ))

        self.play(
            Create(mid_label),
            Create(mid_dot_eq_framebox)
        )
        self.wait(3)

        # Animacije kretanja sredisnje tacke
        mid_dot_x = ValueTracker(0)
        mid_dot_y = ValueTracker(0)
        mid_dot.add_updater(lambda z: z.set_x(mid_dot_x.get_value()))
        mid_dot.add_updater(lambda z: z.set_y(mid_dot_y.get_value()))

        t = 0.7
        self.play(
            mid_dot_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=2,
            rate_func=there_and_back
        )

        t = 0.15
        self.play(
            mid_dot_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=3,
            rate_func=there_and_back
        )
        self.wait()

        self.play(
            Uncreate(mid_label),
            Uncreate(mid_dot),
            Uncreate(mid_dot_eq_framebox),
            Uncreate(mid_dot_tex)
        )

        self.wait()

'''


'''