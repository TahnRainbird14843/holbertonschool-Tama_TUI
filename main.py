from pieces import *
from render import *

"""
This is where the chessboard will actually run
"""


def player_move(pieces, player):
    player_input1 = input()
    selected_piece = None

    for piece in pieces:
        if (piece.position[0] == int(player_input1[0]) and piece.position[1] == int(player_input1[1])):
            selected_piece = piece

    if selected_piece is None:
        raise Exception("invalid piece")

    print(selected_piece.get_valid_moves(game_state))
    player_input2 = input()
    new_position = (int(player_input2[0]), int(player_input2[1]))

    print(new_position)
    piece.update_position(new_position)
    game_state[int(player_input1[0])][int(player_input1[1])] = ' '
    game_state[int(player_input2[0])][int(player_input2[1])] = 'p'
    print("player {} succesfully moved".format(player))


if __name__ == "__main__":
    """this first initialisation can be factored out"""
    white_pieces = []
    black_pieces = []
    for i in range(8):
        white_pieces.append(Pawn((6, i), has_moved=False, direction=1))
        black_pieces.append(Pawn((1, i), has_moved=False, direction=-1))
    white_player = Player(1, white_pieces)
    black_player = Player(-1, black_pieces)
    players = [white_player, black_player]


    game_running = True
    game = GameState()
    board = RenderBoard(game.game_state)
    while (game_running):
        curr_player = 0
        piece_pos = game.get_input(player=1)
        move_pos = game.get_input(player=1)
        for piece in players[curr_player].owned_pieces:
            if piece.position == piece_pos:
                piece_to_move = piece
        piece_to_move.update_position(move_pos)
        game.update_game_state(piece_pos, move_pos)
        board.render_pieces(game.game_state)
        curr_player = (curr_player + 1) % 2

