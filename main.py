from pieces import *
from game import *

"""
This is where the chessboard will actually run
"""


if __name__ == "__main__":
    """this first initialisation can be factored out"""
    game = GameState()
    (white_pieces, black_pieces) = game.init_game()
    white_player = Player(1, white_pieces)
    black_player = Player(-1, black_pieces)

    game_running = True
    board = RenderBoard(game.game_state)
    curr_player = white_player
    opp_player = black_player
    while (game_running):
        piece_pos = game.get_piece_input(curr_player)
        piece_to_move = game.get_piece_at_pos(curr_player, piece_pos)
        move_pos = game.get_move_input(piece_to_move, curr_player, opp_player)
        piece_to_move.update_position(move_pos)
        captured_piece = opp_player.get_piece_at_position(move_pos)
        if (captured_piece is not None):
            opp_player.owned_pieces.remove(captured_piece)
            del captured_piece
        game.update_game_state(piece_pos, move_pos)
        board.render_pieces(game.game_state)
        tmp = curr_player
        curr_player = opp_player
        opp_player = tmp

