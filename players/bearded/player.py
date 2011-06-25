"""Dominoes bearded computer player

"""
from ai import *

class Player:
    def __init__(self, dealed_tiles):
        self.tiles = dealed_tiles
        self.player_position = "1"
        self.knowledge = []
        self.knowledge.append([put_any_double(), weight_matrix(1000, 1000, 100, 50)])
        self.knowledge.append([put_anyone()])

    def human(self):
        return False
    def computer(self):
        return True
    def player_pos(self, pos):
        self.player_position = pos
    def down_tile(self, left_tile, right_tile, board, tiles, log):
        ai = AI(left_tile, right_tile, board, self.tiles, log)
        return ai.go(self.knowledge)
    def game_status(self):
        pass
