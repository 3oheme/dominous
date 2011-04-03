from tools import *

class AI:
    def __init__(self, left_tile, right_tile, board, tiles, log):
        self.left_tile = left_tile
        self.right_tile = right_tile
        self.board = board
        self.tiles = tiles
        self.log = log
    def go(self, knowledge):
        for step in knowledge:
            tile, side = step.go(self.left_tile, self.right_tile, self.board, self.tiles, self.log)
            if tile != None:
                return tile, side
                break
        return None, "pass"

class put_anyone:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log):
        for item in tiles:
            if item[0] == left_tile or item[1] == left_tile:
                tiles.remove(item)
                return item, "left"
                break
            elif item[0] == right_tile or item[1] == right_tile or left_tile == None:
                tiles.remove(item)
                return item, "right"
                break
        return None, "pass"

class put_any_double:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log):
        for item in tiles:
            if item[0] == item[1]:
                if item[0] == left_tile or item[1] == left_tile:
                    tiles.remove(item)
                    return item, "left"
                    break
                elif item[0] == right_tile or item[1] == right_tile or left_tile == None:
                    tiles.remove(item)
                    return item, "right"
                    break
        return None, "pass"

class starting_classic:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log):
        #print "try go with" + str(left_tile) + " and " + str(right_tile)
        if not board:
            # count how many tiles we have of each number
            counter = [0,0,0,0,0,0,0]
            for item in tiles:
                counter[int(item[0])] += 1
                counter[int(item[1])] += 1
            print ""
            print tiles
            print counter
            print tiles[1]
            print " MAX " + str(counter.index(max(counter)))
            raw_input()
            tiles.remove(tiles[1])
            return tiles[1], "right"
        else:
            return None, "pass"