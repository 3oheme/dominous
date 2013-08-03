from pygame import *
from gloss import *

from sound import *
from tools import *
from config import *
from os import *
from selectplayers import *


class SlidesCounter():
    def __init__(self, counter_players, pos = (0,0)):
        self.pos = (pos[0] + 3, pos[1] + 135)
        self.pos_to = self.pos
        self.pos_orig = self.pos
        self.pos_from = self.pos
        self.counter = counter_players
        self.current = 0
        self.eggs = 0
        self.step = 364/(self.counter-1)
    def next(self):
        self.eggs = 0
        self.current = (self.current + 1) % self.counter
        self.pos_from = self.pos
        self.pos_to = (self.pos_orig[0]+(self.current*self.step), self.pos_orig[1])
    def prev(self):
        self.eggs = 0
        self.current = (self.current - 1) % self.counter
        self.pos_from = self.pos
        self.pos_to = (self.pos_orig[0]+(self.current*self.step), self.pos_orig[1])
    def draw(self):
        self.eggs += Gloss.elapsed_seconds * 2
        if (self.eggs > 1.0):
            self.eggs = 1.0
        self.pos = (Gloss.smooth_step(self.pos[0], self.pos_to[0], self.eggs), self.pos_orig[1])
        newpos = self.pos
        newpos2 = (newpos[0]+2, newpos[1]+2)
        newpos3 = (newpos[0]+7, newpos[1]+3)
        Gloss.draw_box(position = newpos2, width = 20, height = 20, color = Color.from_html("#d6d6d6"))
        Gloss.draw_box(position = newpos, width = 20, height = 20, color = Color.from_html("#f7af08"))

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
            basename, extension = os.path.splitext(slide)
            if slide[0] != '.' and extension == '.png':
                tempslides.append(slide)
        
        tempslides.sort()
        
        for slide in tempslides:
            if slide.endswith("png"):
                self.slides.append(Texture(os.path.join(os.getcwd(), 'tutorial', slide)))
        
        self.slides_len = len(self.slides)
        
        self.falling = []
       
        self.slides_counter = SlidesCounter(self.slides_len, (200, 405))
       
    def draw(self):

        Gloss.fill(self.background)
        
        self.slides[self.status-1].draw(position = (0, 0))
        
        for fall in self.falling:
            fall.draw(color = Color(1,1,1,Gloss.smooth_step(1, 0, fall.movetime)))
        
        # pintamos los botones
        if self.status == 1:
            self.left.draw(position = (668, 532), color = Color(1,1,1,0.3))
        else:
            self.left.draw(position = (668, 532))
        
        if self.status == self.slides_len:
            self.right.draw(position = (728, 532), color = Color(1,1,1,0.3))
        else:
            self.right.draw(position = (728, 532))
            
        self.slides_counter.draw()
        
        self.exit.draw(position = (25, 532))
        
    def update(self):
        for fall in self.falling:
            fall.movetime += Gloss.elapsed_seconds * 2
            if (fall.movetime > 1.0): self.falling.remove(fall)
            #fall.move_to(None, Gloss.lerp(0, 10, fall.movetime))
        
    def start(self):
        self.game.on_mouse_down = self.mouse_down
        self.status = 1
        self.slides_counter = SlidesCounter(self.slides_len, (200, 405))

    def stop(self):
        self.status = 0

    def mouse_down(self, event):
        if self.status != 0:
            if self.status != self.slides_len and event.pos[0] > 728 and event.pos[1] > 532 and event.pos[0] < 775 and event.pos[1] < 574:
                newfall = Sprite(self.slides[self.status-1], (0, 0))
                newfall.movetime = 0
                self.falling.insert(0, newfall)
                self.status += 1
                self.slides_counter.next()
            elif self.status != 1 and event.pos[0] > 668 and event.pos[1] > 532 and event.pos[0] < 715 and event.pos[1] < 574:
                newfall = Sprite(self.slides[self.status-1], (0, 0))
                newfall.movetime = 0
                self.falling.insert(0, newfall)
                self.status -= 1
                self.slides_counter.prev()
            elif event.pos[0] > 25 and event.pos[1] > 532 and event.pos[0] < 161 and event.pos[1] < 574:
                self.game.goto_menu()
        
