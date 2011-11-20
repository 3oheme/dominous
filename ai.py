from tools import *

class AI:
    def __init__(self, left_tile, right_tile, board, tiles, log, mypos):
        self.left_tile = left_tile
        self.right_tile = right_tile
        self.board = board
        self.tiles = tiles
        self.log = log
        self.mypos = mypos
    def go(self, knowledge):
        # primero vemos cuantas podemos poner
        tiles_i_can_put = []
        for item in self.tiles:
            if item[0] == self.left_tile or item[1] == self.left_tile or \
                item[0] == self.right_tile or item[1] == self.right_tile or self.left_tile == None:
                tiles_i_can_put.append(item)
        
        # si no podemos poner ninguna pasamos y listo
        if len(tiles_i_can_put) == 0:
            return None, "pass", 0
            
        # si podemos poner solo una la ponemos y listo
        elif len(tiles_i_can_put) == 1:
            item = tiles_i_can_put[0]
            if item[0] == self.left_tile or item[1] == self.left_tile:
                self.tiles.remove(item)
                return item, "left", 0
            elif item[0] == self.right_tile or item[1] == self.right_tile or self.left_tile == None:
                self.tiles.remove(item)
                return item, "right", 0
                
        # si podemos poner varias, usamos la IA
        else:
            for priority in knowledge:
                if len(priority) > 1:
                    iterator = random.sample(range(0, len(priority)), len(priority))
                    for step in iterator:
                        tile, side, mtime = priority[step].go(self.left_tile, self.right_tile, self.board, self.tiles, self.log, self.mypos)
                        if tile != None:
                            return tile, side, mtime
                            break
                else:
                    tile, side, mtime = priority[0].go(self.left_tile, self.right_tile, self.board, self.tiles, self.log, self.mypos)
                    if tile != None:
                        return tile, side, mtime
                        break
        return None, "pass", 0

class put_anyone:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log, mypos):
        for item in tiles:
            if item[0] == left_tile or item[1] == left_tile:
                tiles.remove(item)
                return item, "left", 1
                break
            elif item[0] == right_tile or item[1] == right_tile or left_tile == None:
                tiles.remove(item)
                return item, "right", 1
                break
        return None, "pass", 0

class put_any_double:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log, mypos):
        for item in tiles:
            if item[0] == item[1]:
                if item[0] == left_tile or item[1] == left_tile:
                    tiles.remove(item)
                    return item, "left", 1
                    break
                elif item[0] == right_tile or item[1] == right_tile or left_tile == None:
                    tiles.remove(item)
                    return item, "right", 1
                    break
        return None, "pass", 0
        
class starting_classic:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log, mypos):
        if not board:
            # generamos la matriz
            matriz = _weight_matrix(tiles)
            fin = _max_matrix(matriz)
            tiles.remove(fin)
            return fin, "right", 1
        else:
            return None, "pass", 0

class force_passing:
    def __init__(self):
        pass
    def go(self, left_tile, right_tile, board, tiles, log, mypos):
        passed_tiles = _tiles_passed_next_player(mypos, log)
        """print "***************************"
        print var
        print "***************************"
        print "" """
        for item in tiles:
            if (item[0] == left_tile and item[1] in passed_tiles) or (item[1] == left_tile and item[0] in passed_tiles):
                tiles.remove(item)
                nextplayer = (mypos % 4) + 1
                print "yuhu! como el usuario " + str(nextplayer) + " antes paso, nosotros colocamos el " + item
                print log
                raw_input("Press any Key")
                return item, "left", 1
                break
            elif (item[0] == right_tile and item[1] in passed_tiles) or (item[1] == right_tile and item[0] in passed_tiles):
                tiles.remove(item)
                nextplayer = (mypos % 4) + 1
                print "yuhu! como el usuario " + str(nextplayer) + " antes paso, nosotros colocamos el " + item
                print log
                raw_input("Press any Key")
                return item, "right", 1
                break
        return None, "pass", 0
            
class weight_matrix:
    def __init__(self, mnumber = 1000, mdouble = 100, msiblings = 10, msize = 1):
        self.number = mnumber
        self.double = mdouble
        self.siblings = msiblings
        self.size = msize
    def go(self, left_tile, right_tile, board, tiles, log, mypos):
        matriz = _weight_matrix(tiles, self.number, self.double, self.siblings, self.size)
        fin, side, mtime = _max_matrix(matriz, left_tile, right_tile)
        if fin != None:
            tiles.remove(fin)
            return fin, side, mtime
        else:
            return None, "pass", 0

#
# Helping functions
#

def _tiles_passed_next_player(myposition, log):
    """@brief returns an array of numbers player in my right has passed
    
    example: if I'm player 2, and player 3 has passed with 4 and 6, it will return an array
        with 4 and 6, so I can try to make him pass again
    """
    next_player = (myposition % 4) + 1
    #print "we are player " + str(myposition) + " and we are looking to player " + str(next_player)
    passed_tiles = []
    for movement in log.hands[log.current_hand]:
        #print movement
        if movement['player'] == next_player and movement['tile'] == None:
            passed_tiles.append(movement['left']);
            passed_tiles.append(movement['right']);
    # remove duplicates
    passed_tiles = list(set(passed_tiles))
    return passed_tiles

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
    
def _max_matrix(matrix, left_tile, right_tile):
    """@brief returns max tile for a weight matrix
    """
   
    # quitamos de la matriz las fichas que no podemos colocar
    if left_tile != None:
        for i in range(7):
            for j in range(7):
                if i != int(left_tile) and i != int(right_tile) and j != int(left_tile) and j != int(right_tile):
                    matrix[i][j] = 0

    allmax = []
    for i in range(7):
        allmax.append(max(matrix[i]))
    mightymax = max(allmax)
    
    if mightymax == 0:
        return None, "pass", 0
    
    for i in range(7):
        for j in range(7):
            if matrix[i][j] == mightymax:
                if left_tile == str(i) or left_tile == str(j):
                    return str(i)+str(j), "left", 2
                else:
                    return str(i)+str(j), "right", 2
    return None, "pass", 0