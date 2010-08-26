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
    def game_status(self):
        pass
