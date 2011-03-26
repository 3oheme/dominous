from pygame import *
from gloss import *
from dominoes_game import domino_game

from sound import *
from tools import *
from config import *

import log
import random

class ActivePlayer(Sprite):
    """@brief draws a light circle around current player tiles.
    
    Draws a blinking translucent circle around current player tiles.
    """ 
    def __init__(self):
        self.current_player = 4
        self.texture = Texture(tool.image("theme_gui", "active_player.png"))
        self.angle = 0
        self.scale = 1
        self.eggs = 0
        Sprite.__init__(self, self.texture, (-self.texture.width, -self.texture.width))
    def draw(self):
        if self.current_player is not 4:
            self.eggs += Gloss.elapsed_seconds * 0.5
            if self.eggs > 1:
                self.eggs = 0
        Sprite.draw(self, scale = self.scale, rotation = self.angle, color = Color(1,1,1,Gloss.smooth_step2(0.5, 1, self.eggs)))
    def update(self):
        pass
    def get_player(self):
        return self.current_player
    def player(self, pos):
        self.current_player = pos
        if self.current_player == 0:
            self.position = ((Gloss.screen_resolution[0]/2)-self.texture.half_width, Gloss.screen_resolution[1]-self.texture.height)
            self.angle = 0
        elif self.current_player == 1:
            self.position = (Gloss.screen_resolution[0]-self.texture.height, (Gloss.screen_resolution[1]/2)+self.texture.half_width)
            self.angle = 270
        elif self.current_player == 2:
            self.position = (Gloss.screen_resolution[0]/2+self.texture.half_width, self.texture.height)
            self.angle = 180
        elif self.current_player == 3:
            self.position = (self.texture.height, (Gloss.screen_resolution[1]/2)-self.texture.half_width)
            self.angle = 90
        else:
            self.current_player = 4

class NextPosition(Sprite):
    """@brief draws a circle in the board, so human player can know where to put the tile"""
    def __init__(self):
        self.texture = Texture(tool.image("theme_tile", 'tile_next.png'))
        self.position = (0, 0)
        self.angle = 0
        self.eggs = 0
        Sprite.__init__(self, self.texture, (-self.texture.width, -self.texture.width))
    def draw(self):
        self.eggs += Gloss.elapsed_seconds * 0.5
        if self.eggs > 1:
            self.eggs = 0
        Sprite.draw(self, origin = (self.texture.half_width, self.texture.half_height), scale = config['scale'], rotation = self.angle, color = Color(1,1,1,Gloss.smooth_step2(0.5, 1, self.eggs)))
    def goto(self, position = None, rotation = None):
        if position is None:
            position = self.position
        if rotation is None:
            rotation = self.angle
        self.position = position
        self.angle = rotation

class DebugInfo():
    """@brief prints debug info on screen"""
    def __init__(self):
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", int(config['scale']*40), False, False, 32, 255)
        self.text = ""
    def add(self, string):
        self.text = self.text + string + "\n"
    def show(self):
        self.font_main.draw(self.text, position = (Gloss.screen_resolution[0]-150, 10), color = Color(1, 1, 1, 1))
        self.text = ""

class Scoreboard():
    """@brief prints scoreboard ingame"""
    def __init__(self):
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", int(config['scale']*60), False, False, 32, 255)
        self.text1 = "Equipo 1 - 0"
        self.text2 = "Equipo 2 - 0"
        self.gap = Gloss.screen_resolution[0]/20
        self.textsize1 = self.font_main.measure_string(self.text1)
        self.textsize2 = self.font_main.measure_string(self.text2)
        self.position = (self.textsize1[0],Gloss.screen_resolution[1]-config['tile_width'])
    def draw(self):
        Gloss.draw_box(position = (self.position[0]+Gloss.screen_resolution[0]/8, self.position[1]-Gloss.screen_resolution[0]/16), width = Gloss.screen_resolution[0]/3, height = Gloss.screen_resolution[0]/3, rotation = 85, color = Color(0,0,0,0.6))
        self.font_main.draw(self.text1, position = (self.position[0]-(self.textsize1[0]/2), self.position[1]-(self.textsize1[1]/2)), color = Color(1, 1, 1, 1))
        self.font_main.draw(self.text2, position = (self.position[0]-(self.textsize2[0]/2), self.position[1]-(self.textsize2[1]/2)+self.textsize1[1]), color = Color(1, 1, 1, 1))
    def update_score(self, team1, team2):
        self.text1 = "Equipo 1 - %s" % team1
        self.text2 = "Equipo 2 - %s" % team2
        self.textsize1 = self.font_main.measure_string(self.text1)
        self.textsize2 = self.font_main.measure_string(self.text2)

