from pieces import *
from render import *

"""
This is where the chessboard will actually run
"""


if __name__ == "__main__":
    """this first initialisation can be factored out"""
    white_pieces = []
    black_pieces = []
    for i in range(8):
        white_pieces.append(Pawn((6, i), has_moved=False, direction=1))
        black_pieces.append(Pawn((1, i), has_moved=False, direction=-1))
    for i in range(2):
        white_pieces.append(Rook((7, i * 7)))
        black_pieces.append(Rook((0, i * 7)))
    for i in range(2):
        white_pieces.append(Knight((7, i * 5 + 1)))
        black_pieces.append(Knight((0, i * 5 + 1)))
    for i in range(2):
        white_pieces.append(Bishop((7, i * 3 + 2)))
        black_pieces.append(Bishop((0, i * 3 + 2)))
    white_pieces.append(Queen((7, 3)))
    black_pieces.append(Queen((0, 3)))
    white_pieces.append(King((7, 4)))
    black_pieces.append(King((0, 4)))
    white_player = Player(1, white_pieces)
    black_player = Player(-1, black_pieces)
    players = [white_player, black_player]


    game_running = True
    game = GameState()
    board = RenderBoard(game.game_state)
    curr_player = 0
    opp_player = 1
    while (game_running):
        piece_pos = game.get_input(player=1)
        move_pos = game.get_input(player=1)
        piece_to_move = None
        for piece in players[curr_player].owned_pieces:
            if piece.position == piece_pos:
                piece_to_move = piece
        if (piece_to_move is not None):
            if (tuple_in_list(move_pos, piece_to_move.get_valid_moves(players[curr_player], players[opp_player]))):
                piece_to_move.update_position(move_pos)
                captured_piece = players[opp_player].get_piece_at_position(move_pos)
                if (captured_piece is not None):
                    players[opp_player].owned_pieces.remove(captured_piece)
                    del captured_piece
                game.update_game_state(piece_pos, move_pos)
            else:
                print("Sorry! That move was invalid, skipping turn")
        else:
            print("Sorry! There was no piece selected, skipping turn")
        board.render_pieces(game.game_state)
        curr_player = (curr_player + 1) % 2
        opp_player = (opp_player + 1) % 2

