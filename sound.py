from pygame import *
from gloss import *

from tools import *

import os
import random

class Sound:
    def __init__(self):
        pass
        pygame.mixer.init(44100, 16, 2, 4096)
        self.tile_sound = [
            pygame.mixer.Sound(tool.sound("theme_tile", "tile1.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile2.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile3.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile4.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile5.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile6.ogg")),
            pygame.mixer.Sound(tool.sound("theme_tile", "tile7.ogg"))]
        self.intro_sound = pygame.mixer.Sound(tool.sound("system", "intro_dominous.ogg"))
        self.menu_sound = pygame.mixer.Sound(tool.sound("system", "menu.ogg"))
        self.credits_sound = pygame.mixer.Sound(tool.sound("system", "credits.ogg"))
    def tile(self):
        self.tile_sound[random.randrange(0,7)].play()
    def intro(self):
        self.intro_sound.play()
    def menu(self):
        pygame.mixer.fadeout(500)
        self.menu_sound.play()
    def credits(self):
        pygame.mixer.fadeout(1000)
        self.credits_sound.play()

sound = Sound()