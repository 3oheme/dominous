# -*- coding: utf-8 -*-

from pygame import *
from gloss import *
from config import *

import random

from sound import *
from tools import *
from os import *

import imp

def load_players():
    players = []
    config = ConfigParser.RawConfigParser()
    players_dir = os.listdir(os.path.join(os.environ['PWD'], 'players'))
    for player_dir in players_dir:
        if player_dir[0] != '.':
            config.read(os.path.join(os.environ['PWD'], 'players', player_dir, 'player.ini'))
            player = {
                'id': player_dir,
                'ia': imp.load_source(player_dir, os.path.join(os.environ['PWD'], 'players', player_dir, 'player.py')),
                'name': config.get('Player', 'name'),
                'image': os.path.join(os.environ['PWD'], 'players', player_dir, config.get('Player', 'image')),
                }
            players.append(player)
    return players

allplayers = load_players()

class PlayerImage(Sprite):
    """Player image attached to a player selector
    @brief Player image attached to a player selector"""
    def __init__(self, player):
        self.scale = 0.6
        self.status = 1 # 1 = fixed position
                        # 2 = falling down
        self.eggs = 0
        pos = 0
        self.id = player
        for item in allplayers:
            if item['id'] == player:
                player = pos
            pos = pos + 1
        self.player = pos
        print allplayers[player]['image']
        self.texture = Texture(allplayers[player]['image'])
        self.scale = 0.3
        Sprite.__init__(self, self.texture, (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2))
    def draw(self):
        Sprite.draw(self, origin = (self.texture.half_width, self.texture.half_height), scale = self.scale) 
    def update(self):
        pass

class PlayerSelector():
    """Creates a player selector, where you can choose players just clicking on the image
    @brief Creates a player selector
    """
    def __init__(self, pos):
        """pos points about player position: 2nd, 3rd or 4th"""
        self.pos = pos
        self.selected = config["player" + str(pos)]
        self.player_images = [PlayerImage(self.selected)]
    def draw(self):
        for image in self.player_images:
            image.draw()
    def update(self):
        for image in self.player_images:
            image.update()
        
class SelectPlayers():
    """Select players state.
    @brief Select players state
    """
    def __init__(self, mainp):
        self.game = mainp
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
        self.background = Texture(tool.image("theme_bg", "background.png"))
        self.selectors = [ PlayerSelector(2), PlayerSelector(3), PlayerSelector(4)]
    def draw(self):
        Gloss.fill(self.background)
        if self.status == 1:
            for selector in self.selectors:
                selector.draw()
    def update(self):
        self.game.on_mouse_up = self.events
        if self.status == 1:
            for selector in self.selectors:
                selector.update()
    def start(self):
        self.fadein = True
        self.fadein_amount = 0
    def stop(self):
        pass
    def events(self, event):
        self.game.goto_game()
