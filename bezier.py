from manim import *

import numpy as np

class DotToLine(Scene):
    def construct(self):
        # Hold na 1s
        self.wait()

        # Konstrukcija tacaka
        dot1 = Dot()
        dot2 = Dot()

        # Podesavanje sredisnje tacke
        mid_dot = Dot()
        mid_dot.set_fill(BLACK)
        mid_dot.set_stroke(BLUE, width=4)

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

        self.play(
                Create(line),
                Create(mid_dot),
            )

        self.wait()

        # P_MID = (1 - t) * P[0] + t * P[1]
        t = 0.5

        # Label koji prati sredisnju tacku
        mid_text, mid_number = label = VGroup(
            Text("t = "),
            DecimalNumber(
                0.50,
                num_decimal_places=2
            )
        )
        label.arrange(RIGHT)
        label.scale(0.8)

        label.add_updater(
                lambda m: m.next_to(mid_dot, UP + LEFT)
            )

        # Updater sredisnje tacke
        mid_number.add_updater(lambda m: m.set_value(
                (mid_dot.get_center()[0] - dot1.get_center()[0]) / (dot2.get_center()[0] - dot1.get_center()[0])
            ))

        self.play(Create(label))
        self.wait()

        # Animacije kretanja sredisnje tacke
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
        self.wait()

        self.play(
            Uncreate(label),
            Uncreate(mid_dot)
            )

        self.wait()

'''

Resenje je neodlucivo. 
Vecina velemajstora se slazu da uz savrsenu igru, igra bi se zavrsila kao remi. 
Ali ovo je slucaj u kome nemamo tacne definisane moci, pa ne mozemo da tvrdimo do koje granice ide necija moc. 
Iako jedan igrac vidi buducnost, da li vidi sve alterativne buducnosti ili samo jednu (zivimo u determinizmu?)?
Statisticki gledano, beli igrac pobedjuje vise od crnog (jer prvi napada), iz cega mozemo da zakljucimo da mozda ima odredjenu prednost. 
Svakako, problem nije dovoljno definisan da bi mogle da se iznesu konkretne tvrdnje.

'''