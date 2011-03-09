# -*- coding: utf-8 -*-

from pygame import *
from gloss import *
from config import *

import random

from sound import *
from tools import *
from os import *

import imp

import operator 

def load_players():
    players = []
    config = ConfigParser.RawConfigParser()
    players_dir = os.listdir(os.path.join(os.getcwd(), 'players'))
    for player_dir in players_dir:
        if player_dir[0] != '.':
            config.read(os.path.join(os.getcwd(), 'players', player_dir, 'player.ini'))
            player = {
                'id': player_dir,
                'ia': imp.load_source(player_dir, os.path.join(os.getcwd(), 'players', player_dir, 'player.py')),
                'name': config.get('Player', 'name'),
                'weight': config.get('Player', 'weight'),
                'image': os.path.join(os.getcwd(), 'players', player_dir, config.get('Player', 'image')),
                }
            players.append(player)
    # sort by weight
    players.sort(key=operator.itemgetter('weight'))
    return players

allplayers = load_players()

class PlayerSelector(Sprite):
    """Player selector, where you can choose players just clicking on the image
    @brief Player selector
    """
    def __init__(self, pos, is_static = False):
        """pos points about player position, clockwise - 1st player is bottom player"""
        self.pos = pos
        self.selected = allplayers[0]['id']
        self.player_selected = 0
        self.static = is_static
        if not is_static:
            self.texture = Texture(allplayers[self.player_selected]['image'])
        else:
            self.texture = Texture(tool.image("system", "human.png"))
        self.player_selected_id = allplayers[self.player_selected]['id']
        tex_width = self.texture.width
        tex_half_width = self.texture.half_width
        gap = Gloss.screen_resolution[1]/20
        self.scale = 1
        if pos == 1:
            self.x = (Gloss.screen_resolution[0]/2)-tex_half_width
            self.y = Gloss.screen_resolution[1]-gap-tex_width
        elif pos == 2:
            self.x = Gloss.screen_resolution[0]-gap-tex_width
            self.y = (Gloss.screen_resolution[1]/2)-tex_half_width
        elif pos == 3:
            self.x = (Gloss.screen_resolution[0]/2)-tex_half_width
            self.y = gap
        elif pos == 4:
            self.x = gap
            self.y = (Gloss.screen_resolution[1]/2)-tex_half_width
        self.position = (self.x, self.y)
        Sprite.__init__(self, self.texture, self.position)
        self.falling_images = []
    def draw(self):
        Sprite.draw(self, position = self.position, scale = self.scale)
        for falling_image in self.falling_images:
            falling_image.draw(origin = (75, 75), rotation = falling_image.movetime*20, color = Color(1,1,1,Gloss.smooth_step(1, 0, falling_image.movetime)))
    def update(self):
        for falling_image in self.falling_images:
            falling_image.movetime += Gloss.elapsed_seconds * 2
            if (falling_image.movetime > 1.0): self.falling_images.remove(falling_image)
            # FIXME
            falling_image.move_to(None, Gloss.lerp(self.position[1]+75, self.position[1]+100, falling_image.movetime))
    def click(self):
        if not self.static:
            self.player_selected = self.player_selected + 1
            falling_image = Sprite(self.texture, (self.position[0] + 75, self.position[1]))
            falling_image.movetime = 0
            self.falling_images.insert(0, falling_image)
            if self.player_selected + 1 > len(allplayers):
                self.player_selected = 0
            self.texture = Texture(allplayers[self.player_selected]['image'])
            self.player_selected_id = allplayers[self.player_selected]['id']
    def option(self):
        return self.player_selected_id
        
class SelectPlayers():
    """Select players state.
    @brief Select players state
    """
    def __init__(self, mainp):
        self.game = mainp
        self.fadein = True
        self.fadein_amount = 0
        self.status = 0
        self.game.on_mouse_down = self.mouse_down
        self.falling_images = []
    def draw(self):
        if self.status == 1:
            Gloss.fill(self.background)
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
        self.background = Texture(tool.image("system", "select_player_bg.png"))
        self.game.on_mouse_down = self.mouse_down
        if config['gametype'] == 'human':
            self.selectors = [PlayerSelector(1, True), PlayerSelector(2), PlayerSelector(3), PlayerSelector(4)]
        else:
            self.selectors = [PlayerSelector(1), PlayerSelector(2), PlayerSelector(3), PlayerSelector(4)]
        print "start de selectplayers"
    def stop(self):
        self.status = 0
        config['player1'] = self.selectors[0].option()
        config['player2'] = self.selectors[1].option()
        config['player3'] = self.selectors[2].option()
        config['player4'] = self.selectors[3].option()
        print "stop de selectplayers"
    def mouse_down(self, event):
        if self.status != 0:
            gap = Gloss.screen_resolution[1]/20
            tex_half_width = 75
            tex_width = 150
            if event.pos[0] > (Gloss.screen_resolution[0]/2)-tex_half_width and event.pos[0] < (Gloss.screen_resolution[0]/2)+tex_half_width and \
                event.pos[1] > Gloss.screen_resolution[1]-gap-tex_width and event.pos[1] < Gloss.screen_resolution[1]-gap+tex_width:
                self.selectors[0].click()
            elif event.pos[0] > gap and event.pos[0] < gap+tex_width and \
                event.pos[1] > (Gloss.screen_resolution[1]/2)-tex_half_width and event.pos[1] < (Gloss.screen_resolution[1]/2)+tex_half_width:
                self.selectors[3].click()
            elif event.pos[0] > (Gloss.screen_resolution[0]/2)-tex_half_width and event.pos[0] < (Gloss.screen_resolution[0]/2)+tex_half_width and \
                event.pos[1] > gap and event.pos[1] < gap+tex_width:
                self.selectors[2].click()
            elif event.pos[0] > Gloss.screen_resolution[0]-gap-tex_width and event.pos[0] < Gloss.screen_resolution[0]-gap and \
                event.pos[1] > (Gloss.screen_resolution[1]/2)-tex_half_width and event.pos[1] < (Gloss.screen_resolution[1]/2)+tex_half_width:
                self.selectors[1].click()
            elif event.pos[0] > Gloss.screen_resolution[0]-tex_width and event.pos[1] > Gloss.screen_resolution[1]-tex_width:
                if config['goto_lab']:
                    self.game.goto_lab()
                else:
                    self.game.goto_game()
