from pygame import *
from gloss import *

from tools import *

import os
import ConfigParser

def load_config():
    """ @brief loads a config dictionary
    
    This function reads game configuration from a file. It tries to read config
    from file, if does not exists (first execution) it creates a new file with
    default config.
    """
    file = "config.ini"

    config = ConfigParser.RawConfigParser()

    if not os.path.exists(file):
        # file does not exist, so lets create it
        config.add_section('General')
        config.set('General', 'name', 'Dominous')
        config.set('General', 'window_caption', 'Dominous, an open source dominoes simulator')
        config.set('General', 'lang', 'en')
        config.add_section('Screen')
        config.set('Screen', 'window_width', '800')
        config.set('Screen', 'window_height', '600')
        config.set('Screen', 'full_screen', 'false')
        config.set('Screen', 'window_favicon', os.path.join('images', 'favicon.png'))
        config.add_section('Theme')
        config.set('Theme', 'theme', 'spanish')
        config.add_section('Game')
        config.set('Game', 'player2', 'easy')
        config.set('Game', 'player3', 'easy')
        config.set('Game', 'player4', 'easy')
        # writing our configuration file to file
        with open(file, 'wb') as configfile:
            config.write(configfile)

    # load file
    config = ConfigParser.RawConfigParser()
    config.read(file)
    config_default = {
        'name': config.get('General', 'name'),
        'window_caption': config.get('General', 'window_caption'),
        'window_width': config.getint('Screen', 'window_width'),
        'window_height': config.getint('Screen', 'window_height'),
        'full_screen': config.getboolean('Screen', 'full_screen'),
        'window_favicon': config.get('Screen', 'window_favicon'),
        'tile_width': 525,
        'tile_height': 270,
        'scale': 0.2,
        'theme': config.get('Theme', 'theme'),
        'lang': config.get('General', 'lang'),
        'gametype': 'human',
        'player1': 'easy',
        'player2': 'easy',
        'player3': 'easy',
        'player4': 'easy',
        }
    return config_default

def save_config(config_new):
    config = ConfigParser.RawConfigParser()
    config.add_section('General')
    config.set('General', 'name', 'Dominous')
    config.set('General', 'window_caption', 'Dominous, an open source dominoes simulator')
    config.set('General', 'lang', config_new['lang'])
    config.add_section('Screen')
    config.set('Screen', 'window_width', config_new['window_width'])
    config.set('Screen', 'window_height', config_new['window_height'])
    config.set('Screen', 'full_screen', config_new['full_screen'])
    config.set('Screen', 'window_favicon', os.path.join('images', 'favicon.png'))
    config.add_section('Theme')
    config.set('Theme', 'theme', config_new['theme'])
    # writing our configuration file to file
    with open("config.ini", 'wb') as configfile:
        config.write(configfile)

config = load_config()
