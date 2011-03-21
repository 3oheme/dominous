from pygame import *
from gloss import *
from dominoes_game import domino_game

from sound import *
from tools import *
from config import *
from selectplayers import *

import log
import random

class Lab:
    def __init__(self, mainp):
        self.game = mainp
        self.domino = domino_game()
        self.game.on_mouse_down = self.mouse_down
        self.background = Texture(tool.image("system", "lab_bg.png"))
        self.status = 0
        self.status_backup = 0
        self.matches = 100
        self.current_match = 0
        self.team1_matches = 0
        self.team2_matches = 0
        
        self.po1_from = 375
        self.po1_cur = 375
        self.po1_to = 375
        self.po1_eggs = 0
        self.po2_from = 375
        self.po2_cur = 37
        self.po2_to = 375
        self.po2_eggs = 0
        
        self.pause_eggs = 0
        
        self.pause = Texture(tool.image("system", "pause.png"))
        self.restart = Texture(tool.image("system", "restart.png"))
        self.exit = Texture(tool.image("system", "exit.png"))
        
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 24, False, False, 32, 255)
        
        self.num_tex = Texture(tool.image("system", "plus_one.png"))
        self.num_up = []
        
    def draw(self):
        #str(self.domino.points_team1())
        #self.team1_matches
        Gloss.fill(self.background)

        self.p1.draw((25,  25))
        self.p3.draw((185, 25))
        self.p2.draw((465, 25))
        self.p4.draw((625, 25))

        if self.current_match != 0:
            po1_new = 375+((self.team1_matches-self.team2_matches)*3.75)
            po1_new2 = 750*self.team1_matches/(self.team1_matches+self.team2_matches)
            po1_new = po1_new2/2 + po1_new/2
            po2_new = 750-po1_new
        else:
            po1_new = 375
            po2_new = 375
        
        if po1_new != self.po1_to:
            self.po1_to = po1_new
            self.po1_from = self.po1_cur
            self.po1_eggs = 0
            self.po2_to = po2_new
            self.po2_from = self.po2_cur
            self.po2_eggs = 0
        
        self.po1_eggs += Gloss.elapsed_seconds * 2
        self.po2_eggs += Gloss.elapsed_seconds * 2
        self.po1_cur = Gloss.smooth_step(self.po1_from, self.po1_to, self.po1_eggs)
        self.po2_cur = Gloss.smooth_step(self.po2_from, self.po2_to, self.po2_eggs)
        
        Gloss.draw_box((25, 200), self.po1_cur, 50, 0.0, (0, 0), 1, Color.from_html("#f9b00c"))
        Gloss.draw_box((25, 200), self.po1_cur, 10, 0.0, (0, 0), 1, Color.from_html("#febf1a"))
        Gloss.draw_box((775-self.po2_cur, 200), self.po2_cur, 50, 0.0, (0, 0), 1, Color.from_html("#cccccc"))
        Gloss.draw_box((775-self.po2_cur, 200), self.po2_cur, 10, 0.0, (0, 0), 1, Color.from_html("#e0e0e0"))

        # los puntos de cada partida van de 0 a 200
        Gloss.draw_box((25, 275), (self.domino.points_team1()*375)/200, 25, 0.0, (0, 0), 1, Color.from_html("#f9b00c"))
        Gloss.draw_box((775, 275), (self.domino.points_team2()*375)/200, 25, 0.0, ((self.domino.points_team2()*375)/200, 0), 1, Color.from_html("#cccccc"))

        # pintamos las partidas ganadas encima de la barra
        text2_size = self.font_main.measure_string(str(self.team2_matches))
        self.font_main.draw(str(self.team1_matches), position = (35, 220), color = Color.WHITE)
        self.font_main.draw(str(self.team2_matches), position = (765-text2_size[0], 220), color = Color.WHITE)
        
        # pintamos los botones
        if self.status == 99:
            self.pause_eggs += Gloss.elapsed_seconds
            if self.pause_eggs > 1:
                self.pause_eggs = 0
            self.pause.draw(position = (25, 532), color = Color(1,1,1,Gloss.smooth_step2(0.5, 1, self.pause_eggs)))
        else:
            self.pause.draw(position = (25, 532))
        self.restart.draw(position = (426, 532))
        self.exit.draw(position = (638, 532))
        
        # pintamos los numeros de +1
        for number in self.num_up:
            number.draw(color = Color(1,1,1,Gloss.smooth_step(1, 0, number.movetime)))
        
    def update(self):
        for number in self.num_up:
            number.movetime += Gloss.elapsed_seconds
            if (number.movetime > 1.0): self.num_up.remove(number)
            number.move_to(None, Gloss.lerp(200, 180, number.movetime))
        if self.status == 0:
            pass
        elif self.status == 1:
            # comprobamos si hemos terminado todas las partidas
            if not self.current_match == self.matches:
                self.status = 2
            else:
                self.status = 999
        elif self.status == 2:
            # comprobamos si hemos terminado la partida actual
            if not self.domino.end_game():
                self.status = 3
                self.domino.deal_tiles()
            else:
                self.current_match += 1
                print self.current_match
                if self.domino.points_team1() > self.domino.points_team2(): 
                    self.team1_matches += 1
                    newnumber = Sprite(self.num_tex, (30, 200))
                    newnumber.position_from = 30
                else:
                    self.team2_matches += 1
                    newnumber = Sprite(self.num_tex, (744, 200))
                    newnumber.position_from = 744
                    
                # guardamos y actualizamos las estadísticas
                # FIXME
                
                self.domino.restart()
                self.status = 1
                newnumber.movetime = 0
                self.num_up.insert(0, newnumber)
        elif self.status == 3:
            # si no hemos terminado la mano actual, vamos pidiendo fichas
            while not self.domino.end_hand():
                self.domino.ask_tile(self.domino.nextplayer())
            self.status = 2
        elif self.status == 99:
            # modo pausa
            pass
        elif self.status == 999:
            # terminamos la partida
            print self.domino.stats
            if self.team1_matches > self.team2_matches:
                print "winner team 1"
            else:
                print "winner team 2"
            self.status = 99

    def start(self):
        self.status = 0
        self.domino.create_players(config['player1'],config['player2'],config['player3'],config['player4'])
        print "empieza el laboratorio"
        self.status = 1

        for player in allplayers:
            if config['player1'] == player['id']: self.p1 = Texture(player['image'])
            if config['player2'] == player['id']: self.p2 = Texture(player['image'])
            if config['player3'] == player['id']: self.p3 = Texture(player['image'])
            if config['player4'] == player['id']: self.p4 = Texture(player['image'])

        self.status_backup = 0
        self.matches = 100
        self.current_match = 0
        self.team1_matches = 0
        self.team2_matches = 0
            
    def stop(self):
        self.status = 0

    def mouse_down(self, event):
        if self.status != 1 and event.pos[0] > 25 and event.pos[1] > 532 and event.pos[0] < 186 and event.pos[1] < 574:
            if self.status == 99:
                self.status = self.status_backup
            else:
                self.status_backup = self.status
                self.status = 99
        elif event.pos[0] > 426 and event.pos[1] > 532 and event.pos[0] < 618 and event.pos[1] < 574:
            self.start()
        elif event.pos[0] > 638 and event.pos[1] > 532 and event.pos[0] < 775 and event.pos[1] < 574:
            self.game.goto_menu()
        