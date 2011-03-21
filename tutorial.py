from pygame import *
from gloss import *
from dominoes_game import domino_game

from sound import *
from tools import *
from config import *
from os import *
from selectplayers import *

import log
import random

class Tutorial:
    def __init__(self, mainp):
        self.game = mainp
        self.game.on_mouse_down = self.mouse_down
        self.background = Texture(tool.image("system", "tutorial_bg.png"))
        self.status = 1
        
        self.exit = Texture(tool.image("system", "exit.png"))
        self.right = Texture(tool.image("system", "arrow_right.png"))
        self.left = Texture(tool.image("system", "arrow_left.png"))
        
        self.slides = []
        tempslides = []
        
        preslides = os.listdir(os.path.join(os.getcwd(), 'tutorial'))
        for slide in preslides:
            if slide[0] != '.':
                tempslides.append(slide)
        
        tempslides.sort()
        
        for slide in tempslides:
            self.slides.append(Texture(os.path.join(os.getcwd(), 'tutorial', slide)))
        
        self.slides_len = len(self.slides)
        
        self.falling = []
        
    def draw(self):

        Gloss.fill(self.background)
        
        self.slides[self.status-1].draw(position = (0, 0))
        
        for fall in self.falling:
            fall.draw(rotation = fall.movetime*2, color = Color(1,1,1,Gloss.smooth_step(1, 0, fall.movetime)))
        
        # pintamos los botones
        if self.status == 1:
            self.left.draw(position = (668, 532), color = Color(1,1,1,0.3))
        else:
            self.left.draw(position = (668, 532))
        
        if self.status == self.slides_len:
            self.right.draw(position = (728, 532), color = Color(1,1,1,0.3))
        else:
            self.right.draw(position = (728, 532))
            
        self.exit.draw(position = (25, 532))
        
    def update(self):
        for fall in self.falling:
            fall.movetime += Gloss.elapsed_seconds * 2
            if (fall.movetime > 1.0): self.falling.remove(fall)
            fall.move_to(None, Gloss.lerp(0, 10, fall.movetime))
        
    def start(self):
        self.status = 1
            
    def stop(self):
        self.status = 0

    def mouse_down(self, event):
        if self.status != 0:
            if self.status != self.slides_len and event.pos[0] > 728 and event.pos[1] > 532 and event.pos[0] < 775 and event.pos[1] < 574:
                newfall = Sprite(self.slides[self.status-1], (0, 0))
                newfall.movetime = 0
                self.falling.insert(0, newfall)
                self.status += 1
            elif self.status != 1 and event.pos[0] > 668 and event.pos[1] > 532 and event.pos[0] < 715 and event.pos[1] < 574:
                newfall = Sprite(self.slides[self.status-1], (0, 0))
                newfall.movetime = 0
                self.falling.insert(0, newfall)
                self.status -= 1
            elif event.pos[0] > 25 and event.pos[1] > 532 and event.pos[0] < 161 and event.pos[1] < 574:
                self.game.goto_menu()
        