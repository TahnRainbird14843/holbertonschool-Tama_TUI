import curses
import math
from curses import wrapper

game_state = [['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [' ',' ',' ',' ',' ',' ',' ', ' '],
                [' ',' ',' ',' ',' ',' ',' ', ' '],
                [' ',' ',' ',' ',' ',' ',' ', ' '],
                [' ',' ',' ',' ',' ',' ',' ', ' '],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]

game_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

coord_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

class GameState:
    """
    This class represents the current game state,
    it will initialise from a simplified fen representation
    and will keep track of the current board to be printed
    """
    def __init__(self):
        self.fen = game_fen
        self.game_state = game_state
    
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
    
    def fen_to_game_state(self, fen):
        pass
    
    def game_state_to_fen(self, game_state):
        pass
    
    def update_game_state(self, piece_position, move_position):
        self.game_state[move_position[0]][move_position[1]] = self.game_state[piece_position[0]][piece_position[1]]
        self.game_state[piece_position[0]][piece_position[1]] = ' '
    
    def get_input(self, player):
        player_input = input()
        self.validate_input(player_input, player)
        return ((8 - int(player_input[1]), coord_dict[player_input[0]]))

    def validate_input(self, player_input, player):
        if (type(player_input) is not str or len(player_input) != 2 or
                player_input[0] not in list("abcdefgh") or player_input[1] not in list("12345678")):
            raise ValueError("Input must be in standard chess coordinates")


class RenderBoard:
    """
    this is a class which contains the methods to render the board for each game state
    """
    def __init__(self, game_state):
        self.render_base()
        self.render_pieces(game_state)
    
    def render_base(self):
        pass
    
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