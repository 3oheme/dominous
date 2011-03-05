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
        self.background = Texture(tool.image("system", "lab_bg.png"))
        self.status = 0
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
        
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 24, False, False, 32, 255)
        
    def draw(self):
        #str(self.domino.points_team1())
        #self.team1_matches
        Gloss.fill(self.background)

        self.p1.draw((25,  25))
        self.p3.draw((185, 25))
        self.p2.draw((465, 25))
        self.p4.draw((625, 25))

        po1_new = 375+((self.team1_matches-self.team2_matches)*3.75)
        po2_new = 750-po1_new
        
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
        
        #Gloss.elapsed_seconds
    def update(self):
        if self.status == 0:
            pass
        elif self.status == 1:
            # comprobamos si hemos terminado todas las partidas
            if not self.current_match == self.matches:
                self.status = 2
            else:
                self.status = 99
        elif self.status == 2:
            # comprobamos si hemos terminado la partida actual
            if not self.domino.end_game():
                self.status = 3
                self.domino.deal_tiles()
            else:
                self.current_match += 1
                if self.domino.points_team1() > self.domino.points_team2(): 
                    self.team1_matches += 1 
                else:
                    self.team2_matches += 1
                self.domino.restart()
                self.status = 1
        elif self.status == 3:
            # si no hemos terminado la mano actual, vamos pidiendo fichas
            while not self.domino.end_hand():
                self.domino.ask_tile(self.domino.nextplayer())
            self.status = 2
        elif self.status == 99:
            if self.team1_matches > self.team2_matches:
                print "winner team 1"
            else:
                print "winner team 2"
            self.game.goto_intro()

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

    def stop(self):
        self.status = 0
