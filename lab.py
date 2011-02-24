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
        Gloss.fill(self.background)        
    def update(self):
        if self.status == 0:
            pass
        elif self.status == 1:
            while not self.current_match == self.matches:
                while not self.domino.end_game():
                    print "holaaaaa"
                    self.domino.deal_tiles()
                    while not self.domino.end_hand():
                        self.domino.ask_tile(self.domino.nextplayer())
                    print "Equipo 1: "+ str(self.domino.points_team1()) + "    Equipo 2 " + str(self.domino.points_team2())
                if self.domino.points_team1() > self.domino.points_team2():
                    self.team1_matches += 1
                else:
                    self.team2_matches += 1
                self.domino.restart()
                self.current_match += 1
                print ""
                print "Equipo 1: "+ str(self.team1_matches) + "    Equipo 2 " + str(self.team2_matches)
                print ""
            self.status = 2
        elif self.status == 2:
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
