from manim import *

import numpy as np

'''
Created with ManimCE library

Run with command:
manim -pqh --fps 60 bezier.py BezierIntro

1920 x 1080 quality with 60fps and preview
render with -pql for lower quality
render with -pqk for 4K quality

DON'T CHANGE FPS - animations depends on it
'''

class BezierIntro(Scene):

    def QuadraticBezier(self, dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot_123, line_12, line_23, line_123, mid_dot_12_text, mid_dot_23_text):

        # LaTex Ime
        quadratic_bezier_name = Text("Kvadratna Bézier-ova kriva", t2c={"Kvadratna Bézier-ova kriva": YELLOW}).scale(0.8).shift(2.85 * DOWN)

        # Pisanje t_val updatera sa gornje-desne strane ekrana
        self.t_val_text, self.t_val_equal, self.t_val_number = self.t_val_label = VGroup(
            Text("t", slant=ITALIC),
            Text(" = "),
            DecimalNumber(
                0.50,
                num_decimal_places=2
            )
        )
        self.t_val_text.scale(0.9)
        self.t_val_equal.scale(0.9)
        self.t_val_label.arrange(RIGHT).scale(0.7).shift(3 * UP + 4 * RIGHT)

        self.t_val_number.add_updater(lambda m: m.set_value(self.t))

        # Ispisivanje jednacina...
        self.quadratic_equations = VGroup()
        
        self.quadratic_mid_dot_12_equation = MathTex("A = lerp(t, P_0, P_1)", color=WHITE, substrings_to_isolate= {"A", "t"})
        self.quadratic_mid_dot_23_equation = MathTex("B = lerp(t, P_1, P_2)", color=WHITE, substrings_to_isolate= {"B", "t"})
        self.quadratic_mid_dot_123_equation = MathTex("P = lerp(t, A, B)", color=WHITE, substrings_to_isolate= {"P", "t", "A", "B"}).scale(0.8)

        self.quadratic_mid_dot_12_equation.set_color_by_tex("A", YELLOW)
        self.quadratic_mid_dot_12_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_mid_dot_23_equation.set_color_by_tex("B", RED)
        self.quadratic_mid_dot_23_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_mid_dot_123_equation.set_color_by_tex("P", BLUE)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("A", YELLOW)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("B", RED)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_equations += self.quadratic_mid_dot_12_equation
        self.quadratic_equations += self.quadratic_mid_dot_23_equation

        self.quadratic_equations.arrange(DOWN, aligned_edge=LEFT).scale(0.8).shift(2.5 * UP + 4.5 * LEFT)
        quadratic_equations_framebox = SurroundingRectangle(self.quadratic_equations)

        # Definisanje kretanja bezier-a
        self.draw_upd = 0
        self.k = 1
        self.coeff = 0.007

        # Update t-a frame po frame
        def quad_upd_t_0_1(mobject, dt):
            if self.t > 1:
                self.t = 1.00001
            if self.t < 0:
                self.t = -0.0001

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
            if (self.t > (0.5 - self.coeff)) and (self.t < (0.5 + self.coeff)):
                self.t = 0.5 
            elif self.t > 0.5:
                self.t -= self.coeff
            elif self.t < 0.5:
                self.t += self.coeff
        
        # Transformisanje tacke u odnosu na t
        def mid_dot_12_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot1.get_center() + self.t * dot2.get_center())
        
        def mid_dot_23_updater(mobject, dt):
            mobject.move_to((1 - self.t) * dot2.get_center() + self.t * dot3.get_center())

        def mid_dot_123_updater(mobject, dt):
            mobject.move_to((1 - self.t) * mid_dot_12.get_center() + self.t * mid_dot_23.get_center())
        
        # Kreiranje jednacina i objekata
        self.play(
            Create(line_123),
            Create(mid_dot_12),
            Create(mid_dot_23),
            Create(mid_dot_12_text),
            Create(mid_dot_23_text),
            Create(self.quadratic_equations),
            Create(self.t_val_label),
            Create(quadratic_equations_framebox)
        )
        self.wait()

        # Pocetak animacije sa 2 linije
        dot1.add_updater(quad_upd_t_0_1)
        mid_dot_12.add_updater(mid_dot_12_updater)
        mid_dot_23.add_updater(mid_dot_23_updater)

        self.play(
            Uncreate(mid_dot_12_text),
            Uncreate(mid_dot_23_text)
        )
        self.wait(3)

        dot1.remove_updater(quad_upd_t_0_1)
        dot1.add_updater(quad_upd_t_to_mid)

        self.wait()
        self.play(
            Uncreate(quadratic_equations_framebox)
        )

        self.play(
            mid_dot_123.animate.restore(),
            self.quadratic_equations.animate.add(self.quadratic_mid_dot_123_equation).arrange(DOWN, aligned_edge=LEFT).shift(2.5 * UP + 4.5 * LEFT)
        )
        
        dot1.remove_updater(quad_upd_t_to_mid)
        dot1.add_updater(quad_upd_t_0_1)

        mid_dot_12.add_updater(mid_dot_12_updater)
        mid_dot_23.add_updater(mid_dot_23_updater)
        mid_dot_123.add_updater(mid_dot_123_updater)

        # Pokret linije
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

        quadratic_equations_framebox_upd = SurroundingRectangle(self.quadratic_equations[2])
        self.play(
            Create(quadratic_equations_framebox_upd)
        )
        self.wait()

        self.play(
            dot2.animate.shift(2 * LEFT)
        )

        self.wait(2)

        self.play(
            dot2.animate.shift(2 * RIGHT)
        )
        
        # Pocetak crtanja linije
        self.draw_upd = 1
        curve_line = always_redraw(get_curve)
        self.add(curve_line)

        self.wait(2)
        self.play(Create(quadratic_bezier_name))
        self.wait(2)

        # Zavrsetak i brisanje neophodnih stvari, vracanje na normalu
        dot1.remove_updater(quad_upd_t_0_1)

        dot1.add_updater(quad_upd_t_to_mid)
        self.play(
            Uncreate(self.curve),
            Uncreate(quadratic_bezier_name),
            Uncreate(self.quadratic_equations),
            Uncreate(quadratic_equations_framebox_upd)
        )
        self.wait()
        dot1.remove_updater(quad_upd_t_to_mid)
        self.t = 0.5

    def CubicBezier(self, dot1, dot2, dot3, dot4, mid_dot_12, mid_dot_23, mid_dot_34, mid_dot_123, mid_dot_234, mid_dot_1234,
                        line_12, line_23, line_34, line_123, line_234, line_1234, dot1_text, dot2_text, dot3_text, dot4_text,
                        mid_dot_12_text, mid_dot_23_text, mid_dot_34_text, mid_dot_123_text, mid_dot_234_text, mid_dot_1234_text):
        # LaTex Ime
        cubic_bezier_name = Text("Kubna Bézier-ova kriva", t2c={"Kubna Bézier-ova kriva": YELLOW}).scale(0.8).shift(2.85 * DOWN)

        # Ispisivanje jednacina... ponovo
        self.cubic_equations = VGroup()

        self.cubic_mid_dot_12_equation = MathTex("A = lerp(t, P_0, P_1)", color=WHITE, substrings_to_isolate= {"A", "t"})
        self.cubic_mid_dot_12_equation.set_color_by_tex("A", YELLOW)
        self.cubic_mid_dot_12_equation.set_color_by_tex("t", GRAY_BROWN)

        self.cubic_mid_dot_23_equation = MathTex("B = lerp(t, P_1, P_2)", color=WHITE, substrings_to_isolate= {"B", "t"})
        self.cubic_mid_dot_23_equation.set_color_by_tex("B", RED)
        self.cubic_mid_dot_23_equation.set_color_by_tex("t", GRAY_BROWN)

        self.cubic_mid_dot_123_equation = MathTex("D = lerp(t, A, B)", color=WHITE, substrings_to_isolate= {"D", "t", "A", "B"})
        self.cubic_mid_dot_123_equation.set_color_by_tex("D", BLUE)
        self.cubic_mid_dot_123_equation.set_color_by_tex("A", YELLOW)
        self.cubic_mid_dot_123_equation.set_color_by_tex("B", RED)
        self.cubic_mid_dot_123_equation.set_color_by_tex("t", GRAY_BROWN)

        self.cubic_mid_dot_234_equation = MathTex("E = lerp(t, B, C)", color=WHITE, substrings_to_isolate= {"E", "t", "B", "C"})
        self.cubic_mid_dot_234_equation.set_color_by_tex("E", MAROON)
        self.cubic_mid_dot_234_equation.set_color_by_tex("B", RED)
        self.cubic_mid_dot_234_equation.set_color_by_tex("C", ORANGE)
        self.cubic_mid_dot_234_equation.set_color_by_tex("t", GRAY_BROWN)

        self.cubic_mid_dot_34_equation = MathTex("C = lerp(t, P_2, P_3)", color=WHITE, substrings_to_isolate= {"C", "t"})
        self.cubic_mid_dot_34_equation.set_color_by_tex("C", ORANGE)
        self.cubic_mid_dot_34_equation.set_color_by_tex("t", GRAY_BROWN)

        self.cubic_mid_dot_1234_equation = MathTex("P = lerp(t, C, D)", color=WHITE, substrings_to_isolate= {"P", "t", "C", "D"})
        self.cubic_mid_dot_1234_equation.set_color_by_tex("P", PINK)
        self.cubic_mid_dot_1234_equation.set_color_by_tex("t", GRAY_BROWN)
        self.cubic_mid_dot_1234_equation.set_color_by_tex("C", ORANGE)
        self.cubic_mid_dot_1234_equation.set_color_by_tex("D", BLUE)

        self.cubic_equations += self.cubic_mid_dot_12_equation
        self.cubic_equations += self.cubic_mid_dot_23_equation
        self.cubic_equations += self.cubic_mid_dot_34_equation
        self.cubic_equations += self.cubic_mid_dot_123_equation
        self.cubic_equations += self.cubic_mid_dot_234_equation
        self.cubic_equations += self.cubic_mid_dot_1234_equation

        self.cubic_equations.arrange(DOWN, aligned_edge=LEFT).scale(0.6).shift(2 * UP + 5.5 * LEFT)

        mid_dot_12_text.restore()
        mid_dot_23_text.restore()
        mid_dot_23_text.add_updater(
            lambda m: m.next_to(mid_dot_23, UP)
        )
        mid_dot_123_text.restore()
        mid_dot_123_text = MathTex("D", color=BLUE).scale(0.8)
        mid_dot_123_text.add_updater(
                lambda m: m.next_to(mid_dot_123, 0.5 * UP + 0.5 * LEFT)
            )

        self.play(
            Create(self.cubic_equations),
            Create(mid_dot_12_text),
            Create(mid_dot_23_text),
            Create(mid_dot_34_text),
            Create(mid_dot_123_text),
            Create(mid_dot_234_text),
            Create(mid_dot_1234_text)
        )
        self.wait(2)

        # Kreiranje funkcije za ispis prve krive
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

        # Podesavanje koeficijenata za pomeranje frame-ova
        self.draw_upd = 0
        self.k = 1
        self.coeff = 0.007
        self.t = 0.5

        # Upd t na osnovu frame-a
        def cubic_upd_t_0_1(mobject, dt):
            if self.t > 1:
                self.t = 1.00001
            if self.t < 0:
                self.t = -0.0001
            
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

        self.play(
            Uncreate(mid_dot_12_text),
            Uncreate(mid_dot_23_text),
            Uncreate(mid_dot_34_text),
            Uncreate(mid_dot_123_text),
            Uncreate(mid_dot_234_text),
            Uncreate(mid_dot_1234_text)
        )


        self.wait()
        self.play(
            Create(cubic_bezier_name)
        )

        self.draw_upd = 1
        curve_line_1 = always_redraw(get_cubic_curve)
        self.add(curve_line_1)

        self.wait(2.5)
        self.play(Uncreate(self.curve_1))
        dot1.remove_updater(cubic_upd_t_0_1)
        self.wait()

        self.play(
            dot1.animate.shift(2 * UP ),
            dot4.animate.shift(2 * UP ),
            dot3_text.animate.add_updater(
                lambda m: m.next_to(dot3, DOWN)
            ),
            dot3.animate.shift(4 * DOWN),
            Uncreate(cubic_bezier_name)
        )
        dot3_text.add_updater(
            lambda m: m.next_to(dot3, DOWN)
        )
        self.wait(0.5)

        self.draw_upd = 1
        self.k = 1
        self.t = 1.01
        dot1.add_updater(cubic_upd_t_0_1)

        self.wait(2)

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
        
        self.draw_upd = 1
        curve_line_2 = always_redraw(get_cubic_curve_2)
        self.add(curve_line_2)

        self.wait(2.5)
        self.play(
            Uncreate(self.curve_2),
            dot2.animate.shift(5 * RIGHT),
            dot3.animate.shift(5 * LEFT + 4 * UP),
            dot1.animate.shift(2 * DOWN + 1.5 * RIGHT),
            dot4.animate.shift(2 * DOWN + 1.5 * LEFT),
            dot3_text.animate.add_updater(
                lambda m: m.next_to(dot3, UP)
            ),
        )
        dot3_text.add_updater(
            lambda m: m.next_to(dot3, UP)
        )
        self.wait(0.5)

        # 3 Linija
        self.draw_upd = 1

        self.curve_3 = VGroup()
        self.curve_3.add(Line(dot1.get_center(), dot1.get_center()))
        def get_cubic_curve_3():
            if self.draw_upd == 2:
                last_line = self.curve_3[-1]
                x = mid_dot_1234.get_center()[0]
                y = mid_dot_1234.get_center()[1]
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
                if (x <= dot4.get_center()[0]):
                    self.curve_3.add(new_line)

            return self.curve_3
        
        curve_line_3 = always_redraw(get_cubic_curve_3)
        self.add(curve_line_3)

        self.wait(4.5)

        self.play(
            Uncreate(line_12),
            Uncreate(line_23),
            Uncreate(line_34),
            Uncreate(line_123),
            Uncreate(line_234),
            Uncreate(line_1234)
        )

        self.play(
            Uncreate(dot1),
            Uncreate(dot2),
            Uncreate(dot3),
            Uncreate(dot4),
            Uncreate(mid_dot_12),
            Uncreate(mid_dot_23),
            Uncreate(mid_dot_34),
            Uncreate(mid_dot_123),
            Uncreate(mid_dot_234),
            Uncreate(mid_dot_1234),
            
            Uncreate(self.cubic_equations),
            Uncreate(self.t_val_label)
        )
        
        self.play(
            Uncreate(self.cubic_equations),
            Uncreate(self.curve_3),
            Uncreate(dot1_text),
            Uncreate(dot2_text),
            Uncreate(dot3_text),
            Uncreate(dot4_text)
        )

        # KRAJ KUBNIH KRIVIH

    def construct(self):
        # Ispis Autora
        autori = VGroup()
        autori += Text("Branko Grbić", t2c={"Branko Grbić": ORANGE}).scale(0.45)
        autori += Text("Maša Cucić", t2c={"Maša Cucić": ORANGE}).scale(0.45)
        autori.arrange(DOWN, aligned_edge=LEFT).shift(2.5 * DOWN + 4.5 * RIGHT)

        # Ispis naslova
        text_intro = Text("Bézier-ove krive", t2c={"Bézier": RED, " krive": YELLOW})
        self.play(
            Create(text_intro),
            Create(autori)
        )
        self.wait()

        self.play(
            text_intro.animate.scale(0.3),
            text_intro.animate.shift(3.5*LEFT + 2.6*UP),
            Uncreate(autori)
        )

        # Konstrukcija tacaka
        dot1 = Dot().set_z_index(100)
        dot2 = Dot().set_z_index(100)
        dot3 = Dot().set_z_index(100)
        dot4 = Dot().set_z_index(100)

        # Label njihovih imena
        dot1_text = MathTex("P_0")
        dot1_text.scale(0.8)
        dot1_text.add_updater(
                lambda m: m.next_to(dot1, LEFT)
            )
        
        dot2_text = MathTex("P_1")
        dot2_text.scale(0.8)
        dot2_text.add_updater(
                lambda m: m.next_to(dot2, RIGHT)
            )
        
        dot3_text = MathTex("P_2")
        dot3_text.scale(0.8)
        dot3_text.add_updater(
                lambda m: m.next_to(dot3, RIGHT)
            )

        dot4_text = MathTex("P_3")
        dot4_text.scale(0.8)
        dot4_text.add_updater(
                lambda m: m.next_to(dot4, RIGHT)
            )

        # Podesavanje sredisnje tacke
        mid_dot_123 = Dot().set_z_index(90)
        mid_dot_123.set_fill(BLACK)
        mid_dot_123.set_stroke(BLUE, width=4)
        mid_dot_123.save_state()

        mid_dot_123_text = MathTex("P_{mid}")
        mid_dot_123_text.scale(0.8)
        mid_dot_123_text.save_state()
        mid_dot_123_text.add_updater(
                lambda m: m.next_to(mid_dot_123, DOWN + 0.2 * RIGHT)
            )

        # Pokretanje animacija
        self.play(
            Create(dot1),
            Create(dot2)
        )

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

        mid_dot_123_equation_upd = MathTex("P = lerp(t, P_0, P_1)", color=BLUE)
        mid_dot_123_equation_upd.scale(0.9),
        mid_dot_123_equation_upd.shift(3.5*LEFT + 2.7*UP)
        mid_dot_123_eq_framebox_upd = SurroundingRectangle(mid_dot_123_equation_upd)

        self.play(
            Create(line_12),
            Create(mid_dot_123),
            Create(dot1_text),
            Create(dot2_text),
            Create(mid_dot_123_text),
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
        mid_text.scale(0.8)
        mid_equal.scale(0.8)
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
        self.wait()

        # Animacije kretanja sredisnje tacke
        mid_dot_123_x = ValueTracker(0)
        mid_dot_123_y = ValueTracker(0)
        mid_dot_123.add_updater(lambda z: z.set_x(mid_dot_123_x.get_value()))
        mid_dot_123.add_updater(lambda z: z.set_y(mid_dot_123_y.get_value()))

        t = 0.7
        self.play(
            mid_dot_123_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_123_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=1
        )

        t = 0.15
        self.play(
            mid_dot_123_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_123_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            run_time=2,
        )

        t = 0.5
        self.play(
            mid_dot_123_x.animate.set_value((1-t) * dot1.get_center()[0] + t * dot2.get_center()[0]),
            mid_dot_123_y.animate.set_value((1-t) * dot1.get_center()[1] + t * dot2.get_center()[1]),
            Uncreate(text_intro),
            Create(mid_dot_123_equation_upd),
            Transform(mid_dot_123_eq_framebox, mid_dot_123_eq_framebox_upd),
            run_time=1.5
        )
        self.wait(0.5)


        # Brisanje jednacina, indikatora i shiftovanje postojecih tacaka
        dot3.shift(3 * RIGHT + 2 * DOWN)

        line_23 = Line(start=dot2.get_center(), end=dot3.get_center(), color=GREY)
        line_23.add_updater(lambda z: z.become(Line(dot2.get_center(), dot3.get_center(), color=GREY)))
        
        self.wait()
        self.play(
            Uncreate(mid_label),
            Uncreate(mid_dot_123),
            Uncreate(mid_dot_123_eq_framebox),
            Uncreate(mid_dot_123_text),
            Uncreate(mid_dot_123_equation_upd),

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

        mid_dot_12_text = MathTex("A", color=YELLOW)
        mid_dot_12_text.scale(0.8)
        mid_dot_12_text.add_updater(
                lambda m: m.next_to(mid_dot_12, LEFT)
            )
        mid_dot_12_text.save_state()

        mid_dot_23 = Dot(color=BLUE).shift((dot2.get_center() + dot3.get_center()) / 2).set_z_index(90)
        mid_dot_23.set_fill(BLACK)
        mid_dot_23.set_stroke(RED, width=4)

        mid_dot_23_text = MathTex("B", color=RED)
        mid_dot_23_text.scale(0.8)
        mid_dot_23_text.add_updater(
                lambda m: m.next_to(mid_dot_23, RIGHT)
            )
        mid_dot_23_text.save_state()

        line_123 = Line(start=mid_dot_12.get_center(), end=mid_dot_23.get_center(), color=GREY)
        line_123.add_updater(lambda z: z.become(Line(mid_dot_12.get_center(), mid_dot_23.get_center(), color=GREY)))

        mid_dot_123.set_value((mid_dot_12.get_center() + mid_dot_23.get_center()) / 2)

        
        # Animacija kvadratnog Bezijera
        self.QuadraticBezier(dot1, dot2, dot3, mid_dot_12, mid_dot_23, mid_dot_123, line_12, line_23, line_123, mid_dot_12_text, mid_dot_23_text)


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

        mid_dot_34_text = MathTex("C", color=ORANGE)
        mid_dot_34_text.scale(0.8)
        mid_dot_34_text.add_updater(
                lambda m: m.next_to(mid_dot_34, RIGHT)
            )

        line_234 = Line(start=mid_dot_23.get_center(), end=mid_dot_34.get_center(), color=GREY)
        line_234.add_updater(lambda z: z.become(Line(mid_dot_23.get_center(), mid_dot_34.get_center(), color=GREY)))

        mid_dot_234 = Dot().shift((mid_dot_23.get_center() + mid_dot_34.get_center()) / 2).set_z_index(80)
        mid_dot_234.set_fill(BLACK)
        mid_dot_234.set_stroke(MAROON, width=4)

        mid_dot_234_text = MathTex("E", color=MAROON)
        mid_dot_234_text.scale(0.8)
        mid_dot_234_text.add_updater(
                lambda m: m.next_to(mid_dot_234, 0.5 * UP + 0.5 * RIGHT)
            )

        self.play(
            Create(mid_dot_34),
            Create(line_234),
            Create(mid_dot_234)
        )


        mid_dot_1234 = Dot().shift((mid_dot_123.get_center() + mid_dot_234.get_center()) / 2).set_z_index(80)
        mid_dot_1234.set_fill(BLACK)
        mid_dot_1234.set_stroke(PINK, width=4)

        mid_dot_1234_text = MathTex("P", color=PINK)
        mid_dot_1234_text.scale(0.8)
        mid_dot_1234_text.add_updater(
                lambda m: m.next_to(mid_dot_1234, 0.5 * UP)
            )

        line_1234 = Line(start=mid_dot_123.get_center(), end=mid_dot_234.get_center(), color=GREY)
        line_1234.add_updater(lambda z: z.become(Line(mid_dot_123.get_center(), mid_dot_234.get_center(), color=GREY)))

        self.play(
            Create(mid_dot_1234),
            Create(line_1234)
        )

        # Animacija kubnog Bezijera
        self.CubicBezier(dot1, dot2, dot3, dot4, mid_dot_12, mid_dot_23, mid_dot_34, mid_dot_123, mid_dot_234, mid_dot_1234,
                        line_12, line_23, line_34, line_123, line_234, line_1234, dot1_text, dot2_text, dot3_text, dot4_text,
                        mid_dot_12_text, mid_dot_23_text, mid_dot_34_text, mid_dot_123_text, mid_dot_234_text, mid_dot_1234_text)

        self.wait()

class PracticeScene(Scene):
    def construct(self):
        self.quadratic_equations = VGroup()

        self.quadratic_mid_dot_12_equation = MathTex("A = lerp(t, P_0, P_1)", color=WHITE, substrings_to_isolate= {"A", "t"})
        self.quadratic_mid_dot_23_equation = MathTex("B = lerp(t, P_1, P_2)", color=WHITE, substrings_to_isolate= {"B", "t"})
        self.quadratic_mid_dot_123_equation = MathTex("P = lerp(t, A, B)", color=WHITE, substrings_to_isolate= {"P", "t", "A", "B"}).scale(0.8)

        self.quadratic_mid_dot_12_equation.set_color_by_tex("A", YELLOW)
        self.quadratic_mid_dot_12_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_mid_dot_23_equation.set_color_by_tex("B", RED)
        self.quadratic_mid_dot_23_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_mid_dot_123_equation.set_color_by_tex("P", BLUE)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("A", YELLOW)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("B", RED)
        self.quadratic_mid_dot_123_equation.set_color_by_tex("t", GRAY_BROWN)

        self.quadratic_equations += self.quadratic_mid_dot_12_equation
        self.quadratic_equations += self.quadratic_mid_dot_23_equation

        self.quadratic_equations.arrange(DOWN, aligned_edge=LEFT).scale(0.8).shift(2.5 * UP + 4.5 * LEFT)

        quadratic_equations_framebox = SurroundingRectangle(self.quadratic_equations)


        self.play(
            Create(self.quadratic_equations),
            Create(quadratic_equations_framebox)
        )

        self.play(
            self.quadratic_equations.animate.add(self.quadratic_mid_dot_123_equation).arrange(DOWN, aligned_edge=LEFT).shift(2.5 * UP + 4.5 * LEFT),
            Uncreate(quadratic_equations_framebox)
        )

        quadratic_equations_framebox_upd = SurroundingRectangle(self.quadratic_equations[2])
        self.play(
            Create(quadratic_equations_framebox_upd)
        )
        self.wait(2)
'''


'''