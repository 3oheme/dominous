# -*- coding: utf-8 -*-

from pygame import *
from gloss import *

from sound import *
from tools import *

class Box():
    def __init__(self):
        self.box_x = Gloss.screen_resolution[0]/2
        self.box_y = Gloss.screen_resolution[1]/2
        self.box_width  = Gloss.screen_resolution[0]
        self.box_height = Gloss.screen_resolution[0]*2
        self.box_stop = 0.0
        self.alpha = 0
    def draw(self):
        Gloss.draw_box((self.box_x, self.box_y), self.box_width, self.box_height, Gloss.smooth_step(0, 45, self.alpha), (self.box_width/2, self.box_height/2), 1, Color(1, 1, 1, (Gloss.smooth_step(0, 1, self.alpha))))
    def update(self):
        self.alpha += 0.03

class FinishText():
    def __init__(self):
        self.position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 24, False, False, 32, 255)
        self.str_text = "Gracias por jugar con nosotros \n\nDominous es un proyecto desarrollado \npor Ignacio Palomo Duarte \nRecuerda que puedes ver las novedades \nde Dominous en http://www.3oheme.com/dominous"
        self.fontsize1 = self.font_main.measure_string(self.str_text)
        
    def draw(self):
        self.font_main.draw(self.str_text, position = (self.position[0]-(self.fontsize1[0]/2), self.position[1]), color = Color(0.3, 0.3, 0.3, 1))

    def update(self):
        pass


class Finish():
    """Finish state. Shows credits and fades out
    @brief Finish state
    """
    def __init__(self, mainp):
        self.game = mainp
        self.box = Box()
        self.finishtext = FinishText()
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
    def draw(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
        self.box.draw()
        self.finishtext.draw()
        if self.fadein:
            next = Gloss.lerp(1, 0, self.fadein_amount)
            Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(1,1,1,next))
            self.fadein_amount += 0.05
            if next == 0:
                self.fadein = False
    def update(self):
        self.finishtext.update()
        self.game.on_mouse_up = self.events
    def start(self):
        self.fadein = True
        self.fadein_amount = 0
        sound.credits()
    def stop(self):
        pass
    def events(self, event):
        self.game.goto_exit()
