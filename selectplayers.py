# -*- coding: utf-8 -*-

from pygame import *
from gloss import *
from config import *

from sound import *
from tools import *
from os import *

import md5
import imp
import traceback

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

def load_players():
    players = {}
    config = ConfigParser.RawConfigParser()
    players_dir = os.listdir(os.path.join(os.environ['PWD'], 'players'))
    for player_dir in players_dir:
        if player_dir[0] != '.':
            config.read(os.path.join(os.environ['PWD'], 'players', player_dir, 'player.ini'))
            player = {
                'ia': imp.load_source(player_dir, os.path.join(os.environ['PWD'], 'players', player_dir, 'player.py')),
                'name': config.get('Player', 'name'),
                'image': config.get('Player', 'image'),
                }
            players[player_dir] = player
            

    players = ['sys', 'os', 're', 'unittest'] 
    modules = map(__import__, moduleNames)
    config = ConfigParser.RawConfigParser()
    config.read(file)
    config_default = {
        'name': config.get('General', 'name'),


class SelectPlayers():
    """Select players state.
    @brief Select players state
    """
    def __init__(self, mainp):
        self.game = mainp
        self.box = Box()
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
        load_players()
        
    def draw(self):
        Gloss.fill(top = Color.WHITE, bottom = Color(0.8, 0.8, 0.8, 1))
        self.box.draw()
        if self.fadein:
            next = Gloss.lerp(1, 0, self.fadein_amount)
            Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(1,1,1,next))
            self.fadein_amount += 0.05
            if next == 0:
                self.fadein = False
    def update(self):
        self.game.on_mouse_up = self.events
    def start(self):
        self.fadein = True
        self.fadein_amount = 0
        sound.credits()
    def stop(self):
        pass
    def events(self, event):
        self.game.goto_game()
