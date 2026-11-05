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
    board = wrapper(RenderBoard)
    board.render_base()
    board.render_pieces(game.game_state)

    curr_player = white_player
    opp_player = black_player

    while (game_running):
        piece_pos = game.get_piece_input(curr_player)
        piece_to_move = game.get_piece_at_pos(curr_player, piece_pos)
        move_pos, captured_piece, capture_pos = game.get_move_input(piece_to_move, curr_player, opp_player)

        piece_to_move.update_position(move_pos)
        curr_player.update_castling_rights(piece_to_move)
        curr_player.update_en_passant(piece_to_move, piece_pos, move_pos, is_curr=True)
        opp_player.update_en_passant(piece_to_move, piece_pos, move_pos, is_curr=False)

        if isinstance(captured_piece, King):
            break
        elif (captured_piece is not None):
            opp_player.owned_pieces.remove(captured_piece)
            del captured_piece

        game.update_game_state(curr_player, piece_to_move, piece_pos, move_pos, capture_pos)
        board.render_pieces(game.game_state)

        tmp = curr_player
        curr_player = opp_player
        opp_player = tmp

    if curr_player.player == 1:
        print("White Wins!")
    else:
        print("Black Wins!")
