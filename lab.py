from pygame import *
from gloss import *
from dominoes_game import domino_game

from sound import *
from tools import *
from config import *
from selectplayers import *

class Lab:
    def __init__(self, mainp):
        self.game = mainp
        self.domino = domino_game()
        self.game.on_mouse_down = self.mouse_down
        self.background = Texture(tool.image("system", "lab_bg.png"))
        self.status = 0
        self.status_backup = 0
        self.matches = 100
        self.current_match = 0
        self.team1_matches = 0
        self.team2_matches = 0
        
        self.graph = {
            'position' : (25,325),
            'points1' : [(0, 0)],
            'points2' : [(0, 0)],
        }
        
        self.po1_from = 375
        self.po1_cur = 375
        self.po1_to = 375
        self.po1_eggs = 0
        self.po2_from = 375
        self.po2_cur = 37
        self.po2_to = 375
        self.po2_eggs = 0
        
        self.pause_eggs = 0
        
        self.pause = Texture(tool.image("system", "pause.png"))
        self.restart = Texture(tool.image("system", "restart.png"))
        self.exit = Texture(tool.image("system", "exit.png"))
        
        self.font_main = SpriteFont("fonts/Comfortaa Regular.ttf", 24, False, False, 32, 255)
        self.font_small = SpriteFont("fonts/Comfortaa Regular.ttf", 16, False, False, 32, 255)
        
        self.num_tex = Texture(tool.image("system", "plus_one.png"))
        self.num_up = []
        
        self.stats = {
            'player_pass' : [0, 0, 0, 0],
            'player_win' : [0, 0, 0, 0],
            'game_close' : 0,
            'hands_played' : 0,
            'greatest_close' : [0, 0]
        }
            
        # temp - media y maxima de manos hasta terminar una partida
        self.t_num = [0]
        
    def draw(self):
        #str(self.domino.points_team1())
        #self.team1_matches
        Gloss.fill(self.background)

        self.p1.draw((25,  25))
        self.p3.draw((185, 25))
        self.p2.draw((465, 25))
        self.p4.draw((625, 25))

        if self.current_match != 0:
            po1_new = 375+((self.team1_matches-self.team2_matches)*3.75)
            po1_new2 = 750*self.team1_matches/(self.team1_matches+self.team2_matches)
            po1_new = po1_new2/2 + po1_new/2
            po2_new = 750-po1_new
        else:
            po1_new = 375
            po2_new = 375
        
        if po1_new != self.po1_to:
            self.po1_to = po1_new
            self.po1_from = self.po1_cur
            self.po1_eggs = 0
            self.po2_to = po2_new
            self.po2_from = self.po2_cur
            self.po2_eggs = 0
        
        self.po1_eggs += Gloss.elapsed_seconds * 2
        self.po2_eggs += Gloss.elapsed_seconds * 2
        self.po1_cur = Gloss.smooth_step(self.po1_from, self.po1_to, self.po1_eggs)
        self.po2_cur = Gloss.smooth_step(self.po2_from, self.po2_to, self.po2_eggs)
        
        Gloss.draw_box((25, 200), self.po1_cur, 50, 0.0, (0, 0), 1, Color.from_html("#f9b00c"))
        Gloss.draw_box((25, 200), self.po1_cur, 10, 0.0, (0, 0), 1, Color.from_html("#febf1a"))
        Gloss.draw_box((775-self.po2_cur, 200), self.po2_cur, 50, 0.0, (0, 0), 1, Color.from_html("#cccccc"))
        Gloss.draw_box((775-self.po2_cur, 200), self.po2_cur, 10, 0.0, (0, 0), 1, Color.from_html("#e0e0e0"))

        # los puntos de cada partida van de 0 a 200
        Gloss.draw_box((25, 275), (self.domino.points_team1()*375)/200, 25, 0.0, (0, 0), 1, Color.from_html("#f9b00c"))
        Gloss.draw_box((775, 275), (self.domino.points_team2()*375)/200, 25, 0.0, ((self.domino.points_team2()*375)/200, 0), 1, Color.from_html("#cccccc"))

        # pintamos las partidas ganadas encima de la barra
        text2_size = self.font_main.measure_string(str(self.team2_matches))
        self.font_main.draw(str(self.team1_matches), position = (35, 220), color = Color.WHITE)
        self.font_main.draw(str(self.team2_matches), position = (765-text2_size[0], 220), color = Color.WHITE)
        
        self.print_graph()
        
        # pintamos los botones
        if self.status == 99:
            self.pause_eggs += Gloss.elapsed_seconds
            if self.pause_eggs > 1:
                self.pause_eggs = 0
            self.pause.draw(position = (25, 532), color = Color(1,1,1,Gloss.smooth_step2(0.5, 1, self.pause_eggs)))
        else:
            self.pause.draw(position = (25, 532))
        self.restart.draw(position = (426, 532))
        self.exit.draw(position = (638, 532))
        
        # pintamos los numeros de +1
        for number in self.num_up:
            number.draw(color = Color(1,1,1,Gloss.smooth_step(1, 0, number.movetime)))
    
        # partida terminada
        if self.status == 999:
            if self.team1_matches > self.team2_matches:
                Gloss.draw_box((465, 25), 150, 150, 0, (0,0), 1, Color(1, 1, 1, 0.8))
                Gloss.draw_box((625, 25), 150, 150, 0, (0,0), 1, Color(1, 1, 1, 0.8))
            elif self.team1_matches < self.team2_matches:
                Gloss.draw_box((25, 25), 150, 150, 0, (0,0), 1, Color(1, 1, 1, 0.8))
                Gloss.draw_box((185, 25), 150, 150, 0, (0,0), 1, Color(1, 1, 1, 0.8))
        
    def print_graph(self):
        mod_points1 = []
        mod_points2 = []
        for point in self.graph['points1']:
            mod_points1.append((point[0]+self.graph['position'][0], 181-((point[1]*181)/self.matches)+self.graph['position'][1]))
        for point in self.graph['points2']:
            mod_points2.append((point[0]+self.graph['position'][0], 181-((point[1]*181)/self.matches)+self.graph['position'][1]))
        
        #pintamos las letras de equipo ganador si alguien pasa de las 50 victorias
        if self.team1_matches >= self.matches/2:
            for point in mod_points1:
                if point[1] == 416 or int(point[1]) < 416:
                    self.font_small.draw("Ganador equipo 1", position = (point[0]-139, 398), color = Color.from_html("#f9b00c"))
                    break
        elif self.team2_matches >= self.matches/2:
            for point in mod_points2:
                if point[1] <= 416:
                    self.font_small.draw("Ganador equipo 2", position = (point[0]-139, 398), color = Color.from_html("#cccccc"))
                    break
        
        # lineas de la grafica
        Gloss.draw_line((25, 507), (775, 507), color = Color.from_html("#d2d2d2"), width = 2.0)
        Gloss.draw_line((25, 507), (25, 325), color = Color.from_html("#d2d2d2"), width = 2.0)
        
        # algunas lineas de referencia
        Gloss.draw_line((25, 416), (775, 416), color = Color.from_html("#d2d2d2"), width = 1.0)
        
        Gloss.draw_line((400, 495), (400, 519), color = Color.from_html("#d2d2d2"), width = 1.0)
        Gloss.draw_line((212, 495), (212, 519), color = Color.from_html("#d2d2d2"), width = 1.0)
        Gloss.draw_line((612, 495), (612, 519), color = Color.from_html("#d2d2d2"), width = 1.0)
        
        Gloss.draw_lines(mod_points1, color = Color.from_html("#f9b00c"), width = 3.0)
        Gloss.draw_lines(mod_points2, color = Color.from_html("#cccccc"), width = 3.0)
        
    def update(self):
        for number in self.num_up:
            number.movetime += Gloss.elapsed_seconds
            if (number.movetime > 1.0): self.num_up.remove(number)
            number.move_to(None, Gloss.lerp(200, 180, number.movetime))
        if self.status == 0:
            pass
        elif self.status == 1:
            # comprobamos si hemos terminado todas las partidas
            if not self.current_match == self.matches:
                self.status = 2
            else:
                self.status = 999
        elif self.status == 2:
            # comprobamos si hemos terminado la partida actual
            if not self.domino.end_game():
                self.status = 3
                self.domino.deal_tiles()
            else:
                #temp manos por partida
                self.t_num.append(0)

                self.current_match += 1
                #print self.current_match
                if self.domino.points_team1() > self.domino.points_team2(): 
                    self.team1_matches += 1
                    newnumber = Sprite(self.num_tex, (30, 200))
                    newnumber.position_from = 30
                else:
                    self.team2_matches += 1
                    newnumber = Sprite(self.num_tex, (744, 200))
                    newnumber.position_from = 744
                
                #temp
                #self.team1_matches += 3
                
                # guardamos y actualizamos las estadisticas
                self.stats['player_pass'][0] += self.domino.stats['player_pass'][0]
                self.stats['player_pass'][1] += self.domino.stats['player_pass'][1]
                self.stats['player_pass'][2] += self.domino.stats['player_pass'][2]
                self.stats['player_pass'][3] += self.domino.stats['player_pass'][3]
                
                self.stats['player_win'][0] += self.domino.stats['player_win'][0]
                self.stats['player_win'][1] += self.domino.stats['player_win'][1]
                self.stats['player_win'][2] += self.domino.stats['player_win'][2]
                self.stats['player_win'][3] += self.domino.stats['player_win'][3]
                
                self.stats['game_close'] += self.domino.stats['game_close']
                
                self.stats['hands_played'] += self.domino.stats['hands_played']
                
                #print "llevamos jugadas " + str(self.stats['hands_played']) + " manos"
                
                if self.stats['greatest_close'][0] < self.domino.stats['greatest_close'][0]:
                    self.stats['greatest_close'][0] = self.domino.stats['greatest_close'][0]
                if self.stats['greatest_close'][1] < self.domino.stats['greatest_close'][1]:
                    self.stats['greatest_close'][1] = self.domino.stats['greatest_close'][1]
                
                self.domino.restart()
                self.status = 1
                newnumber.movetime = 0
                self.num_up.insert(0, newnumber)
                
                # calculos para grafica
                self.graph['points1'].append(((750*self.current_match)/self.matches, self.team1_matches))
                self.graph['points2'].append(((750*self.current_match)/self.matches, self.team2_matches))
                
        elif self.status == 3:
            # si no hemos terminado la mano actual, vamos pidiendo fichas
            while not self.domino.end_hand():
                self.domino.ask_tile(self.domino.nextplayer())
            self.status = 2
            self.t_num[-1] += 1
        elif self.status == 99:
            # modo pausa
            #print max(self.t_num)
            pass

        elif self.status == 999:
            # terminamos la partida
            #print self.stats
            """
            if self.team1_matches > self.team2_matches:
                print "winner team 1"
            else:
                print "winner team 2"
            """
            #self.status = 99

    def start(self):
        self.status = 0
        self.domino.create_players(config['player1'],config['player2'],config['player3'],config['player4'])
        #print "empieza el laboratorio"
        self.status = 1

        for player in allplayers:
            if config['player1'] == player['id']: self.p1 = Texture(player['image'])
            if config['player2'] == player['id']: self.p2 = Texture(player['image'])
            if config['player3'] == player['id']: self.p3 = Texture(player['image'])
            if config['player4'] == player['id']: self.p4 = Texture(player['image'])

        self.status_backup = 0
        self.matches = 100
        self.current_match = 0
        self.team1_matches = 0
        self.team2_matches = 0
        self.graph = {
            'position' : (25,325),
            'points1' : [(0, 0)],
            'points2' : [(0, 0)],
        }
        self.stats = {
            'player_pass' : [0, 0, 0, 0],
            'player_win' : [0, 0, 0, 0],
            'game_close' : 0,
            'hands_played' : 0,
            'greatest_close' : [0, 0]
        }
            
    def stop(self):
        self.status = 0

    def mouse_down(self, event):
        if self.status != 1 and event.pos[0] > 25 and event.pos[1] > 532 and event.pos[0] < 186 and event.pos[1] < 574:
            if self.status == 99:
                self.status = self.status_backup
            else:
                self.status_backup = self.status
                self.status = 99
        elif event.pos[0] > 426 and event.pos[1] > 532 and event.pos[0] < 618 and event.pos[1] < 574:
            self.start()
        elif event.pos[0] > 638 and event.pos[1] > 532 and event.pos[0] < 775 and event.pos[1] < 574:
            self.game.goto_menu()
        
