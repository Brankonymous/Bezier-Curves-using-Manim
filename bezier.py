from manim import *

import numpy as np

class BezierIntro(Scene):
    def QuadraticBezier(self, dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot, line_12, line_23, line_mid_12):
        self.play(
            Create(line_mid_12),
            Create(mid_dot_12),
            Create(mid_dot_23)
        )
        self.wait()

        self.k = 1
        self.coeff = 0.005

        def upd_time(mobject, dt):
            if self.k < 2 and (self.t > 0.75 or self.t < 0.25):
                self.k *= -1

            if self.k == 2 and self.t > 0:
                self.t -= self.coeff
            elif self.k == 2 and self.t <= 0:
                self.k = 3
                self.t += 2 * self.coeff
            elif self.k == 3:
                if self.t < 1:
                    self.t += 2 * self.coeff
            else:
                self.t += self.k * self.coeff
        
        def mid_dot_12_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot1.get_center() + self.t * dot2.get_center())
        
        def mid_dot_23_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot2.get_center() + self.t * dot3.get_center())

        def mid_dot_updater(mobject, dt):
            mobject.move_to((1 - self.t) * mid_dot_12.get_center() + self.t * mid_dot_23.get_center())

        dot1.add_updater(upd_time)
        mid_dot_12.add_updater(mid_dot_12_updater)
        mid_dot_23.add_updater(mid_dot_23_updater)
        mid_dot.add_updater(mid_dot_updater)

        self.wait(0.5)

        self.play(
            dot2.animate.shift(2 * LEFT)
        )

        self.wait(1)

        self.play(
            dot2.animate.shift(2 * RIGHT)
        )

        self.curve = VGroup()
        self.curve.add(Line(dot1.get_center(), dot1.get_center()))
        def get_curve():
            if self.k == 3:
                last_line = self.curve[-1]
                x = mid_dot.get_center()[0]
                y = mid_dot.get_center()[1]
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
                self.curve.add(new_line)

            return self.curve
        
        self.k = 2
        curve_line = always_redraw(get_curve)
        self.add(curve_line)

        self.wait(5)
        dot1.remove_updater(upd_time)

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
        dot1 = Dot().set_z_index(100)
        dot2 = Dot().set_z_index(100)
        dot3 = Dot().set_z_index(100)
        dot4 = Dot().set_z_index(100)

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
        
        dot3_text = MathTex("P_3")
        dot3_text.scale(0.8)
        dot3_text.add_updater(
                lambda m: m.next_to(dot3, RIGHT)
            )

        dot4_text = MathTex("P_4")
        dot4_text.scale(0.8)
        dot4_text.add_updater(
                lambda m: m.next_to(dot4, RIGHT)
            )

        # Podesavanje sredisnje tacke
        mid_dot = Dot().set_z_index(90)
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

        # Definisanje linije i mid_line_12 koja prati sredisnju tacku izmedju tacaka 1 i 2
        line_12 = Line(start=dot1.get_center(), end=dot2.get_center(), color=GREY)
        line_12.add_updater(lambda z: z.become(Line(dot1.get_center(), dot2.get_center(), color=GREY)))

        # Jednacina sredisnje tacke
        mid_dot_equation = MathTex("P_{mid} = (1-t)*P_0 + t*P_1", color=BLUE)
        mid_dot_equation.scale(0.9),
        mid_dot_equation.shift(3.5*LEFT + 2.7*UP)
        mid_dot_eq_framebox = SurroundingRectangle(mid_dot_equation)

        self.play(
                Create(line_12),
                Create(mid_dot),
                Create(dot1_text),
                Create(dot2_text),
                Create(mid_dot_tex)
            )

        self.wait()
        self.play(
            Transform(text_intro, mid_dot_equation)
        )
        self.wait()

        # P_MID = (1 - t) * P[0] + t * P[1]
        self.t = 0.5

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
        self.wait(2)

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
            run_time=2.5,
            rate_func=there_and_back
        )
        t = 0.5
        self.wait()


        # Brisanje jednacina, indikatora i shiftovanje postojecih tacaka
        dot3.shift(3 * RIGHT + 2 * DOWN)

        line_23 = Line(start=dot2.get_center(), end=dot3.get_center(), color=GREY)
        line_23.add_updater(lambda z: z.become(Line(dot2.get_center(), dot3.get_center(), color=GREY)))
        
        self.play(
            Uncreate(mid_label),
            Uncreate(mid_dot_eq_framebox),
            Uncreate(mid_dot_tex),
            Uncreate(mid_dot_equation),
            Uncreate(text_intro),

            Create(dot3),
            Create(dot3_text),
            Create(line_23),
            dot2_text.animate.add_updater(
                lambda m: m.next_to(dot2, UP)
            ),
            dot2.animate.shift(3 * LEFT),
        )
        dot2_text.add_updater(
                lambda m: m.next_to(dot2, UP)
            )

        

        # Dodavanje sredisnjih tacaka
        mid_dot_12 = Dot(color=BLUE).shift((dot1.get_center() + dot2.get_center()) / 2)

        mid_dot_23 = Dot(color=BLUE).shift((dot2.get_center() + dot3.get_center()) / 2)

        line_mid_12 = Line(start=mid_dot_12.get_center(), end=mid_dot_23.get_center(), color=GREY)
        line_mid_12.add_updater(lambda z: z.become(Line(mid_dot_12.get_center(), mid_dot_23.get_center(), color=GREY)))

        mid_dot.set_value((mid_dot_12.get_center() + mid_dot_23.get_center()) / 2)


        # Animacija kvadratnog Bezijera
        self.QuadraticBezier(dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot, line_12, line_23, line_mid_12)



        self.wait()

class BezierIntro2(Scene):
    def construct(self):
        a = 2
        error(a)
'''


'''