class FullScoreboard():
    """@brief print a scoreboard after every hand and when finishing game"""
    def __init__(self):
        self.text_team1 = "Equipo 1"
        self.text_team2 = "Equipo 2"
        self.points_team1 = []
        self.points_team2 = []
        self.font_main = SpriteFont("fonts/handsean.ttf", 19, False, False, 32, 255)
        self.position = (Gloss.screen_resolution[0], Gloss.screen_resolution[1])
    def draw(self):
        Gloss.fill(top = Color(0,0,0,0.7), bottom = Color(0,0,0,9))
        output = self.text_team1 + "    " + self.text_team2 + "\n"
        #for item in self.points
        #TEMP
        self.points_team1 = [0, 12, 12, 12, 12, 65, 71, 91, 104, 112,  112, 112, 112, 165, 171, 191, 210]
        self.points_team2 = [0, 0,  32, 48, 81, 81, 81, 97, 100, 100,  132, 148, 181, 181, 181, 197, 230]
        count = 0
        for x in self.points_team1:
            #print "E1:" + str(self.points_team1[count]) + " - E2:" + str(self.points_team2[count])
            self.font_main.draw(str(self.points_team1[count]), position = (self.position[0],self.position[1]+(count*26)))
            self.font_main.draw(str(self.points_team2[count]), position = (self.position[0]+100,self.position[1]+(count*26)))))
            count += 1
    def update_score(self, team1, team2):
        self.points_team1.append(team1)
        self.points_team2.append(team2)
    def update(self):
        pass

class PassButton(Sprite):
    """@brief Button to pass your turn"""
    def __init__(self):
        self.text = "paso"
        self.texture_original = Texture(tool.image("theme_tile", 'tile_hidden.png'))
        Sprite.__init__(self, self.texture_original, (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]+config['tile_width']))
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", int(config['scale']*60), False, False, 32, 255)
        self.textsize = self.font_main.measure_string(self.text)
        self.opacity = 1
        self.from_pos = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]+config['tile_width'])
        self.goto_pos = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]+config['tile_width'])
        self.eggs = 0
    def draw(self):
        if self.goto_pos != self.position:
            self.eggs += Gloss.elapsed_seconds
            if self.eggs > 1.0:
                self.eggs = 1.0
            Sprite.move_to(self, Gloss.smooth_step(self.from_pos[0], self.goto_pos[0], self.eggs), Gloss.smooth_step(self.from_pos[1], self.goto_pos[1], self.eggs))
        Sprite.draw(self, origin = (self.texture.half_width, self.texture.half_height), scale = config['scale'], color = Color(1,1,1,self.opacity))
        self.font_main.draw(self.text, position = (self.position[0]-(self.textsize[0]/2), self.position[1]-(self.textsize[1]/2)), color = Color(1, 1, 1, 1))
    def set_hover(self):
        self.opacity = 0.7
    def remove_hover(self):
        self.opacity = 1
    def move_button(self, from_pos, goto_pos):
        self.eggs = 0
        self.from_pos = from_pos
        self.goto_pos = goto_pos
        self.eggs = 0
    def update(self):
        pass

class IngameMenu():
    """@brief shows an ingame menu"""
    def __init__(self):
        self.position = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.text1 = "continuar la partida"
        self.text2 = "volver al menu"
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", int(config['scale']*60), False, False, 32, 255)
        self.textsize1 = self.font_main.measure_string(self.text1)
        self.textsize2 = self.font_main.measure_string(self.text2)
        self.gap = self.textsize1[1]*2
    def draw(self):
        Gloss.fill(top = Color(0,0,0,0.7), bottom = Color(0,0,0,9))
        # Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(0,0,0,0.8))
        self.font_main.draw(self.text1, position = (self.position[0]-(self.textsize1[0]/2), self.position[1]-(self.textsize1[1]/2)), color = Color(1, 1, 1, 1))
        self.font_main.draw(self.text2, position = (self.position[0]-(self.textsize2[0]/2), self.position[1]+self.gap-(self.textsize2[1]/2)), color = Color(1, 1, 1, 1))
    def update(self):
        pass
    def click(self, pos):
        if (pos[0]>self.position[0]-self.textsize1[0]/2 and pos[0]<self.position[0]+self.textsize1[0]/2 and \
            pos[1]>self.position[1]-self.textsize1[1]/2 and pos[1]<self.position[1]+self.textsize1[1]/2):
            return 1
        elif (pos[0]>self.position[0]-self.textsize2[0]/2 and pos[0]<self.position[0]+self.textsize2[0]/2 and \
            pos[1]>self.position[1]+(self.textsize1[1]/2)+self.gap-(self.textsize2[1]) and pos[1]<self.position[1]+(self.textsize1[1]/2)+self.gap):
            return 2
        else:
            return 0

