from helpers import add_tuple
from render import game_state

"""
This is for creating the different piece classes
"""


class Player:
    """
    The player class owns pieces, and is split into the two
    chess players

    This class also will get the user input for each player
    """
    def __init__(self, player, pieces):
        self.player = player
        self.owned_pieces = pieces
    
    @property
    def owned_pieces(self):
        return self.__owned_pieces

    @owned_pieces.setter
    def owned_pieces(self, pieces):
        self.__owned_pieces = pieces
    
    @property
    def player(self):
        return (self.__player)

    @player.setter
    def player(self, player):
        self.validate_player("Player - player", player)
        self.__player = player

    def validate_player(self, name, value):
        if (value != 1 and value != -1):
            raise TypeError("{} must be in [1, -1]".format(name))



class Piece:
    """
    The Piece class encompasses all the different pieces
    which can be owned by a player, it implements a shared position
    and requires each piece to have a method to find its valid moves

    User 1 to indicate white player and -1 to indicate black player
        This is so that the pawns get their direction specified inherently
        by their color
    """
    def __init__(self, position):
        self.position = position
    
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, position):
        if (not self.validate_position(position)):
            raise ValueError("starting position must be a length 2 tuple of",
                            "integers that fits on the chess grid")
        self.__position = position
    
    def validate_position(self, position):
        return (type(position) is tuple and len(position) == 2 and
                0 <= position[0] < 8 and 0 <= position[1] < 8)

    def get_valid_moves(self, position, game_state):
        raise Exception("get_valid_moves needs to be implemented in each subclass")

    def update_position(self, new_position):
        raise Exception("update_position needs to be implemented in each subclass")
    
    def validate_boolean(self, name, boolean):
        if (type(boolean) is not bool):
            raise TypeError("{} must be a boolean".format(name))


class Pawn(Piece):
    """
    The Pawn has a unique variable has_moved which handles the double
    move on turn 1
    """
    def __init__(self, position, has_moved=False, direction=1):
        super().__init__(position)
        self.has_moved = has_moved
        self.direction = direction

    @property
    def has_moved(self):
        return self.__has_moved
    
    @has_moved.setter
    def has_moved(self, has_moved):
        super().validate_boolean("pawn - has_moved", has_moved)
        self.__has_moved = has_moved
    
    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.validate_direction(direction)
        self.__direction = direction
    
    def validate_direction(self, direction):
        if (direction not in [1, -1]):
            raise ValueError("direction of pawn must be either 1 or -1 depending on which player it is owned by")
    
    def get_valid_moves(self, game_state):
        moves = []
        check_move = add_tuple(self.position, (self.direction * 1, 0))
        if (super().validate_position(check_move)):
            moves.append((check_move))
        check_move = add_tuple(self.position, (self.direction * 2, 0))
        if (super().validate_position(check_move) and not self.has_moved):
            moves.append((check_move))
        return(moves)

    def update_position(self, new_position):
        self.__init__(new_position, has_moved=True, direction = self.direction)
