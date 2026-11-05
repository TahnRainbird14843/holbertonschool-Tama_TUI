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
                         'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F',
                         ' ': ' '}


"""gamestate should keep track of en_passant and castling rights for each player"""
class GameState:
    """
    This class represents the current game state,
    it will initialise from a simplified fen representation
    and will keep track of the current board to be printed
    """
    def __init__(self, en_passant=None):
        self.fen = game_fen
        self.game_state = [[' ' for _ in range(8)] for _ in range(8)]
        self.en_passant = en_passant
    
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
    
    def update_game_state(self, player, piece, piece_position, move_position, capture_position):
        self.game_state[move_position[0]][move_position[1]] = self.game_state[piece_position[0]][piece_position[1]]
        self.game_state[piece_position[0]][piece_position[1]] = ' '
        if capture_position is not None and capture_position != move_position:
            self.game_state[capture_position[0]][capture_position[1]] = ' '
        if isinstance(piece, King):
            self.check_castle(player, piece_position, move_position)
        elif isinstance(piece, Pawn) and move_position[0] in [7, 0]:
            self.promote_pawn(player, piece, move_position)
    
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

        captured_piece = opponent.get_piece_at_position(coord_input)
        if isinstance(piece, Pawn) and opponent.en_passant is not None and coord_input == opponent.en_passant:
            captured_piece = opponent.get_piece_at_position(add_tuple(coord_input, (-opponent.player, 0)))
        if captured_piece is not None:
            capture_pos = captured_piece.position
        else:
            capture_pos = None
        return coord_input, captured_piece, capture_pos
            
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

    def check_castle(self, player, piece_pos, move_pos):
        if move_pos[1] - piece_pos[1] == 2:
            rank = piece_pos[0]
            rook = player.get_piece_at_position((rank, 7))
            rook.update_position((rank, 5))
            self.update_game_state((rank, 7), (rank, 5), None)

        elif move_pos[1] - piece_pos[1] == -2:
            rank = piece_pos[0]
            rook = player.get_piece_at_position((rank, 0))
            rook.update_position((rank, 3))
            self.update_game_state((rank, 0), (rank, 3), None)

    def promote_pawn(self, player, piece, move_pos):
        player.owned_pieces.remove(piece)
        new_queen = Queen(move_pos, player.player)
        player.owned_pieces.append(new_queen)
        symbol = 'q'
        if player.player == 1:
            symbol = 'Q'
        self.game_state[move_pos[0]][move_pos[1]] = piece_to_unicode_dict[symbol]



class RenderBoard:
    """
    this is a class which contains the methods to render the board for each game state
    """
    def __init__(self, stdscreen, sq_dimensions=(5, 3)):
        self.screen = stdscreen
        self.sq_dimensions = sq_dimensions
        curses.curs_set(0)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        print("\033[?1003h\n")

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

        for i in range(8):
            self.screen.addch(8 * self.sq_dimensions[1] + 2, i * self.sq_dimensions[0] + 4, list(coord_dict.keys())[i])
            self.screen.addch(1, i * self.sq_dimensions[0] + 4, list(coord_dict.keys())[i])

        for i in range(8):
            self.screen.addch(i * self.sq_dimensions[1] + 3, 0, f"{8 - i}")
            self.screen.addch(i * self.sq_dimensions[1] + 3, 8 * self.sq_dimensions[0] + 3, f"{8 - i}")

        self.screen.refresh()

    def get_square(self, coord):
        coord_list = []
        for i in range(self.sq_dimensions[0]):
            for j in range(self.sq_dimensions[1]):
                coord_list.append((self.sq_dimensions[0] * coord[0] + i, self.sq_dimensions[1] * coord[1] + j))
        return coord_list

    def render_pieces(self, game_state):
        for col in range(8):
            for row in range(8):
                square_centre = self.get_square((col, row))[7]
                self.screen.addch(square_centre[1] + 2, square_centre[0] + 2,
                                  game_state[row][col], curses.color_pair((col + row) % 2))

        self.screen.refresh()