class Tile(Sprite):
    """@brief draws a unique tile in screen"""
    def __init__(self, tile):
        self.texture_original = Texture(tool.image("theme_tile", 'tile_' + tile + '.png'))
        self.texture_rev = Texture(tool.image("theme_tile", "tile_hidden.png"))
        self.tile = tile
        self.reversed = False
        self.from_pos = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.goto_pos = (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        self.eggs = 0
        self.angle = 0
        self.from_angle = 0
        self.goto_angle = 0
        self.draggable = False
        self.played_sound = False
        self.scale = config['scale']
        self.from_scale = config['scale']
        self.goto_scale = config['scale']
        self.speed = 1
        self.is_passing = False
        self.passing_status = 0
        self.play_sound = True
        Sprite.__init__(self, self.texture_original, (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2))
    def draw(self):
        Sprite.draw(self, origin = (self.texture.half_width, self.texture.half_height), scale = self.scale, rotation = self.angle)
    def update(self):
        if self.goto_pos != self.position or self.goto_angle != self.angle:
            self.eggs += Gloss.elapsed_seconds * self.speed
            if self.eggs > 0.8 and self.played_sound == False:
                if self.play_sound:
                    sound.tile()
                self.played_sound = True
            if self.eggs > 1.0:
                self.eggs = 1.0
            Sprite.move_to(self, Gloss.smooth_step(self.from_pos[0], self.goto_pos[0], self.eggs), Gloss.smooth_step(self.from_pos[1], self.goto_pos[1], self.eggs))
        if self.goto_angle != self.angle:
            self.angle = Gloss.smooth_step(self.from_angle, self.goto_angle, self.eggs)
        if self.is_passing:
            if self.passing_status == 1: #subiendo
                self.scale = Gloss.smooth_step(self.from_scale, self.goto_scale, self.eggs)
                self.eggs += Gloss.elapsed_seconds * self.speed * 2
                if abs(self.scale-self.goto_scale) < 0.01:
                    self.passing_status = 2
            elif self.passing_status == 2: #golpe
                self.eggs = 0
                self.from_scale = config['scale']
                self.goto_scale = config['scale'] * 1.2
                self.scale = config['scale']
                self.passing_status = 3
                sound.tile()
            elif self.passing_status == 3: #subiendo
                self.scale = Gloss.smooth_step(self.from_scale, self.goto_scale, self.eggs)
                self.eggs += Gloss.elapsed_seconds * self.speed * 5
                if abs(self.scale-self.goto_scale) < 0.01:
                    self.passing_status = 4
            elif self.passing_status == 4: #golpe
                self.eggs = 0
                self.from_scale = config['scale']
                self.goto_scale = config['scale']
                self.scale = config['scale']
                self.passing_status = 0
                self.is_passing = False
                sound.tile()
    def pass_effect(self):
        self.is_passing = True
        self.eggs = 0
        self.passing_status = 1
        """@brief make a pass effect, moving up and down the tile"""
        self.played_sound = False
        self.eggs = 0
        self.from_scale = config['scale']
        self.goto_scale = config['scale'] * 1.5
    def tile_is_passing(self):
        return self.is_passing
    def drag(self, position):
        """@brief place tile in its position, without moving"""
        self.from_pos = position
        self.goto_pos = position
        self.position = position
    def goto(self, position = None, rotation = None, speed = None, sound = True):
        """@brief move tile slowly to its position"""
        self.played_sound = False
        if position is None:
            position = self.position
        if rotation is None:
            rotation = self.angle
        if speed is None:
            self.speed = 1
        else:
            self.speed = speed
        self.eggs = 0
        self.from_pos = self.position
        self.from_angle = self.angle
        self.goto_pos = position
        self.goto_angle = rotation
        self.play_sound = sound
    def stopped(self):
        if self.goto_pos == self.position and self.goto_angle == self.angle and self.scale == self.from_scale:
            return True
        else:
            return False
    def reverse(self):
        """@brief flip tile"""
        if self.reversed:
            self.texture = self.texture_original
            self.reversed = False
        else:
            self.texture = self.texture_rev
            self.reversed = True

def load_tiles(domino):
    sprites = {}
    for tile in domino.tiles:
        sprite = Tile(tile)
        sprite.id = tile
        sprites[tile] = sprite
    x = float(config['window_width'] * config['window_height'])
    y = sprites["00"].texture.width * sprites["00"].texture.height
    config['scale'] = round( (((x / y ) * 0.0075) + 0.12), 2)
    for tile in domino.tiles:
        sprites[tile].scale = config['scale']
        sprites[tile].from_scale = config['scale']
        sprites[tile].goto_scale = config['scale']
    config['tile_width'] = int(config['scale']* sprites["00"].texture.width)
    config['tile_height'] = int(config['scale']* sprites["00"].texture.height)
    return sprites

def stopped(tiles):
    moving = False
    for key, tile in tiles.iteritems():
        moving = moving or tile.stopped()
    return moving

def draw_tiles(tiles):
    for key, tile in tiles.iteritems():
        tile.draw()

def cleant(tile):
    if tile[0] > tile[1]:
        tile = tile[1] + tile[0]
    return tile

class Engine:
    """
    This is a finite-state machine managing main game loop. Iterates around following graph

    Status = 0 - game start, reset all, create players
        1 - fade in
        2 - deal tiles
        if game is over:
            999 - end game, goto menu
        if hand is over:
            99 - end hand
            100 - move tiles to center
            101 - show full screen scoreboard
            goto 1
        else:
            3 - draw available positions
            4 - ask tile next player
            if next player is human:
                if player must pass:
                    20 - human player must pass
                    21 - waiting to click pass button
                    22 - human pressed pass button
                    23 - pass effect
                    goto 5
                else:
                    6 - start drag n drop player tile
                    7 - dragging tile
                    8 - mousedown released
                    if player can place tile here:
                        goto 5
                    else:
                        goto 6
            else:
                if computer must pass:
                    23 - pass effect
                else:
                    5 - move tile to its place
                goto 3

    @brief main engine class
    """
    def __init__(self, mainp):
        self.game = mainp
        self.domino = domino_game()
        self.background = Texture(tool.image("theme_bg", "background.png"))
        self.button_menu = Texture(tool.image("system", "home.png"))
        self.tiles = load_tiles(self.domino)
        self.active_player = ActivePlayer()
        self.next_left = NextPosition()
        self.next_right = NextPosition()
        self.passbutton = PassButton()
        self.scoreboard = Scoreboard()
        self.fullscoreboard = FullScoreboard()
        self.ingame_menu = IngameMenu()
        self.debug = DebugInfo()
        self.fadein_amount = 0
        self.once = True
        self.new_tile = ""
        self.side = ""
        self.counter = 0
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 12, False, False, 32, 255)
        self.right_dir = "right"
        self.left_dir = "left"
        self.dragging = False
        self.dragging_tile = "XX"
        self.status = 0
        self.tiles_temp = []
        self.timer_temp = 0
        self.game.on_mouse_down = self.mouse_down
        self.game.on_mouse_up = self.mouse_up
        self.game.on_mouse_motion = self.mouse_motion
        self.game.on_key_down = self.key_pressed
    def draw(self):
        Gloss.fill(self.background)
        self.button_menu.draw((35, 35))
        # Status = 0 - game start, reset all, create players
        if self.status == 0:
            pass
        # Status = 1 - fade in
        elif self.status == 1:
            draw_tiles(self.tiles)
            next = Gloss.lerp(1, 0, self.fadein_amount)
            Gloss.draw_box((0,0), Gloss.screen_resolution[0], Gloss.screen_resolution[1], color = Color(1,1,1,next))
            self.fadein_amount += Gloss.elapsed_seconds * 5
            if next == 0:
                self.status = 2
        # Status = 2 - deal tiles
        elif self.status == 2:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 3 - draw available positions
        elif self.status == 3:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 4 - ask tile next player
        elif self.status == 4:
            self.active_player.draw()
            self.scoreboard.draw()
            self.passbutton.draw()
            draw_tiles(self.tiles)
        # Status = 5 - move tile to its place
        elif self.status == 5:
            self.active_player.draw()
            self.scoreboard.draw()
            self.passbutton.draw()
            draw_tiles(self.tiles)
        # Status = 6 - drag n drop player tile
        elif self.status == 6:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 7 - dragging tile self.dragging_tile
        elif self.status == 7:
            self.active_player.draw()
            self.scoreboard.draw()
            #self.next_left.draw()
            #self.next_right.draw()
            draw_tiles(self.tiles)
            self.tiles[self.dragging_tile].draw()
        # Status = 8 - released mouse down
        elif self.status == 8:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 20 - human player must pass
        elif self.status == 20:
            self.active_player.draw()
            self.scoreboard.draw()
            self.passbutton.draw()
            draw_tiles(self.tiles)
        # Status = 21 - waiting to click pass button
        elif self.status == 21:
            self.active_player.draw()
            self.scoreboard.draw()
            self.passbutton.draw()
            draw_tiles(self.tiles)
        # Status = 22 - passing effect
        elif self.status == 22:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 23 - passing effect
        elif self.status == 23:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 24 - passing effect
        elif self.status == 24:
            self.active_player.draw()
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 100 - move tiles to center
        elif self.status == 100:
            self.scoreboard.draw()
            draw_tiles(self.tiles)
        # Status = 101 - move tiles to center
        elif self.status == 101:
            self.scoreboard.draw()
            draw_tiles(self.tiles)
            self.fullscoreboard.draw()
        # Status = 500 - ingame menu
        elif self.status == 500:
            self.scoreboard.draw()
            draw_tiles(self.tiles)
            #TEMP
            #self.ingame_menu.draw()
            self.fullscoreboard.draw()
        # draw info on screen
        self.debug.add('Status = %s' % str(self.status))
        if Gloss.running_slowly:
            self.debug.add('Gloss.running_slowly')
        self.debug.add('elapsed_seconds = %s' % str(Gloss.elapsed_seconds))
        self.debug.add('scoreboard (%s, %s)' % (str(self.domino.points_team1()), str(self.domino.points_team2())))
        self.debug.show()

    def update(self):
        for key, tile in self.tiles.iteritems():
            tile.update()
        self.passbutton.update()
        # Status = 0 - game start, reset all, create players
        if self.status == 0:
            if config['gametype'] == 'human':
                self.domino.create_players("h",config['player2'],config['player3'],config['player4'])
            elif config['gametype'] == 'computer':
                self.domino.create_players(config['player1'],config['player2'],config['player3'],config['player4'])
            self.status = 1
        # Status = 1 - fade in
        elif self.status == 1:
            pass
        # Status = 2 - deal tiles
        elif self.status == 2:
            # execute only once
            if self.once:
                self.domino.deal_tiles()
                self.place_player_tiles(0)
                self.place_player_tiles(1)
                self.place_player_tiles(2)
                self.place_player_tiles(3)
                if self.domino.player_type[0] == "h":
                    self.side_up_player_tiles(0)
                else:
                    self.side_down_player_tiles(0)
                if self.domino.player_type[1] == "h":
                    self.side_up_player_tiles(1)
                else:
                    self.side_down_player_tiles(1)
                if self.domino.player_type[2] == "h":
                    self.side_up_player_tiles(2)
                else:
                    self.side_down_player_tiles(2)
                if self.domino.player_type[3] == "h":
                    self.side_up_player_tiles(3)
                else:
                    self.side_down_player_tiles(3)
                self.once = False
            if stopped(self.tiles):
                self.status = 3
            if self.domino.end_game():
                self.status = 999
        # Status = 3 - draw available positions
        elif self.status == 3:
            print "status = 3"
            if self.domino.end_hand():
                print "end.hand"
                self.status = 99
            elif self.domino.end_game():
                print "end.game"
                self.status = 999
            else:
                self.status = 4
        # Status = 4 - ask tile next player
        elif self.status == 4:
            nextplayer = self.domino.nextplayer()
            if self.domino.player_type[nextplayer] == "h":
                if self.domino.player_must_pass(nextplayer):
                    self.status = 20
                else:
                    self.status = 6
                self.active_player.player(0)
            else:
                self.new_tile, self.side = self.domino.ask_tile(nextplayer)
                self.active_player.player(self.domino.currentplayer())
                # draw board
                print " "
                self.domino.print_hand()
                print " "
                # move tile to its position
                if self.new_tile != "XX":
                    self.tiles[self.new_tile].reverse()
                    self.place_next_player_tile()
                    self.place_player_tiles(self.domino.currentplayer())
                    self.status = 5
                else:
                    self.status = 23
        # Status = 5 - move tile to its place
        elif self.status == 5:
            if self.new_tile == "XX" or self.tiles[self.new_tile].stopped():
                self.status = 3
        # Status = 6 - start drag n drop player tile
        elif self.status == 6:
            pass
        # Status = 7 - dragging tile
        elif self.status == 7:
            left_pos = self.next_tile_position(self.tiles[self.dragging_tile], "left")
            right_pos = self.next_tile_position(self.tiles[self.dragging_tile], "right")
            self.next_left.goto(left_pos)
            #self.next_left.goto((200, 300), 90)
            self.next_right.goto(right_pos)
            #self.next_right.goto((300, 400), 0)
            mousepos = mouse.get_pos()
            self.tiles[self.dragging_tile].drag(mousepos)
        # Status = 8 - mousedown released - can player place tile here?
        elif self.status == 8:
            self.new_tile = self.dragging_tile
            radius = config['tile_width'] * 130
            if len(self.domino.board) == 0:
                # first tile in board
                self.side = "left"
                self.domino.players_tiles[0].remove(self.new_tile)
                self.new_tile, self.side = self.domino.ask_tile(self.domino.currentplayer(), self.new_tile, self.side)
                self.place_next_player_tile()
                self.place_player_tiles(self.domino.currentplayer())
                self.status = 5
            else:
                if len(self.domino.board) == 1:
                    centerpos = self.tiles[cleant(self.domino.board[0])].position
                    if (Point.distance_squared(self.tiles[self.dragging_tile].position, (centerpos[0]-(config['tile_width']), centerpos[1])) < radius):
                        self.side = "left"
                    elif (Point.distance_squared(self.tiles[self.dragging_tile].position, (centerpos[0]+(config['tile_width']), centerpos[1])) < radius):
                        self.side = "right"
                    else:
                        self.side = "null"
                else:
                    if (Point.distance_squared(self.tiles[self.dragging_tile].position, self.tiles[cleant(self.domino.board[0])].position) < radius):
                        self.side = "left"
                    elif (Point.distance_squared(self.tiles[self.dragging_tile].position, self.tiles[cleant(self.domino.board[-1])].position) < radius):
                        self.side = "right"
                    else:
                        self.side = "null"
                if self.side != "null":
                    if self.domino.can_i_put_this_tile_in_this_side(self.new_tile, self.side):
                        self.domino.players_tiles[0].remove(self.new_tile)
                        self.new_tile, self.side = self.domino.ask_tile(self.domino.currentplayer(), self.new_tile, self.side)
                        self.place_next_player_tile()
                        self.place_player_tiles(self.domino.currentplayer())
                        self.status = 5
                    else:
                        self.place_player_tiles(self.domino.currentplayer())
                        self.status = 6
                else:
                    self.place_player_tiles(self.domino.currentplayer())
                    self.status = 6
        # Status = 20 - human player must pass
        elif self.status == 20:
            gap = config['tile_height'] / 4
            all_tiles_width = (len(self.domino.players_tiles[0]) * config['tile_height']) + ((len(self.domino.players_tiles[0])-1)*gap)
            origin = (Gloss.screen_resolution[0]/2 + (all_tiles_width/2+1) + (config['tile_width']/2), Gloss.screen_resolution[1] + (config['tile_width']))
            destination = (Gloss.screen_resolution[0]/2 + (all_tiles_width/2+1) + (config['tile_width']/2), Gloss.screen_resolution[1] - gap - (config['tile_width']/2))
            self.passbutton.move_button(origin, destination)
            self.status = 21
        # Status = 21 - waiting to press pass button
        elif self.status == 21:
            pass
        # Status = 22 - human pressed pass button
        elif self.status == 22:
            gap = config['tile_height'] / 4
            all_tiles_width = (len(self.domino.players_tiles[0]) * config['tile_height']) + ((len(self.domino.players_tiles[0])-1)*gap)
            origin = (Gloss.screen_resolution[0]/2 + (all_tiles_width/2+1) + (config['tile_width']/2), Gloss.screen_resolution[1] - gap - (config['tile_width']/2))
            destination = (Gloss.screen_resolution[0]/2 + (all_tiles_width/2+1) + (config['tile_width']/2), Gloss.screen_resolution[1] + (config['tile_width']))
            self.passbutton.move_button(origin, destination)
            self.status = 23
        # Status = 23 - start pass effect
        elif self.status == 23:
            self.tiles[self.domino.players_tiles[self.domino.currentplayer()][-1]].pass_effect()
            # FIXME
            """del self.tiles_temp[:]
            self.tiles_temp = self.domino.players_tiles[currentplayer][:]
            self.timer_temp = Gloss.total_seconds"""
            self.status = 24 
        # Status = 24 - passing effect
        elif self.status == 24: 
            """if len(self.tiles_temp):
                if self.timer_temp < Gloss.total_seconds:
                    newtile = self.tiles_temp.pop()
                    self.tiles[newtile].pass_effect()
                    self.timer_temp += 0.2
            else:
                self.status = 3
                del self.tiles_temp[:]
                self.timer_temp = 0"""
            if self.tiles[self.domino.players_tiles[self.domino.currentplayer()][-1]].tile_is_passing() == False:
                self.status = 3
        # Status = 99 - end hand
        elif self.status == 99:
            print "end hand - status 99"
            self.status = 100
            self.once = True
            self.right_dir = "right"
            self.left_dir = "left"
            for key, tile in self.tiles.iteritems():
                self.tiles[key].goto((Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2), 0)
                if not self.tiles[key].reversed:
                    self.tiles[key].reverse()
            self.scoreboard.update_score(str(self.domino.points_team1()), str(self.domino.points_team2()))
            self.fullscoreboard.update_score(str(self.domino.points_team1()), str(self.domino.points_team2()))
        # Status = 100 - move tiles to center
        elif self.status == 100:
            if self.tiles['00'].stopped():
                self.status = 101
        # Status = 101 - move tiles to center
        elif self.status == 101:
            pass
        # Status = 500 - show ingame menu
        elif self.status == 500:
            pass
        # Status = 999 - end game, goto menu
        elif self.status == 999:
            self.game.goto_intro()
    def next_left_tile_position(self):
        if len(self.domino.board) == 0:
            return (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        elif len(self.domino.board) == 1:
            return ((Gloss.screen_resolution[0]/2)-config['tile_width'], Gloss.screen_resolution[1]/2)
        else:
            return self.tiles[cleant(self.domino.board[0])].position
    def next_right_tile_position(self):
        if len(self.domino.board) == 0:
            return (Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2)
        elif len(self.domino.board) == 1:
            return ((Gloss.screen_resolution[0]/2)+config['tile_width'], Gloss.screen_resolution[1]/2)
        else:   
            return self.tiles[cleant(self.domino.board[-1])].position
    def start(self):
        pass
    def stop(self):
        pass
    def tile_clicked(self, pos):
        for key, tile in self.tiles.iteritems():
            if pos[0] < (self.tiles[key].position[0]+(config['tile_height']/2)) and \
                pos[0] > (self.tiles[key].position[0]-(config['tile_height']/2)) and \
                pos[1] < (self.tiles[key].position[1]+(config['tile_width']/2)) and \
                pos[1] > (self.tiles[key].position[1]-(config['tile_width']/2)):
                return key
        return None
        
    def mouse_down(self, event):
        # start drag n drop
        if self.status == 6:
            tile = self.tile_clicked(event.pos)
            if tile != None and tile in self.domino.players_tiles[0]:
                self.dragging = True
                self.dragging_tile = tile
                self.status = 7
        # pass button
        elif self.status == 21:
            if self.mouse_on_button_pass():
                self.status = 22
        # fullscreen scoreboard
        elif self.status == 101:
            self.status = 2
        # ingame menu
        if self.status != 500 and self.status != 0 and self.status != 101 and event.pos[0] > 35 and event.pos[1] > 35 and event.pos[0] < 112 and event.pos[1] < 58:
            self.status_backup = self.status
            self.status = 500
        elif self.status == 500:
            option = self.ingame_menu.click(event.pos)
            if option == 2:
                self.game.goto_intro()
            else:
                self.status = self.status_backup
    def key_pressed(self, event):
        # show ingame menu
        if event.key == K_ESCAPE and self.status != 500 and self.status != 101:
            self.status_backup = self.status
            self.status = 500
        elif event.key == K_ESCAPE:
            self.status = self.status_backup
        elif event.key == K_r:
            # cheat mode :-D
            for key, tile in self.tiles.iteritems():
                if self.tiles[key].reversed:
                    self.tiles[key].reverse()
    def mouse_motion(self, event):
        if self.status == 21:
            if self.mouse_on_button_pass():
                self.passbutton.set_hover()
            else:
                self.passbutton.remove_hover()
    def mouse_up(self, event):
        if self.status == 7:
            self.status = 8
    def mouse_on_button_pass(self):
        mousepos = mouse.get_pos()
        buttonpos_x = self.passbutton.position[0] - (config['tile_width']/2)
        buttonpos_y = self.passbutton.position[1] - (config['tile_height']/2)
        if mousepos[0] > buttonpos_x and mousepos[0] < buttonpos_x + config['tile_width'] and \
            mousepos[1] > buttonpos_y and mousepos[1] < buttonpos_y + config['tile_height']:
            return True
        else:
            return False
    def next_tile_position(self, tile, side = "left"):
        """@brief given a certain tile, it return next position
        @param tile tile we want to place
        @param side left or right side
        @returns array with [0] => position in (x,y) format and [1] => angle
        """
        # FIXME
        return ((400, 400))
        # place first tile in board
        if len(self.domino.board) == 0:
            return [(Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2), 90]
            
        else:
            if len(self.domino.board) == 1:
                if self.side == "right":
                    prev_tile = self.domino.board[-1]
                else:
                    prev_tile = self.domino.board[0]
            else:
                if self.side == "right":
                    prev_tile = self.domino.board[-2]
                else:
                    prev_tile = self.domino.board[1]
            right_change_dir = False
            left_change_dir = False
            # is there room to place the tile? if not, we must change direction
            if self.side is 'right':
                direction = self.right_dir
            else:
                direction = self.left_dir
            gap = config['tile_width']*3
            if direction is 'right' and self.tiles[prev_tile].position[0] > (Gloss.screen_resolution[0]-gap):
                if self.side is 'right':
                    self_right_dir = "up"
                    right_change_dir = True
                else:
                    self_left_dir = "up"
                    left_change_dir = True
            elif direction is 'up' and self.tiles[prev_tile].position[1] < gap:
                if self.side is 'right':
                    self_right_dir = "left"
                    right_change_dir = True
                else:
                    self_left_dir = "left"
                    left_change_dir = True
            elif direction is 'left' and self.tiles[prev_tile].position[0] < gap:
                if self.side is 'right':
                    self_right_dir = "down"
                    right_change_dir = True
                else:
                    self_left_dir = "down"
                    left_change_dir = True
            elif direction is 'down' and self.tiles[prev_tile].position[1] > (Gloss.screen_resolution[1]-gap):
                if self.side is 'right':
                    self_right_dir = "right"
                    right_change_dir = True
                else:
                    self_left_dir = "right"
                    left_change_dir = True
            if self.side is 'right':
                direction = self_right_dir
            else:
                direction = self_left_dir
            # now place tile
            if direction is "right":
                if self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270:
                    inc_x = config['tile_width']/2 + config['tile_height']/2
                    inc_y = 0
                    new_angle = 0
                elif (self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = config['tile_width']
                    inc_y = 0
                    new_angle = 0
                else:
                    inc_x = config['tile_width']/2 + config['tile_height']/2
                    inc_y = 0
                    new_angle = 90
            elif direction is "up":
                if self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    new_angle = 90
                elif (self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = 0
                    inc_y = config['tile_width'] * (-1)
                    new_angle = 90
                else:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    new_angle = 0
            elif direction is "left":
                if self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270:
                    inc_x = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    inc_y = 0
                    new_angle = 0
                elif (self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = config['tile_width'] * (-1)
                    inc_y = 0
                    new_angle = 0
                else:
                    inc_x = (config['tile_width']/2 + config['tile_height']/2) *(-1)
                    inc_y = 0
                    new_angle = 90
            elif direction is "down":
                if self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2)
                    new_angle = 90
                elif (self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = 0
                    inc_y = config['tile_width']
                    new_angle = 90
                else:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2)
                    new_angle = 0
            
            return [(self.tiles[prev_tile].position[0] + inc_x, self.tiles[prev_tile].position[1] + inc_y), new_angle]

    def place_next_player_tile(self):
        """ useful vars:
                self.new_tile = tile to put in board
                self.side = side to place self.new_tile in board
                self.right_dir = direction where right board side is growing to
                self.left_dir = direction where left board side is growing to
        """
        # place first tile in board
        if self.domino.first_tile == self.new_tile:
            if self.new_tile[0] == self.new_tile[1]:
                new_angle = 90
            else:
                new_angle = 0
            self.tiles[self.new_tile].goto((Gloss.screen_resolution[0]/2, Gloss.screen_resolution[1]/2), new_angle)
        # in other case...
        else:
            if self.side == "right":
                prev_tile = self.domino.board[-2]
            else:
                prev_tile = self.domino.board[1]
            if prev_tile[0] > prev_tile[1]:
                prev_tile = prev_tile[1] + prev_tile[0] 
            right_change_dir = False
            left_change_dir = False
            # is there room to place the tile? if not, we must change direction
            if self.side is 'right':
                direction = self.right_dir
            else:
                direction = self.left_dir
            gap = config['tile_width']*3
            if direction is 'right' and self.tiles[prev_tile].position[0] > (Gloss.screen_resolution[0]-gap):
                if self.side is 'right':
                    self.right_dir = "up"
                    right_change_dir = True
                else:
                    self.left_dir = "up"
                    left_change_dir = True
            elif direction is 'up' and self.tiles[prev_tile].position[1] < gap:
                if self.side is 'right':
                    self.right_dir = "left"
                    right_change_dir = True
                else:
                    self.left_dir = "left"
                    left_change_dir = True
            elif direction is 'left' and self.tiles[prev_tile].position[0] < gap:
                if self.side is 'right':
                    self.right_dir = "down"
                    right_change_dir = True
                else:
                    self.left_dir = "down"
                    left_change_dir = True
            elif direction is 'down' and self.tiles[prev_tile].position[1] > (Gloss.screen_resolution[1]-gap):
                if self.side is 'right':
                    self.right_dir = "right"
                    right_change_dir = True
                else:
                    self.left_dir = "right"
                    left_change_dir = True
            if self.side is 'right':
                direction = self.right_dir
            else:
                direction = self.left_dir
            # now place tile
            if direction is "right":
                if self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270:
                    inc_x = config['tile_width']/2 + config['tile_height']/2
                    inc_y = 0
                    new_angle = 0
                elif (self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = config['tile_width']
                    inc_y = 0
                    new_angle = 0
                else:
                    inc_x = config['tile_width']/2 + config['tile_height']/2
                    inc_y = 0
                    new_angle = 90
            elif direction is "up":
                if self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    new_angle = 90
                elif (self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = 0
                    inc_y = config['tile_width'] * (-1)
                    new_angle = 90
                else:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    new_angle = 0
            elif direction is "left":
                if self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270:
                    inc_x = (config['tile_width']/2 + config['tile_height']/2) * (-1)
                    inc_y = 0
                    new_angle = 0
                elif (self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = config['tile_width'] * (-1)
                    inc_y = 0
                    new_angle = 0
                else:
                    inc_x = (config['tile_width']/2 + config['tile_height']/2) *(-1)
                    inc_y = 0
                    new_angle = 90
            elif direction is "down":
                if self.tiles[prev_tile].angle == 0 or self.tiles[prev_tile].angle == 180:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2)
                    new_angle = 90
                elif (self.tiles[prev_tile].angle == 90 or self.tiles[prev_tile].angle == 270) and self.new_tile[0] != self.new_tile[1]:
                    inc_x = 0
                    inc_y = config['tile_width']
                    new_angle = 90
                else:
                    inc_x = 0
                    inc_y = (config['tile_width']/2 + config['tile_height']/2)
                    new_angle = 0
            # reverse tile
            if self.side == "left":
                if (direction == "left" or direction == "up") and self.domino.board[0] != self.new_tile:
                    new_angle += 180
                elif (direction == "down" or direction == "right") and self.domino.board[0] == self.new_tile:
                    new_angle += 180
            elif self.side == "right":
                if (direction == "right" or direction == "down") and self.domino.board[-1] != self.new_tile:
                    new_angle += 180
                elif (direction == "up" or direction == "left") and self.domino.board[-1] == self.new_tile:
                    new_angle += 180
            
            self.tiles[self.new_tile].goto((self.tiles[prev_tile].position[0] + inc_x, self.tiles[prev_tile].position[1] + inc_y), new_angle) 

    def side_down_player_tiles(self, player):
        for tile in self.domino.players_tiles[player]:
            if not self.tiles[tile].reversed:
                self.tiles[tile].reverse()
    def side_up_player_tiles(self, player):
        for tile in self.domino.players_tiles[player]:
            if self.tiles[tile].reversed:
                self.tiles[tile].reverse()

    def place_player_tiles(self, player):
        # place player tiles
        gap = config['tile_height'] / 4
        all_tiles_width = (len(self.domino.players_tiles[player]) * config['tile_height']) + ((len(self.domino.players_tiles[player])-1)*gap)
        if player == 0:
            first_x = Gloss.screen_resolution[0]/2 - all_tiles_width/2
            first_y = Gloss.screen_resolution[1] - gap - (config['tile_width']/2)
            for tile in self.domino.players_tiles[0]:
                self.tiles[tile].goto((first_x, first_y), 90, sound = False)
                first_x += gap + config['tile_height']
        elif player == 1:
            first_x = (Gloss.screen_resolution[0] - gap) - config['tile_width']/2
            first_y = Gloss.screen_resolution[1]/2 - all_tiles_width/2
            for tile in self.domino.players_tiles[1]:
                if self.status == 2:
                    self.tiles[tile].goto((first_x, first_y), 180, sound = True)
                else:
                    self.tiles[tile].goto((first_x, first_y), 180, sound = False)
                first_y += gap + config['tile_height']
        elif player == 2:
            first_x = Gloss.screen_resolution[0]/2 - all_tiles_width/2
            first_y = gap + config['tile_width']/2
            for tile in self.domino.players_tiles[2]:
                self.tiles[tile].goto((first_x, first_y), 90, sound = False)
                first_x += gap + config['tile_height']
        elif player == 3:
            first_x = gap + config['tile_width']/2
            first_y = Gloss.screen_resolution[1]/2 - all_tiles_width/2
            for tile in self.domino.players_tiles[3]:
                self.tiles[tile].goto((first_x, first_y), 0.5, sound = False)
                first_y += gap + config['tile_height']

