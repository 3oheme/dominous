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
        self.background = Texture(tool.image("theme_bg", "background.png"))
    def draw(self):
        pass
    def update(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
        
