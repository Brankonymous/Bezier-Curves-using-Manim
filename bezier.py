from manim import *

import numpy as np

class BezierIntro(Scene):
    def QuadraticBezier(self, dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot_123, line_12, line_23, line_123):
        self.play(
            Create(line_123),
            Create(mid_dot_12),
            Create(mid_dot_23)
        )
        self.wait()

        self.draw_upd = 0
        self.k = 1
        self.coeff = 0.007

        def quad_upd_t_0_1(mobject, dt):
            if self.t > 1 or self.t < 0:
                if self.t < 0 and self.draw_upd == 1:
                    self.draw_upd = 2
                if self.t > 1 and self.draw_upd == 2:
                    self.draw_upd = 3
                self.k *= -1

            if self.draw_upd == 3:
                return
            elif self.draw_upd == 2:
                self.t += self.k * self.coeff
            
            self.t += self.k * self.coeff
        
        def quad_upd_t_to_mid(mobject, dt):
            if self.t > 0.5:
                self.t -= self.coeff
        
        def mid_dot_12_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot1.get_center() + self.t * dot2.get_center())
        
        def mid_dot_23_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot2.get_center() + self.t * dot3.get_center())

        def mid_dot_123_updater(mobject, dt):
            mobject.move_to((1 - self.t) * mid_dot_12.get_center() + self.t * mid_dot_23.get_center())

        self.curve = VGroup()
        self.curve.add(Line(dot1.get_center(), dot1.get_center()))
        def get_curve():
            if self.draw_upd == 2:
                last_line = self.curve[-1]
                x = mid_dot_123.get_center()[0]
                y = mid_dot_123.get_center()[1]
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
                self.curve.add(new_line)

            return self.curve

        # Pocetak animacije
        dot1.add_updater(quad_upd_t_0_1)
        mid_dot_12.add_updater(mid_dot_12_updater)
        mid_dot_23.add_updater(mid_dot_23_updater)
        mid_dot_123.add_updater(mid_dot_123_updater)

        self.wait(6)

        self.play(
            dot2.animate.shift(2 * LEFT)
        )

        self.wait(6)

        self.play(
            dot2.animate.shift(2 * RIGHT)
        )
        
        self.draw_upd = 1
        curve_line = always_redraw(get_curve)
        self.add(curve_line)

        self.wait(6)

        dot1.remove_updater(quad_upd_t_0_1)

        dot1.add_updater(quad_upd_t_to_mid)
        self.play(
            Uncreate(self.curve)
        )
        self.wait(4)
        dot1.remove_updater(quad_upd_t_to_mid)
        self.t = 0.5

    def CubicBezier(self, dot1, dot2, dot3, dot4, mid_dot_12, mid_dot_23, mid_dot_34, mid_dot_123, mid_dot_234, mid_dot_1234,
                        line_12, line_23, line_34, line_123, line_234, line_1234):
        self.curve_1 = VGroup()
        self.curve_1.add(Line(dot1.get_center(), dot1.get_center()))
        def get_cubic_curve():
            if self.draw_upd == 2:
                last_line = self.curve_1[-1]
                x = mid_dot_1234.get_center()[0]
                y = mid_dot_1234.get_center()[1]
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
                self.curve_1.add(new_line)

            return self.curve_1


        self.draw_upd = 0
        self.k = 1
        self.coeff = 0.007
        self.t = 0.5

        def cubic_upd_t_0_1(mobject, dt):
            if self.t > 1 or self.t < 0:
                if self.t < 0 and self.draw_upd == 1:
                    self.draw_upd = 2
                if self.t > 1 and self.draw_upd == 2:
                    self.draw_upd = 3
                self.k *= -1

            if self.draw_upd == 3:
                return
            elif self.draw_upd == 2:
                self.t += self.k * self.coeff
            
            self.t += self.k * self.coeff
        
        def cubic_upd_t_to_mid(mobject, dt):
            if self.t > 0.5:
                self.t -= self.coeff
        
        # Vec imamo mid_dot_12_updater, mid_dot_23_updater i mid_dot_123_updater
        def mid_dot_34_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot3.get_center() + self.t * dot4.get_center())
        def mid_dot_234_updater(mobject, dt):
            mobject.move_to((1 - self.t) * mid_dot_23.get_center() + self.t * mid_dot_34.get_center())
        def mid_dot_1234_updater(mobject, dt):
            mobject.move_to((1 - self.t) * mid_dot_123.get_center() + self.t * mid_dot_234.get_center())

        mid_dot_34.add_updater(mid_dot_34_updater)
        mid_dot_234.add_updater(mid_dot_234_updater)
        mid_dot_1234.add_updater(mid_dot_1234_updater)
        dot1.add_updater(cubic_upd_t_0_1)


        self.wait(6)

        self.draw_upd = 1
        curve_line_1 = always_redraw(get_cubic_curve)
        self.add(curve_line_1)

        self.wait(6)

        dot1.remove_updater(cubic_upd_t_0_1)
        self.play(
            Uncreate(self.curve_1),
            dot1.animate.shift(2 * UP ),
            dot4.animate.shift(2 * UP ),
            dot3.animate.shift(4 * DOWN),
            run_time=1
        )

        self.draw_upd = 1
        dot1.add_updater(cubic_upd_t_0_1)

        # 2 Linija
        self.curve_2 = VGroup()
        self.curve_2.add(Line(dot1.get_center(), dot1.get_center()))
        def get_cubic_curve_2():
            if self.draw_upd == 2:
                last_line = self.curve_2[-1]
                x = mid_dot_1234.get_center()[0]
                y = mid_dot_1234.get_center()[1]
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
                self.curve_2.add(new_line)

            return self.curve_2
        
        curve_line_2 = always_redraw(get_cubic_curve_2)
        self.add(curve_line_2)

        self.wait(6)

        self.play(Uncreate(self.curve_2))

    def construct(self):
        # Ispis naslova
        text_intro = Text("Bézier-ove krive", t2c={"Bézier": RED, " krive": YELLOW})
        self.play(
            Create(text_intro),
            run_time=0.6
        )
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
        mid_dot_123 = Dot().set_z_index(90)
        mid_dot_123.set_fill(BLACK)
        mid_dot_123.set_stroke(BLUE, width=4)
        mid_dot_123_tex = MathTex("P_{mid}")
        mid_dot_123_tex.scale(0.8)
        mid_dot_123_tex.add_updater(
                lambda m: m.next_to(mid_dot_123, DOWN + 0.2 * RIGHT)
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
        mid_dot_123_equation = MathTex("P_{mid} = (1-t)*P_0 + t*P_1", color=BLUE)
        mid_dot_123_equation.scale(0.9),
        mid_dot_123_equation.shift(3.5*LEFT + 2.7*UP)
        mid_dot_123_eq_framebox = SurroundingRectangle(mid_dot_123_equation)

        self.play(
                Create(line_12),
                Create(mid_dot_123),
                Create(dot1_text),
                Create(dot2_text),
                Create(mid_dot_123_tex)
            )

        self.wait()
        self.play(
            Transform(text_intro, mid_dot_123_equation)
        )
        self.wait()

        # P_MID = (1 - t) * P[0] + t * P[1]
        self.t = 0.5

        # mid_label - prati sredisnju tacku i ispisuje vrednost
        mid_text, mid_equal, mid_number = mid_label = VGroup(
            Text("t", slant=ITALIC),
            Text(" = "),
            DecimalNumber(
                0.50,
                num_decimal_places=2
            )
        )
        mid_label.arrange(RIGHT)
        mid_label.scale(0.8)

        mid_label.add_updater(
                lambda m: m.next_to(mid_dot_123, UP + LEFT)
            )

        # Updater sredisnje tacke
        mid_number.add_updater(lambda m: m.set_value(
                (mid_dot_123.get_center()[0] - dot1.get_center()[0]) / (dot2.get_center()[0] - dot1.get_center()[0])
            ))

        self.play(
            Create(mid_label),
            Create(mid_dot_123_eq_framebox)
        )
        self.wait(2)

        # Animacije kretanja sredisnje tacke
        mid_dot_123_x = ValueTracker(0)
        mid_dot_123_y = ValueTracker(0)
        mid_dot_123.add_updater(lambda z: z.set_x(mid_dot_123_x.get_value()))
        mid_dot_123.add_updater(lambda z: z.set_y(mid_dot_123_y.get_value()))

        t = 0.7
        self.play(
            mid_dot_123_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_123_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=2,
            rate_func=there_and_back
        )

        t = 0.15
        self.play(
            mid_dot_123_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_123_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
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
            Uncreate(mid_dot_123_eq_framebox),
            Uncreate(mid_dot_123_tex),
            Uncreate(mid_dot_123_equation),
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
        mid_dot_12.set_fill(BLACK)
        mid_dot_12.set_stroke(YELLOW, width=4)

        mid_dot_23 = Dot(color=BLUE).shift((dot2.get_center() + dot3.get_center()) / 2).set_z_index(90)
        mid_dot_23.set_fill(BLACK)
        mid_dot_23.set_stroke(RED, width=4)

        line_123 = Line(start=mid_dot_12.get_center(), end=mid_dot_23.get_center(), color=GREY)
        line_123.add_updater(lambda z: z.become(Line(mid_dot_12.get_center(), mid_dot_23.get_center(), color=GREY)))

        mid_dot_123.set_value((mid_dot_12.get_center() + mid_dot_23.get_center()) / 2)


        # Animacija kvadratnog Bezijera
        self.QuadraticBezier(dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot_123, line_12, line_23, line_123)


        # Dodavanje potrebnih tacaka i linije za Kubnog bezier-a

        line_34 = Line(start=dot3.get_center(), end=dot4.get_center(), color=GREY)
        line_34.add_updater(lambda z: z.become(Line(dot3.get_center(), dot4.get_center(), color=GREY)))

        dot4.shift(3 * RIGHT + 2 * DOWN)

        self.play(
            dot2.animate.shift(2 * LEFT),
            dot3.animate.shift(4 * UP + LEFT),
            dot3_text.animate.add_updater(
                lambda m: m.next_to(dot3, UP)
            ),
            Create(line_34),
            Create(dot4),
            Create(dot4_text)
        )
        dot3_text.add_updater(
                lambda m: m.next_to(dot3, UP)
            )

        mid_dot_34 = Dot().shift((dot3.get_center() + dot4.get_center()) / 2).set_z_index(90)
        mid_dot_34.set_fill(BLACK)
        mid_dot_34.set_stroke(ORANGE, width=4)

        line_234 = Line(start=mid_dot_23.get_center(), end=mid_dot_34.get_center(), color=GREY)
        line_234.add_updater(lambda z: z.become(Line(mid_dot_23.get_center(), mid_dot_34.get_center(), color=GREY)))

        mid_dot_234 = Dot().shift((mid_dot_23.get_center() + mid_dot_34.get_center()) / 2).set_z_index(80)
        mid_dot_234.set_fill(BLACK)
        mid_dot_234.set_stroke(MAROON, width=4)

        self.play(
            Create(mid_dot_34),
            Create(line_234),
            Create(mid_dot_234)
        )


        mid_dot_1234 = Dot().shift((mid_dot_123.get_center() + mid_dot_234.get_center()) / 2).set_z_index(80)
        mid_dot_1234.set_fill(BLACK)
        mid_dot_1234.set_stroke(PINK, width=4)

        line_1234 = Line(start=mid_dot_123.get_center(), end=mid_dot_234.get_center(), color=GREY)
        line_1234.add_updater(lambda z: z.become(Line(mid_dot_123.get_center(), mid_dot_234.get_center(), color=GREY)))

        self.play(
            Create(mid_dot_1234),
            Create(line_1234)
        )

        self.wait(1)

        # Animacija kubnog Bezijera
        self.CubicBezier(dot1, dot2, dot3, dot4, mid_dot_12, mid_dot_23, mid_dot_34, mid_dot_123, mid_dot_234, mid_dot_1234,
                        line_12, line_23, line_34, line_123, line_234, line_1234)

        self.wait()

class BezierIntro2(Scene):
    def construct(self):
        dot = Dot()
        dot.set_fill(BLACK)
        dot.set_stroke(PURPLE, width=4)

        self.play(Create(dot))
        dot.set_value([0, 1, 0])
        self.play(
            dot.animate.set_value([0, 1, 0])
        )
'''


'''