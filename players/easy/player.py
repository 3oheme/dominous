"""Dominoes most basic computer player

This player just puts any available tile. You may use this file to create
your own player.
"""
from ai import *

class Player:
    def __init__(self, dealed_tiles):
        self.tiles = dealed_tiles
        self.knowledge = []
        self.knowledge.append(put_any_double())
        self.knowledge.append(put_anyone())
        self.player_position = "1" # player_pos = 1 - Player that starts this hand
                                   #              2 - Second player
                                   #              3 - Third player, plays with player 1
                                   #              4 - Second player
    def human(self):
        return False
    def computer(self):
        return True
    def player_pos(self, pos):
        self.player_position = pos
    def down_tile(self, left_tile, right_tile, board, tiles, log):
        ai = AI(left_tile, right_tile, board, self.tiles, log)
        print "Soy el jugador easy"
        return ai.go(self.knowledge)
    def game_status(self):
        pass
