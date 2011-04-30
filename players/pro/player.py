"""Dominoes Pro computer player

"""
from ai import *

class Player:
    def __init__(self, dealed_tiles):
        self.tiles = dealed_tiles
        # player_pos = 1 - Player that starts this hand
        #              2 - Second player
        #              3 - Third player, plays with player 1
        #              4 - Second player
        self.player_position = "1"
        
        # depending of player position, we will use one or another strategy
        self.global_knowledge = [[], [], [], []]
        
        # if I am hand player - player 1
        #self.global_knowledge[0].append(starting_classic())
        self.global_knowledge[0].append(put_any_double())
        self.global_knowledge[0].append(put_anyone())
        
        # I am second player, im trying to break p1 game
        self.global_knowledge[1].append(put_anyone())
        
        # I am helping player 1
        self.global_knowledge[2].append(put_anyone())
        
        # This is gonna be soooo hard...
        self.global_knowledge[3].append(put_anyone())

    def human(self):
        return False
    def computer(self):
        return True
    def player_pos(self, pos):
        self.player_position = pos
    def down_tile(self, left_tile, right_tile, board, tiles, log):
        #print left_tile
        #print right_tile
        if left_tile is None and right_tile is None:
            print "tanto left_tile como right_tile son none, y yo soy el jugador " + str(self.player_position)
        ai = AI(left_tile, right_tile, board, self.tiles, log)
        return ai.go(self.global_knowledge[self.player_position-1])
    def game_status(self):
        pass
