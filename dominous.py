#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
from gloss import *

from intro import *
from menu import *
from engine import *
from finish import *
from selectplayers import *
from tutorial import *
from lab import *
from tools import *

from config import *

class DominousGame(GlossGame):
    """
    Main game class. This class is a finite-state machine that controls
    the game flow, and calls following objects:
        intro: intro animation, logo fading in
        menu: shows main menu and options
        engine: dominoes graphic engine
        finish: credits
        exit: close all
    @brief Main game class
    """
    def preload_content(self):
        self.intro = Intro(self)
        self.menu = Menu(self)
        self.selectplayers = SelectPlayers(self)
        self.tutorial = Tutorial(self)
        self.finish = Finish(self)
        self.flow = self.intro
        #self.flow = self.selectplayers
        #self.flow = self.finish
        self.flow.start()
    def draw_loading_screen(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
    def load_content(self):
        pass
    def draw(self):
        self.flow.draw()
    def update(self):
        self.flow.update()
    def goto_intro(self):
        self.flow.stop()
        self.flow = self.intro
        self.flow.start()
    def goto_menu(self):
        self.flow.stop()
        self.flow = self.menu
        self.flow.start()
    def goto_selectplayers(self):
        self.flow.stop()
        self.flow = self.selectplayers
        self.flow.start()
    def goto_tutorial(self):
        self.flow.stop()
        self.flow = self.tutorial
        self.flow.start()
    def goto_game(self):
        self.flow.stop()
        self.engine = Engine(self)
        self.flow = self.engine
        self.flow.start()
    def goto_lab(self):
        self.flow.stop()
        self.lab = Lab(self)
        self.flow = self.lab
        self.flow.start()
    def goto_finish(self):
        self.flow.stop()
        self.flow = self.finish
        self.flow.start()
    def goto_exit(self):
        self.quit()

if __name__ == '__main__':
    """ Dominous main game function """
    game = DominousGame(config['window_caption'])
    Gloss.screen_resolution = config['window_width'], config['window_height']
    if config['full_screen'] == 'True':
        Gloss.full_screen = 1
    else:
        Gloss.full_screen = 0
    game.run()
