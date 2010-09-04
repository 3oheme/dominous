import os, clips
from tools import *

class AI:
    def __init__(self):

        # plantilla de fichas del jugador

        ficha_name  = 'ficha'
        ficha_text  = '(slot ficha_izq)'
        ficha_text += '(slot ficha_der)'
        ficha_comm  = 'fichas del jugador'

        clips.BuildTemplate(ficha_name, ficha_text, ficha_comm)

        # plantilla del tablero, representado por los movimientos

        tablero_name  = 'movimiento'
        tablero_text  = '(slot turno)'
        tablero_text += '(slot jugador)'
        tablero_text += '(slot tiempo)'
        tablero_text += '(slot ficha)'
        tablero_text += '(slot lado)'
        tablero_comm  = 'cada movimiento del juego'

        clips.BuildTemplate(tablero_name, tablero_text, tablero_comm)

        # plantilla header con elementos de ayuda

        header_name  = 'header'
        header_text  = '(slot ficha_izq)'
        header_text += '(slot ficha_der)'
        header_text += '(slot turno)'
        header_comm  = 'plantilla de ayuda'

        clips.BuildTemplate(header_name, header_text, header_comm)

        # estas plantillas luego las hacemos exportables, para que los modulos jugador las importen

        mod_name  = "MAIN"
        mod_body  = "(export deftemplate ?ALL)"
        mod_main = clips.BuildModule(mod_name, mod_body)

        clips.Reset()

        self.players = {}

    def create_players(self, p1, p2, p3, p4):
        if p1 != "h":
            mod_name  = "JUGADOR1"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[1] = clips.BuildModule(mod_name, mod_body)
            clips.Load(tool.ai('easy')) # FIXME mod to enable select a different difficult level
        if p2 != "h":
            mod_name  = "JUGADOR2"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[2] = clips.BuildModule(mod_name, mod_body)
            clips.Load(tool.ai('easy')) # FIXME
        if p3 != "h":
            mod_name  = "JUGADOR3"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[3] = clips.BuildModule(mod_name, mod_body)
            clips.Load(tool.ai('easy')) # FIXME
        if p4 != "h":
            mod_name  = "JUGADOR4"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[4] = clips.BuildModule(mod_name, mod_body)
            clips.Load(tool.ai('easy')) # FIXME

    def put_tile(self, player, board, players_tiles):
        self.players[player].SetFocus()
        clips.Run(1)
        output = clips.StdoutStream.Read()
        return parse_tile_info(output)

    def add_move(self, player, tile, side):
        for k, v in self.players:
            self.players[k].SetFocus()
            clips.BuildDeffacts("movimiento", "(jugador "+player+")(ficha "+tile+")(lado "+side+")")

    def update_header(self, counter, left_side, right_side):
        # FIXME
        # quitar la regla header y poner la nueva - http://pyclips.sourceforge.net/manual/pyclips-objects.html - Retract()
        for k, v in self.players:
            self.players[k].SetFocus()
            rule_name  = 'temporal'
            rule_prec  = '(declare (salience 99))'
            rule_prec += 'h1<-(header ?h)'
            rule_body  = 'modify ?h1 (ficha_izq '+ left_side+') (ficha_der '+ right_side +') (turno '+ counter +'))'
            delete_me = clips.BuildRule(rule_name, rule_prec, rule_body)
            clips.Run(1)
            delete_me.Remove()
        pass

    def set_player_tile(self, tile):
        self.players[player].SetFocus()
        clips.BuildDeffacts("ficha", "(jugador "+player+")(ficha_izq "+tile[0]+")(ficha_der "+tile[1]+")")

    def parse_tile_info(self, output):
        """ Must return new_tile, side""" 
        return "XX", "XX" # FIXME
