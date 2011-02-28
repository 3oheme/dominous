from pygame import *
from gloss import *
from dominoes_game import domino_game

from sound import *
from tools import *
from config import *

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
    def draw(self):
        #str(self.domino.points_team1())
        #self.team1_matches
        Gloss.fill(self.background)
        Gloss.draw_box((50, 50), self.team1_matches*4, 50, 0.0, (0, 0), 1, Color.BLUE)
        Gloss.draw_box((50, 110), self.team2_matches*4, 50, 0.0, (0, 0), 1, Color.BLUE)

        Gloss.draw_box((50, 200), self.domino.points_team1()*2, 20, 0.0, (0, 0), 1, Color.RED)
        Gloss.draw_box((50, 230), self.domino.points_team2()*2, 20, 0.0, (0, 0), 1, Color.RED)

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
    def stop(self):
        self.status = 0
