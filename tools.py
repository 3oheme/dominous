#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dominous - dominoes simulator
#
# Developed by Ignacio Palomo Duarte
#    mail: ignacio.palomo.duarte@gmail.com
#    web:  http://www.3oheme.com/dominous

# Helping functions

import os, random
import log
from config import *

class Dtools:
    def __init__(self):
        pass
    def image(self, space, name = None):
        """ @brief helper function for getting path images.
            @param space can be:
                system - images for intro, gui, logo and menu
                theme_tiles - ingame tile images
                theme_bg - random ingame background from background directory
            @returns the path (OS sensitive) of the image. If image does not exists it will return
            a default image, and write the error in a log file"""
        if space == 'system':
            path = os.path.join("images", name)
        elif space == 'theme_tile':
            path = os.path.join("themes", config['theme'], "images", "tiles", name)
        elif space == 'theme_gui':
            path = os.path.join("themes", config['theme'], "images", "gui", name)
        elif space == 'theme_bg':
            file = random.choice([x for x in os.listdir(os.path.join("themes", config['theme'], "images", "background")) if os.path.isfile(os.path.join("themes", config['theme'], "images", "background", x))])
            path = os.path.join("themes", config['theme'], "images", "background", file)
        else:
            path = ''

        if os.path.exists(path):
            return path
        else:
            log.write('Cannot found image %s in path %s' % (name, path))
            path = os.path.join("images", "error.png")
            if os.path.exists(path):
                return path
            else:
                log.write('OMG, cannot load default image - this is very strange :-(')

    def ai(self, player):
        return os.path.join("players", player, "rules.clp")

    def sound(self, space, name):
        """ @brief helper function for getting the path of music and effect sounds.
            Mainly used from sound.py and sound object.
            @param space can be:
                system - music for intro, gui, logo and menu
                theme  - ingame music, like tile hit and game music
            @returns the path (OS sensitive) of the sound. If file does not exists it will return
            a default sound, and write the error in a log file"""
        if space == 'system':
            path = os.path.join("sounds", name)
        elif space == 'theme_tile':
            path = os.path.join("themes", config['theme'], "sounds", "tiles", name)
        elif space == 'theme_music':
            path = os.path.join("themes", config['theme'], "sounds", "music", name)
        elif space == 'theme_ambient':
            path = os.path.join("themes", config['theme'], "sounds", "ambient", name)
        else:
            path = ''

        if os.path.exists(path):
            return path
        else:
            log.write('Cannot load sound: %s ' % name)
            path = os.path.join("sounds", "tile1.ogg")
            if os.path.exists(path):
                return path
            else:
                log.write('OMG, cannot load default sound - this is very strange :-(')

tool = Dtools()
