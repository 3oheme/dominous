# -*- coding: utf-8 -*-

from pygame import *
from gloss import *
from config import *

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

class Options1():
    def __init__(self):
        self.position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 38, False, False, 32, 255)
        self.str_quick_game = "partida rapida"
        self.str_tournament = "laboratorio"
        self.str_tutorial = "tutorial"
        self.str_options = "opciones"
        self.str_exit = "salir"
        self.fontsize1 = self.font_main.measure_string(self.str_quick_game)
        self.fontsize2 = self.font_main.measure_string(self.str_tournament)
        self.fontsize3 = self.font_main.measure_string(self.str_options)
        self.fontsize4 = self.font_main.measure_string(self.str_tutorial)
        self.fontsize5 = self.font_main.measure_string(self.str_exit)
        self.eggs = 0
    def draw(self):
        self.font_main.draw(self.str_quick_game, position = (self.position[0]-(self.fontsize1[0]/2), self.position[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_tournament, position = (self.position[0]-(self.fontsize2[0]/2), self.position[1]+self.fontsize1[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_options, position = (self.position[0]-(self.fontsize3[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_tutorial, position = (self.position[0]-(self.fontsize4[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_exit, position = (self.position[0]-(self.fontsize5[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize5[1]+20), color = Color(0.3, 0.3, 0.3, 1))
    def update(self):
        pass
    def hide(self):
        pass
    def show(self):
        pass
    def click(self, pos):
        if (pos[0]>self.position[0]-self.fontsize1[0]/2 and pos[0]<self.position[0]+self.fontsize1[0]/2 and \
            pos[1]>self.position[1] and pos[1]<self.position[1]+self.fontsize1[1]):
            config['goto_lab'] = False
            config['gametype'] = 'human'
            return 2
        elif (pos[0]>self.position[0]-self.fontsize2[0]/2 and pos[0]<self.position[0]+self.fontsize2[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1] and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]):
            config['gametype'] = 'computer'
            config['goto_lab'] = True
            return 2
        elif (pos[0]>self.position[0]-self.fontsize3[0]/2 and pos[0]<self.position[0]+self.fontsize3[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1] and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]):
            return 10
        elif (pos[0]>self.position[0]-self.fontsize4[0]/2 and pos[0]<self.position[0]+self.fontsize4[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1] and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize4[1]):
            return 3
        elif (pos[0]>self.position[0]-self.fontsize5[0]/2 and pos[0]<self.position[0]+self.fontsize5[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize4[1]+20 and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+20+self.fontsize4[1]+self.fontsize5[1]):
            return 99
        else:
            return 1
 
class Options2():
    def __init__(self):
        self.position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 38, False, False, 32, 255)
        self.str_quick_game = config['gametype']
        self.str_tournament = config['theme'] 
        self.str_options = "   "
        self.str_exit = "volver"
        self.fontsize1 = self.font_main.measure_string(self.str_quick_game)
        self.fontsize2 = self.font_main.measure_string(self.str_tournament)
        self.fontsize3 = self.font_main.measure_string(self.str_options)
        self.fontsize4 = self.font_main.measure_string(self.str_exit)
        self.eggs = 0
            
        # read all themes from HD and store in a list
        self.themes = []
        themes_dir = os.listdir(os.path.join(os.getcwd(), 'themes'))
        for theme_dir in themes_dir:
            if theme_dir[0] != '.':
                self.themes.append(theme_dir)
        self.themes.sort() # python rules :-D
    def draw(self):
        self.font_main.draw(self.str_quick_game, position = (self.position[0]-(self.fontsize1[0]/2), self.position[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_tournament, position = (self.position[0]-(self.fontsize2[0]/2), self.position[1]+self.fontsize1[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_options, position = (self.position[0]-(self.fontsize3[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]), color = Color(0.3, 0.3, 0.3, 1))
        self.font_main.draw(self.str_exit, position = (self.position[0]-(self.fontsize4[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+50), color = Color(0.3, 0.3, 0.3, 1))
    def update(self):
        pass
    def hide(self):
        pass
    def show(self):
        pass
    def click(self, pos):
        if (pos[0]>self.position[0]-self.fontsize1[0]/2 and pos[0]<self.position[0]+self.fontsize1[0]/2 and \
            pos[1]>self.position[1] and pos[1]<self.position[1]+self.fontsize1[1]):
            if config['gametype'] == "human":
                self.str_quick_game = 'computer'
                config['gametype'] = 'computer'
            else:
                self.str_quick_game = 'human'
                config['gametype'] = 'human'
            self.fontsize1 = self.font_main.measure_string(self.str_quick_game)
            return 10
        elif (pos[0]>self.position[0]-self.fontsize2[0]/2 and pos[0]<self.position[0]+self.fontsize2[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1] and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]):
            theme_index = self.themes.index(config['theme']) +1
            if theme_index == len(self.themes):
                theme_index = 0
            config['theme'] = self.themes[theme_index]
            self.str_tournament = self.themes[theme_index]
            self.fontsize2 = self.font_main.measure_string(self.str_tournament)
            return 10
        elif (pos[0]>self.position[0]-self.fontsize3[0]/2 and pos[0]<self.position[0]+self.fontsize3[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1] and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]):
            pass
        elif (pos[0]>self.position[0]-self.fontsize4[0]/2 and pos[0]<self.position[0]+self.fontsize4[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+50 and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+50+self.fontsize4[1]):
            return 1
        else:
            return 10


class Menu():
    def __init__(self, mainp):
        self.game = mainp
        self.box = Box()
        self.options1 = Options1()
        self.options2 = Options2()
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
        self.logo = Texture(tool.image("system", "dominous.png"))
        
    def draw(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
        self.box.draw()
        
        self.logo.draw(position = (309, 99), scale = 0.22)
        
        if self.status == 1:
            self.options1.draw()
        elif self.status == 2:
            self.options1.draw()
        elif self.status == 10:
            self.options2.draw()

        if self.fadein:
            next = Gloss.lerp(1, 0, self.fadein_amount)
            Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(1,1,1,next))
            self.fadein_amount += 0.05
            if next == 0:
                self.fadein = False
    def update(self):
        # options 1
        if self.status == 1:
            self.box.update()
            self.options1.update()
            self.game.on_mouse_up = self.events
        # start quick game
        elif self.status == 2:
            self.game.goto_selectplayers()
        # go to tutorial
        elif self.status == 3:
            self.game.goto_tutorial()
        elif self.status == 10:
            self.options2.update()
        # exit game
        elif self.status == 99:
            # before exit, lets save options
            save_config(config)
            self.game.goto_finish()
        else:
            self.status = 1
    def start(self):
        self.box = Box()
        self.options1 = Options1()
        self.options2 = Options2()
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
        sound.menu()
    def stop(self):
        pass
    def events(self, event):
        if self.status == 1:
            self.status = self.options1.click(event.pos)
        elif self.status == 10:
            self.status = self.options2.click(event.pos)
