"""Dominoes human player

"""

class playerh:
    def __init__(self, dealed_tiles):
        self.tiles = dealed_tiles
    def human(self):
        return "True"
    def computer(self):
        return False
    def down_tile(self, left_tile, right_tile):
        return self.engine.get_player_tile()
        #print self.tiles
        #x = 0
        #while x != 1:
        #    tile = raw_input('Select a tile: ')
        #    side = raw_input('Select a side (left or right): ')
        #    if (tile in self.tiles):
        #        self.tiles.remove(tile)
        #        x = 1
        #        return tile, side
    def game_status(self):
        pass
