import random
from player_basic import player1
from player_human import playerh
from selectplayers import *

import log
import copy

import datetime

class GameLog:
    """@brief Log class to save a complete game
    """
    def __init__(self, date, place, max_points, player1, player2, player3, player4, description):
        self.info = {
            "date" : date,
            "place" : place,
            "max_points" : max_points,
            "player1" : player1,
            "player2" : player2,
            "player3" : player3,
            "player4" : player4,
            "team1" : player1 + " " + player3,
            "team2" : player2 + " " + player4,
            "description" : description,
            "winner_team" : "",
            "team1_points" : 0,
            "team2_points" : 0,
        }
        self.hands = [[]]
        self.current_hand = 0
    def move(self, player, tile, side, left, right, mtime = 0):
        # time is the time player took while thinking.
        # values:   0 = I din't have to think, just one tile available to play
        #           1 = I have many posibilities
        #           2 = Really long time thinking
        movement = {
            'player' : player,
            'tile' : tile,
            'side' : side,
            'left' : left,
            'right' : right,
            'mtime' : mtime,
        }
        self.hands[self.current_hand].append(movement)
    def end_hand(self, team1_points, team2_points):
        self.current_hand += 1
        self.hands.append([])
        self.info['team1_points'] = team1_points
        self.info['team2_points'] = team2_points
    def end_game(self):
        if int(self.info['team1_points']) > self.info['max_points']:
            self.info['winner_team'] = self.info['player1'] + " " + self.info['player3'] 
        else:
            self.info['winner_team'] = self.info['player2'] + " " + self.info['player4'] 
    def __str__(self):
        print "INFORMACION"
        for k, v in self.info.items():
            print k + ": " + str(v)
        print ""
        iter = 1
        for hand in self.hands:
            print "MANO NUM " + str(iter)
            iter += 1
            for move in hand:
                print " " + str(move['player']) + " - " + str(move['tile']) + " - " + str(move['side']) \
                    + " - " + str(move['left']) + " - " + str(move['right']) + " - " + str(move['mtime'])
            print ""
        return ""

