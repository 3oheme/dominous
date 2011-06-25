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
        self.color = 1
    def draw(self):
        self.font_main.draw(self.str_quick_game, position = (self.position[0]-(self.fontsize1[0]/2), self.position[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_tournament, position = (self.position[0]-(self.fontsize2[0]/2), self.position[1]+self.fontsize1[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_options, position = (self.position[0]-(self.fontsize3[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_tutorial, position = (self.position[0]-(self.fontsize4[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_exit, position = (self.position[0]-(self.fontsize5[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize5[1]+20), color = Color(0.3, 0.3, 0.3, self.color))
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
            config['gametype_current'] = 'single'
            return 2
        elif (pos[0]>self.position[0]-self.fontsize2[0]/2 and pos[0]<self.position[0]+self.fontsize2[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1] and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]):
            config['gametype_current'] = 'lab'
            config['goto_lab'] = True
            return 2
        elif (pos[0]>self.position[0]-self.fontsize3[0]/2 and pos[0]<self.position[0]+self.fontsize3[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1] and \
            pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]):
            return 110
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
        if config['gametype'] == 'computer':
            self.str_quick_game = 'modo de juego solo computadora'
        else:
            self.str_quick_game = 'modo de juego un jugador'
        self.str_tournament = "tema grafico " + config['theme']
        if config['speed'] == '1':
            self.str_options = "velocidad normal"
        elif config['speed'] == '2':
            self.str_options = "velocidad rapida"
        else:
            self.str_options = "velocidad extra rapida"
        if config['full_screen'] == 'True':
            self.str_full = 'Pantalla completa'
        else:
            self.str_full = 'Modo ventana'
        self.str_exit = "volver"
        self.fontsize1 = self.font_main.measure_string(self.str_quick_game)
        self.fontsize2 = self.font_main.measure_string(self.str_tournament)
        self.fontsize3 = self.font_main.measure_string(self.str_options)
        self.fontsize4 = self.font_main.measure_string(self.str_exit)
        self.fontsize5 = self.font_main.measure_string(self.str_full)
        self.eggs = 0
        self.color = 1
            
        # read all themes from disk and store in a list
        self.themes = []
        themes_dir = os.listdir(os.path.join(os.getcwd(), 'themes'))
        for theme_dir in themes_dir:
            if theme_dir[0] != '.':
                self.themes.append(theme_dir)
        self.themes.sort() # python rules :-D
    def draw(self):
        self.font_main.draw(self.str_quick_game, position = (self.position[0]-(self.fontsize1[0]/2), self.position[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_tournament, position = (self.position[0]-(self.fontsize2[0]/2), self.position[1]+self.fontsize1[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_options, position = (self.position[0]-(self.fontsize3[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_full, position = (self.position[0]-(self.fontsize5[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]), color = Color(0.3, 0.3, 0.3, self.color))
        self.font_main.draw(self.str_exit, position = (self.position[0]-(self.fontsize4[0]/2), self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize5[1]+50), color = Color(0.3, 0.3, 0.3, self.color))
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
                self.str_quick_game = 'modo de juego solo computadora'
                config['gametype'] = 'computer'
            else:
                self.str_quick_game = 'modo de juego un jugador'
                config['gametype'] = 'human'
            self.fontsize1 = self.font_main.measure_string(self.str_quick_game)
            return 10
        elif (pos[0]>self.position[0]-self.fontsize2[0]/2 and pos[0]<self.position[0]+self.fontsize2[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1] and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]):
            theme_index = self.themes.index(config['theme']) +1
            if theme_index == len(self.themes):
                theme_index = 0
            config['theme'] = self.themes[theme_index]
            self.str_tournament = "tema grafico " + self.themes[theme_index]
            self.fontsize2 = self.font_main.measure_string(self.str_tournament)
            return 10
        elif (pos[0]>self.position[0]-self.fontsize3[0]/2 and pos[0]<self.position[0]+self.fontsize3[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1] and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]):
            if self.str_options == "velocidad normal":
                config['speed'] = '2'
                self.str_options = "velocidad rapida"
            elif self.str_options == "velocidad rapida":
                config['speed'] = '3'
                self.str_options = "velocidad extra rapida"
            else:
                self.str_options = "velocidad normal"
                config['speed'] = '1'
            self.fontsize3 = self.font_main.measure_string(self.str_options)
            return 10
        elif (pos[0]>self.position[0]-self.fontsize5[0]/2 and pos[0]<self.position[0]+self.fontsize5[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1] and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize5[1]):
            if self.str_full == 'Pantalla completa':
                config['full_screen'] = 'False'
                self.str_full = 'Modo ventana'
            else:
                config['full_screen'] = 'True'
                self.str_full = 'Pantalla completa'
            self.fontsize5 = self.font_main.measure_string(self.str_full)
            return 9
        elif (pos[0]>self.position[0]-self.fontsize4[0]/2 and pos[0]<self.position[0]+self.fontsize4[0]/2 and \
            pos[1]>self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+self.fontsize5[1]+50 and pos[1]<self.position[1]+self.fontsize1[1]+self.fontsize2[1]+self.fontsize3[1]+50+self.fontsize4[1]+self.fontsize5[1]):
            return 101
        else:
            return 10

class Overlay():
    def __init__(self):
        self.position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 28, False, False, 32, 255)
        self.text = "Para poder intercambiar entre\nlos modos de pantalla completa\ny modo ventana debes salir y\nvolver a ejecutar la aplicacion \n\n                      aceptar"
        self.fontsize = self.font_main.measure_string(self.text)
    def draw(self):
        Gloss.fill(top = Color(0,0,0,0.7), bottom = Color(0,0,0,9))
        self.font_main.draw(self.text, position = (self.position[0]-(self.fontsize[0]/2), self.position[1]), color = Color(1, 1, 1, 1))
    def update(self):
        pass
    def click(self, pos):
        return 10
       
class Menu():
    def __init__(self, mainp):
        self.game = mainp
        self.box = Box()
        self.options1 = Options1()
        self.options2 = Options2()
        self.overlay = Overlay()
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
        self.logo = Texture(tool.image("system", "dominous.png"))
        self.eggs = 0
        
    def draw(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
        self.box.draw()
        
        self.logo.draw(position = (309, 99), scale = 0.22)
        
        if self.status == 1:
            self.options1.draw()
        elif self.status == 110:
            self.options1.draw()
            self.options2.draw()
        elif self.status == 2:
            self.options1.draw()
        elif self.status == 9:
            self.overlay.draw()
        elif self.status == 10:
            self.options2.draw()
        elif self.status == 101:
            self.options1.draw()
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
            self.eggs = 0
            self.box.update()
            self.options1.update()
            self.game.on_mouse_up = self.events
        # from options 1 to 10
        if self.status == 110:
            self.eggs += Gloss.elapsed_seconds * 2
            if self.eggs > 1:
                self.status = 10
            self.options1.position = (Gloss.smooth_step(400, 350, self.eggs), 300)
            self.options1.color = Gloss.smooth_step(1, 0, self.eggs)
            
            self.options2.position = (Gloss.smooth_step(450, 400, self.eggs), 300)
            self.options2.color = Gloss.smooth_step(0, 1, self.eggs)
        # start quick game
        elif self.status == 2:
            self.game.goto_selectplayers()
        # go to tutorial
        elif self.status == 3:
            self.game.goto_tutorial()
        # show info overlay - restart program to have fullscreen
        elif self.status == 9:
            self.overlay.update()
        elif self.status == 10:
            self.eggs = 0
            self.options2.update()
        elif self.status == 101:
            self.eggs += Gloss.elapsed_seconds * 2
            if self.eggs > 1:
                self.status = 1
            self.options1.position = (Gloss.smooth_step(350, 400, self.eggs), 300)
            self.options1.color = Gloss.smooth_step(0, 1, self.eggs)
            
            self.options2.position = (Gloss.smooth_step(400, 450, self.eggs), 300)
            self.options2.color = Gloss.smooth_step(1, 0, self.eggs)
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
        elif self.status == 9:
            self.status = self.overlay.click(event.pos)
        elif self.status == 10:
            self.status = self.options2.click(event.pos)