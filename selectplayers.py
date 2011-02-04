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
    def __init__(self, player, x, y):
        self.status = 1 # 1 = fixed position
                        # 2 = falling down
        self.eggs = 0
        self.speed = 1
        temp_pos = 0
        self.id = player
        for item in allplayers:
            if item['id'] == player:
                player = temp_pos
            temp_pos = temp_pos + 1
        self.player = temp_pos
        self.texture = Texture(allplayers[player]['image'])
        self.scale = 0.3
        self.pos = (x, y)
        self.to_pos = (x, y+100)
        self.falling = False
        Sprite.__init__(self, self.texture, self.pos)
    def draw(self):
        Sprite.draw(self, position = self.pos, scale = self.scale) 
    def update(self):
        x, y = self.pos
        self.pos = (x+1, y+1)
    def remove(self):
        self.falling = True

class PlayerSelector(Sprite):
    """Player selector, where you can choose players just clicking on the image
    @brief Player selector
    """
    def __init__(self, pos):
        """pos points about player position: 2nd, 3rd or 4th"""
        self.pos = pos
        gap = Gloss.screen_resolution[1]/20
        if pos == 1:
            self.x = Gloss.screen_resolution[0]-gap
            self.y = (Gloss.screen_resolution[1]/2)-gap
        elif pos == 2:
            self.x = gap
            self.y = Gloss.screen_resolution[1]/2
        elif pos == 3:
            self.x = Gloss.screen_resolution[0]/2
            self.y = gap
        elif pos == 4:
            self.x = Gloss.screen_resolution[0]-gap
            self.y = Gloss.screen_resolution[1]/2
        self.selected = allplayers[0]['id']
        self.player_selected = 0
        self.scale = 0.3
        self.position = (self.x, self.y)
        self.texture = Texture(allplayers[self.player_selected]['image'])
        Sprite.__init__(self, self.texture, self.position)
    def draw(self):
        Sprite.draw(self, position = self.position, scale = self.scale)
    def update(self):
        pass
    def click(self):
        self.player_selected = self.player_selected + 1
        if self.player_selected + 1 > len(allplayers):
            self.player_selected = 0
        print allplayers
        print self.player_selected
        self.texture = Texture(allplayers[self.player_selected]['image'])
        print "click en selector " + str(self.pos) + ", ahora tiene el valor" + str(self.player_selected)
    def option(self):
        return self.player_selected
        
class SelectPlayers():
    """Select players state.
    @brief Select players state
    """
    def __init__(self, mainp):
        self.game = mainp
        self.fadein = True
        self.fadein_amount = 0
        self.status = 0
        self.background = Texture(tool.image("theme_bg", "background.png"))
        if config['gametype'] == 'human':
            self.selectors = [PlayerSelector(2), PlayerSelector(3), PlayerSelector(4)]
        else:
            self.selectors = [PlayerSelector(1), PlayerSelector(2), PlayerSelector(3), PlayerSelector(4)]
        self.game.on_mouse_down = self.mouse_down
        self.falling_images = []
    def draw(self):
        Gloss.fill(self.background)
        if self.status == 1:
            for selector in self.selectors:
                selector.draw()
            for falling_image in self.falling_images:
                falling_image.draw()
    def update(self):
        if self.status == 1:
            for selector in self.selectors:
                selector.update()
    def start(self):
        self.fadein = True
        self.fadein_amount = 0
        self.status = 1
    def stop(self):
        self.status = 0
        pass
    def mouse_down(self, event):
        if self.status != 0:
            print "event.pos[0] = " + str(event.pos[0])
            if event.pos[0] > Gloss.screen_resolution[1]/2:
                self.selectors[1].click()
            else:
                self.selectors[2].click()

