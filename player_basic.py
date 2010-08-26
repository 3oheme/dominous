"""Dominoes most basic computer player

This player just puts any available tile. You may use this file to create
your own player.
"""

class player1:
    def __init__(self, dealed_tiles):
        self.tiles = dealed_tiles
    def human(self):
        return "False"
    def computer(self):
        return True
    def down_tile(self, left_tile, right_tile):
        """place a tile"""
        for item in self.tiles:
            if item[0] == left_tile or item[1] == left_tile:
                self.tiles.remove(item)
                return item, "left"
                break
            elif item[0] == right_tile or item[1] == right_tile or left_tile == None:
                self.tiles.remove(item)
                return item, "right"
                break
        return None, "pass"
    def game_status(self):
        pass