class domino_game:
    """@brief Game class to manage a full dominoes game
    
    Includes methods to shuffle domino tiles, deal them to players, ask players to
    down tiles and checking game and players are properly playing using defined
    rules.

    Currently it just supports International dominoes game type, two teams of two
    players playing one against the other, finishing when reaching 200 points. For
    more info you can follow the next link
    http://es.wikipedia.org/wiki/Domin%C3%B3#Modalidad_Domin.C3.B3_Internacional
    """
    # Methods
    def __init__(self):
        self.points = config['points_per_game']
        self.next_player = 0
        self.points_team_1 = 0
        self.points_team_2 = 0
        self.hand_counter = 0
        self.step_counter = 0
        self.player_started = 0
        self.tiles = ["00", "01", "02", "03", "04", "05", "06",
                      "11", "12", "13", "14", "15", "16",
                      "22", "23", "24", "25", "26",
                      "33", "34", "35", "36",
                      "44", "45", "46",
                      "55", "56",
                      "66"]
        self.board = []
        self.left_tile  = None
        self.right_tile = None
        self.first_tile = "00"
        self.players_tiles = [[], [], [], []]
        self.players = []
        self.player_pass = 0
        self.player_type = [1, 1, 1, 1]
        # FIXME rellenar con valores reales
        self.gamelog = GameLog(datetime.datetime.now(), "home", self.points, "hola1", "hola2", "hola3", "hola4", "lorem ipsum")
        self.stats = {
            'player_pass' : [0, 0, 0, 0],
            'player_win' : [0, 0, 0, 0],
            'game_close' : 0,
            'hands_played' : 0,
            'greatest_close' : [0, 0]
        }
    def create_players(self, p1, p2, p3, p4):
        """@brief generates players

        Generates 4 players. Each player can be human "h" or computer.

        @param p1 defines player 1 behaviour
        @param p2 defines player 2 behaviour
        @param p3 defines player 3 behaviour
        @param p4 defines player 4 behaviour
        """
        # god: Oh myself, this code makes me so sad i should kill some kitten
        # me: but it works, so shut up
        # god: no, it doesn't, you silly faggot
        # me: ok, i'll fix it tomorrow
        # me: done!
        # god: ok, much better
        
        if p1 == "h":
            self.players.append(playerh(self.players_tiles[0]))
        else:
            for item in allplayers:
                if item['id'] == p1:
                    self.players.append(item['ia'].Player(self.players_tiles[0]))
                    break
        for item in allplayers:
            if item['id'] == p2:
                self.players.append(item['ia'].Player(self.players_tiles[1]))
                break
        for item in allplayers:
            if item['id'] == p3:
                self.players.append(item['ia'].Player(self.players_tiles[2]))
                break
        for item in allplayers:
            if item['id'] == p4:
                self.players.append(item['ia'].Player(self.players_tiles[3]))
                break
        self.player_type = [p1, p2, p3, p4]
    def currentplayer(self):
        return self.next_player
    def nextplayer(self):
        if self.hand_counter == 1 and len(self.board) == 0:
            """player with 66 starts"""
            if "66" in self.players_tiles[0]:
                self.player_started = 0
            elif "66" in self.players_tiles[1]:
                self.player_started = 1
            elif "66" in self.players_tiles[2]:
                self.player_started = 2
            elif "66" in self.players_tiles[3]:
                self.player_started = 3
            self.next_player = self.player_started
            return self.player_started
        elif len(self.board) == 0:
            self.player_started = (self.player_started + 1) % 4
            self.next_player = self.player_started
            
            self.players[self.next_player].player_pos(1)
            self.players[(self.next_player+1)%4].player_pos(2)
            self.players[(self.next_player+2)%4].player_pos(3)
            self.players[(self.next_player+3)%4].player_pos(4)
            return self.player_started
        else:
            self.next_player = (self.next_player + 1) % 4
            self.step_counter += 1
            return self.next_player
    def points_team1(self): return self.points_team_1
    def points_team2(self): return self.points_team_2
    def points_hand_team(self, team):
        if team == 1 or team == 2:
            points_hand = 0
            for item in self.players_tiles[team-1]:
                points_hand = points_hand + int(item[0]) + int(item[1])
            for item in self.players_tiles[team+1]:
                points_hand = points_hand + int(item[0]) + int(item[1])
            return points_hand
        else:
            return False
    def print_hand(self):
        #print self.board
        #print "player 1: %s" % self.players_tiles[0]
        #print "player 2: %s" % self.players_tiles[1]
        #print "player 3: %s" % self.players_tiles[2]
        #print "player 4: %s" % self.players_tiles[3]
        #print ""
        pass
    def deal_tiles(self):
        self.hand_counter += 1
        del self.board[:]
        del self.players_tiles[0][:]
        del self.players_tiles[1][:]
        del self.players_tiles[2][:]
        del self.players_tiles[3][:]
        #random.seed(1) #starts player 3
        #random.seed(2) #starts player 1
        #random.seed(4) #starts player 2
        #random.seed(5) #starts player 4
        random.shuffle(self.tiles)
        tiles_position = 0;
        self.step_counter = 0
        self.left_tile = None
        self.right_tile = None
        for item in self.tiles:
            self.players_tiles[tiles_position].append(item)
            if item == "66" and self.hand_counter == 1:
                self.players[tiles_position].player_pos(1)
                tiles_position = (tiles_position+1) % 4
                self.players[tiles_position].player_pos(2)
                tiles_position = (tiles_position+1) % 4
                self.players[tiles_position].player_pos(3)
                tiles_position = (tiles_position+1) % 4
                self.players[tiles_position].player_pos(4)
                tiles_position = (tiles_position+1) % 4
            else:
                self.players[self.player_started].player_pos(1)
            tiles_position = (tiles_position+1) % 4
            
    def create_gamelog(self):
        pass
    def end_hand(self):
        if len(self.players_tiles[0]) == 0 or len(self.players_tiles[2]) == 0:
            self.stats['player_win'][self.next_player] += 1
            self.points_team_1 = self.points_team_1 + self.points_hand_team(1) + self.points_hand_team(2)
            self.player_pass = 0
            self.stats['hands_played'] += 1
            self.gamelog.end_hand(self.points_team_1, self.points_team_2)
            return True
        elif len(self.players_tiles[1]) == 0 or len(self.players_tiles[3]) == 0:
            self.stats['player_win'][self.next_player] += 1
            self.points_team_2 = self.points_team_2 + self.points_hand_team(1) + self.points_hand_team(2)
            self.player_pass = 0
            self.hand_counter = self.hand_counter + 1
            self.stats['hands_played'] += 1
            self.gamelog.end_hand(self.points_team_1, self.points_team_2)
            return True
        elif self.player_pass == 4:
            if self.points_hand_team(1) < self.points_hand_team(2):
                #print "after draw, team 1 wins!"
                #print "team_1: %s" % self.points_hand_team(1)
                #print "team_2: %s" % self.points_hand_team(2)
                self.points_team_1 = self.points_team_1 + self.points_hand_team(1) + self.points_hand_team(2)
                if (self.stats['greatest_close'][0] < self.points_hand_team(1) + self.points_hand_team(2)):
                    self.stats['greatest_close'][0] = self.points_hand_team(1) + self.points_hand_team(2)
            elif self.points_hand_team(1) > self.points_hand_team(2):
                #print "after draw, team 2 wins!"
                #print "team_1: %s" % self.points_hand_team(1)
                #print "team_2: %s" % self.points_hand_team(2)
                self.points_team_2 = self.points_team_2 + self.points_hand_team(1) + self.points_hand_team(2)
                if (self.stats['greatest_close'][1] < self.points_hand_team(1) + self.points_hand_team(2)):
                    self.stats['greatest_close'][1] = self.points_hand_team(1) + self.points_hand_team(2)
            self.stats['game_close'] += 1
            self.player_pass = 0
            self.hand_counter = self.hand_counter + 1
            self.gamelog.end_hand(self.points_team_1, self.points_team_2)
            return True
        else:
            return False
    def end_game(self):
        if int(self.points_team_1) > int(self.points) or int(self.points_team_2) > int(self.points):
            self.gamelog.end_game()
            return True
        else:
            return False
    def player_must_pass(self, player_id):
        for item in self.players_tiles[player_id]:
            if item[0] == self.left_tile or item[1] == self.left_tile or item[0] == self.right_tile \
                or item[1] == self.right_tile or self.left_tile == None:
                return False
        return True
    def can_i_put_this_tile_in_this_side(self, tile, side):
        "This function was created after Feria del Puerto de Santa Maria fair"
        if (side == 'left' and (tile[0] == self.left_tile or tile[1] == self.left_tile)) \
            or (side == 'right' and (tile[0] == self.right_tile or tile[1] == self.right_tile)):
            return True
        else:
            return False
    def ask_tile(self, player_pos, new_tile = None, side = None, mtime = 1):
        """ Ask a player for a tile """
        if new_tile == None or side == None:
            new_tile, side, mtime = self.players[player_pos].down_tile(self.left_tile, self.right_tile, copy.deepcopy(self.board), None, None)
        log.write("player %s puts %s tile in the %s" % (player_pos + 1, new_tile, side))
        self.gamelog.move(player_pos+1, new_tile, side, self.left_tile, self.right_tile, mtime)
        if new_tile != None or side != 'pass':
            self.player_pass = 0
            if len(self.board) == 0:
                """first move"""
                self.board.append(new_tile)
                self.left_tile = new_tile[0]
                self.right_tile = new_tile[1]
                self.first_tile = new_tile
            else:
                """other"""
                if side == 'left' and new_tile[0] == self.left_tile:
                    self.board.insert(0, new_tile[1] + new_tile[0])
                    self.left_tile = new_tile[1]
                elif side == 'left' and new_tile[1] == self.left_tile:
                    self.board.insert(0, new_tile)
                    self.left_tile = new_tile[0]
                elif side == 'right' and new_tile[0] == self.right_tile:
                    self.board.append(new_tile)
                    self.right_tile = new_tile[1]
                elif side == 'right' and new_tile[1] == self.right_tile:
                    self.board.append(new_tile[1] + new_tile[0])
                    self.right_tile = new_tile[0]
            return new_tile, side, mtime
        else:
            self.player_pass += 1
            log.write("player %s pass" % (player_pos + 1))
            self.stats['player_pass'][player_pos] += 1
            return "XX", "XX", 0
    def restart(self):
        self.points_team_1 = 0
        self.points_team_2 = 0
        
        self.left_tile = None
        self.right_tile = None
        
        # restart stats
        self.stats['player_pass'] = [0, 0, 0, 0]
        self.stats['player_win'] = [0, 0, 0, 0]
        self.stats['game_close'] = 0
        self.stats['greatest_close'] = [0, 0]