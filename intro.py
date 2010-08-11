# -*- coding: utf-8 -*-

from pygame import *
from gloss import *

from sound import *
from tools import *

class Intro():
    def __init__(self, mainp):
        self.game = mainp
        self.logo_fade = 0
        self.logo_fade_out = 0
        self.logo_fading_out = False
        self.fadeout_amount = 0.0
        self.fadeout = False
        self.timer_off = 4.2
        self.timer_goto_menu = 7.5
    def draw(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
        if Gloss.total_seconds < self.timer_off:
            self.logo_fade += 0.005
            if self.logo_fade > 1:
                self.logo_fade = 1
            self.logo.draw(position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/1.5), origin = (self.logo.half_width, self.logo.half_height), scale = Gloss.smooth_step(0.35, 0.4, self.logo_fade))
        else:
            self.logo_fade_out += 0.007
            if self.logo_fade_out > 1:
                self.logo_fade_out = 1
            self.logo.draw(position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/1.5), origin = (self.logo.half_width, self.logo.half_height), scale = Gloss.smooth_step(0.4, 0.45, self.logo_fade_out), color = Color(1,1,1,Gloss.smooth_step(1, 0, self.logo_fade_out)))
        if self.fadeout:
            next = Gloss.lerp(0, 1, self.fadeout_amount)
            Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(1,1,1,next))
            self.fadeout_amount += 0.05
            if next == 1:
                self.game.goto_menu()
        if Gloss.total_seconds > self.timer_goto_menu:
            self.game.goto_menu()
        
    def update(self):
        self.game.on_mouse_up = self.events
    def start(self):
        self.logo = Texture(tool.image("system", "dominous.png"))
        sound.intro()
    def stop(self):
        del self.logo
    def events(self, event):
        self.fadeout = True
