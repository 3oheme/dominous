import os, clips

class AI:
    def __init__(self):

        # definimos las plantillas para fichas y tablero

        ficha_name  = 'ficha'
        ficha_text  = '(slot jugador)'
        ficha_text += '(slot ficha_izq)'
        ficha_text += '(slot ficha_der)'
        ficha_comm  = 'fichas en el tablero'

        clips.BuildTemplate(ficha_name, ficha_text, ficha_comm)

        # tablero

        tablero_name  = 'movimiento'
        tablero_text  = '(slot turno)'
        tablero_text += '(slot jugador)'
        tablero_text += '(slot tiempo)'
        tablero_text += '(slot ficha_pegada)'
        tablero_text += '(slot ficha_libre)'
        tablero_comm  = 'cada movimiento del juego'

        clips.BuildTemplate(tablero_name, tablero_text, tablero_comm)

        # estas plantillas luego las hacemos exportables, para que los modulos jugador las importen

        mod_name  = "MAIN"
        mod_body  = "(export deftemplate ?ALL)"
        mod_main = clips.BuildModule(mod_name, mod_body)

        self.players = {}

    def create_players(p1, p2, p3, p4):
        if p1 != "h":
            mod_name  = "JUGADOR1"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[1] = clips.BuildModule(mod_name, mod_body)
            clips.Load('j'+p1+'_reglas.clp')
        if p2 != "h":
            mod_name  = "JUGADOR2"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[2] = clips.BuildModule(mod_name, mod_body)
            clips.Load('j'+p2+'_reglas.clp')
        if p3 != "h":
            mod_name  = "JUGADOR3"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[3] = clips.BuildModule(mod_name, mod_body)
            clips.Load('j'+p3+'_reglas.clp')
        if p4 != "h":
            mod_name  = "JUGADOR4"
            mod_body  = '(import MAIN deftemplate ?ALL)'
            self.players[4] = clips.BuildModule(mod_name, mod_body)
            clips.Load('j'+p4+'_reglas.clp')

    def put_tile(player, board, players_tiles):
        self.players[player].SetFocus()
        self.update_facts(player, board, players_tiles)
        clips.Run(1)
        output = clips.StdoutStream.Read()
        return parse_tile_info(output)

    def update_facts(player, board, players_tiles):
        pass

    def parse_tile_info(output):
        """ Must return new_tile, side"""
        pass
