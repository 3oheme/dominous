from tools import *

class AI:
    def __init__(self, left_tile, right_tile, board, tiles, log):
        self.left_tile = left_tile
        self.right_tile = right_tile
        self.board = board
        self.tiles = tiles
        self.log = log
    def go(self, knowledge):
        # primero vemos cuantas podemos poner
        tiles_i_can_put = []
        for item in self.tiles:
            if item[0] == self.left_tile or item[1] == self.left_tile or item[0] == self.right_tile or item[1] == self.right_tile or self.left_tile == None:
                tiles_i_can_put.append(item)
        
        # si no podemos poner ninguna
        if len(tiles_i_can_put) == 0:
            return None, "pass"
        # si podemos poner solo una
        elif len(tiles_i_can_put) == 1:
            item = tiles_i_can_put[0]
            if item[0] == self.left_tile or item[1] == self.left_tile:
                self.tiles.remove(item)
                return item, "left"
            elif item[0] == self.right_tile or item[1] == self.right_tile or self.left_tile == None:
                self.tiles.remove(item)
                return item, "right"
        # si podemos poner varias, usamos la IA
        else:
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
            # generamos la matriz
            matriz = _weight_matrix(tiles)
            fin = _max_matrix(matriz)
            tiles.remove(fin)
            return fin, "right"
        else:
            return None, "pass"

class always_matrix:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log):
        matriz = _weight_matrix(tiles)
        fin = _max_matrix(matriz)
        if fin != "00":
            tiles.remove(fin)
            return fin, "right"
        else:
            return None, "pass"

#
# Helping functions
#

def _weight_matrix(tiles, number = 1000, double = 100, siblings = 10, size = 1):
    """@brief returns a weight matrix
    
    @param tiles must be an array of tiles strings
    @param number defines weight for just having this tile
    @param double defines weight if the tile is a double
    @param siblings defines weight added for each brother tile
    @param size defines weight added depending of number height 
    """ 
    table = [ [ 0 for i in range(7) ] for j in range(7) ]
    counter = [0,0,0,0,0,0,0]
    # calculamos peso de numeros y dobles
    for item in tiles:
        table[int(item[0])][int(item[1])] += number
        if item[0] != item[1]:
            table[int(item[1])][int(item[0])] += number
            counter[int(item[0])] += 1
            counter[int(item[1])] += 1
        else:
            table[int(item[1])][int(item[0])] += double
            counter[int(item[0])] += 1
            
    # calculamos los hermanos
    for i in range(7):
        for j in range(7):
            if table[i][j] != 0 and i != j:
                table[i][j] += (counter[i] + counter[j]) * siblings
            if table[i][j] != 0 and i == j:
                table[i][j] += counter[i] * siblings

    # valoramos las mas pesadas
    for i in range(7):
        for j in range(7):
            if table[i][j] != 0:
                table[i][j] += (j + i) * size
    return table
    
def _max_matrix(matrix):
    allmax = []
    for i in range(7):
        allmax.append(max(matrix[i]))
    mightymax = max(allmax)
    for i in range(7):
        for j in range(7):
            if matrix[i][j] == mightymax:
                return str(i)+str(j)