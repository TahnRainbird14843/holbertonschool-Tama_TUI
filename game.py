import curses
import math
from curses import wrapper
from helpers import *
from pieces import *

game_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

coord_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
piece_to_class_dict = {'P': Pawn, 'R': Rook, 'B': Bishop, 'N': Knight, 'Q': Queen, 'K': King,
                       'p': Pawn, 'r': Rook, 'b': Bishop, 'n': Knight, 'q': Queen, 'k': King}
piece_to_unicode_dict = {'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657',
                         'N': '\u2658', 'P': '\u2659', 'k': '\u265A', 'q': '\u265B',
                         'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'}


"""gamestate should keep track of en_passant and castling rights for each player"""
class GameState:
    """
    This class represents the current game state,
    it will initialise from a simplified fen representation
    and will keep track of the current board to be printed
    """
    def __init__(self):
        self.fen = game_fen
        self.game_state = [[' ' for _ in range(8)] for _ in range(8)]
    
    @property
    def fen(self):
        return (self.__fen)
    
    @fen.setter
    def fen(self, fen):
        self.validate_fen(fen)
        self.__fen = fen
    
    @property
    def game_state(self):
        return (self.__game_state)

    @game_state.setter
    def game_state(self, game_state):
        self.validate_game(game_state)
        self.__game_state = game_state
    
    def validate_fen(self, fen):
        pass
    
    def validate_game(self, game_state):
        pass
    
    def init_game(self):
        i = j = 0
        white_pieces = []
        black_pieces = []
        try:
            for chr in self.fen:
                if (chr.isnumeric()):
                    j += int(chr)
                elif (chr.islower()):
                    black_pieces.append(piece_to_class_dict[chr]((i, j), direction=-1))
                    self.game_state[i][j] = piece_to_unicode_dict[chr]
                    j += 1
                elif (chr.isupper()):
                    white_pieces.append(piece_to_class_dict[chr]((i, j), direction=1))
                    self.game_state[i][j] = piece_to_unicode_dict[chr]
                    j += 1
                elif (chr == '/' and j == 8):
                    i += 1
                    j = 0
                else:
                    raise ValueError('Invalid fen')
        except:
            raise ValueError('Invalid fen')
        return (white_pieces, black_pieces)
    
    def get_fen(self, game_state):
        pass
    
    def update_game_state(self, piece_position, move_position):
        self.game_state[move_position[0]][move_position[1]] = self.game_state[piece_position[0]][piece_position[1]]
        self.game_state[piece_position[0]][piece_position[1]] = ' '
    
    def get_piece_input(self, player):
        coord_input = None
        while (coord_input is None):
            player_input = input()
            coord_input = self.validate_piece_input(player_input, player)
        return coord_input

    def get_move_input(self, piece, hero, opponent):
        coord_input = None
        while (coord_input is None):
            player_input = input()
            coord_input = self.validate_move_input(player_input, piece, hero, opponent)
        return coord_input
            
    def get_piece_at_pos(self, player, coord):
        for piece in player.owned_pieces:
            if (piece.position == coord):
                return piece

    def validate_piece_input(self, player_input, player):
        if (type(player_input) is not str or len(player_input) != 2 or
                player_input[0] not in list("abcdefgh") or player_input[1] not in list("12345678")):
            return None
        coord_input = (8 - int(player_input[1]), coord_dict[player_input[0]])
        if (not tuple_in_list(coord_input, player.piece_pos_list())):
            print("invalid input {}".format(coord_input))
            return None
        return coord_input

    def validate_move_input(self, player_input, piece, hero, opponent):
        if (type(player_input) is not str or len(player_input) != 2 or
                player_input[0] not in list("abcdefgh") or player_input[1] not in list("12345678")):
            return None
        coord_input = (8 - int(player_input[1]), coord_dict[player_input[0]])
        if (not tuple_in_list(coord_input, piece.get_valid_moves(hero, opponent))):
            print("invalid input {}".format(coord_input))
            return None
        return coord_input



class RenderBoard:
    """
    this is a class which contains the methods to render the board for each game state
    """
    def __init__(self, stdscreen, sq_dimensions=(5, 3)):
        self.screen = stdscreen
        self.sq_dimensions = sq_dimensions

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, stdscreen):
        self.__screen = stdscreen

    @property
    def sq_dimensions(self):
        return self.__sq_dimensions

    @sq_dimensions.setter
    def sq_dimensions(self, sq_dimensions):
        self.__sq_dimensions = sq_dimensions

    def render_base(self):
        self.screen.clear()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        for i in range(8):
            for j in range(8):
                for tup in self.get_square((i, j)):
                    self.screen.addstr(tup[1] + 2, tup[0] + 2, " ", curses.color_pair(1))
            
        for i in range(8):
            for j in range(8):
                if ((i + j) % 2 == 0):
                    for tup in self.get_square((i, j)):
                        self.screen.addstr(tup[1] + 2, tup[0] + 2, " ", curses.color_pair(2))

        self.screen.refresh()

        self.screen.getch()

    def get_square(self, coord):
        coord_list = []
        for i in range(self.sq_dimensions[0]):
            for j in range(self.sq_dimensions[1]):
                coord_list.append((self.sq_dimensions[0] * coord[0] + i, self.sq_dimensions[1] * coord[1] + j))
        return coord_list

    def render_pieces(self, game_state):
        for i in range(8):
            print("{}  {}".format(8 - i, game_state[i]))
        print("     a    b    c    d    e    f    g    h")

"""
def render_board(stdscr):
    # Clear screen
    stdscr.clear()

    sq_width = 5
    sq_height = 3
    nrows = sq_height * 8
    ncols = sq_width * 8

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    for i in range(nrows):
        for j in range(ncols):
            if ((math.floor(i / sq_height) + math.floor(j / sq_width)) % 2 == 0):
                if (i % sq_height == math.floor(sq_height / 2) and j % sq_width == math.floor(sq_width / 2)):
                    stdscr.addstr(i, j, game_state[math.floor(i / sq_height)][math.floor(j / sq_width)], curses.color_pair(1))
                else:
                    stdscr.addstr(i, j, " ", curses.color_pair(1))
            else:
                if (i % sq_height == math.floor(sq_height / 2) and j % sq_width == math.floor(sq_width / 2)):
                    stdscr.addstr(i, j, game_state[math.floor(i / sq_height)][math.floor(j / sq_width)], curses.color_pair(2))
                else:
                    stdscr.addstr(i, j, " ", curses.color_pair(2))

    # Refresh the screen to show the message
    stdscr.refresh()
    
    # Wait for user input before exiting
    stdscr.getch()

if (__name__ == "__main__"):
    wrapper(render_board)
"""

board = wrapper(RenderBoard)
board.render_base()