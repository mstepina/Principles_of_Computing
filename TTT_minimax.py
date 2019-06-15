"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Makes a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1,-1)
    else:
        best_score = -1
        best_square = (-1,-1)
        for square in board.get_empty_squares():    
            clone_board = board.clone()
            clone_board.move(square[0], square[1], player)
            square_result = mm_move(clone_board, provided.switch_player(player))
            current_score = square_result[0] * SCORES[player]
            if current_score == 1: 
                return square_result[0], square
            if current_score >= best_score:
                best_score = current_score
                best_square = square              
        return best_score* SCORES[player], best_square     

#print  mm_move(provided.TTTBoard(3, False,
#                           [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], 
#                            [provided.PLAYERO, provided.PLAYERO, provided.EMPTY],
#                            [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]),
#         provided.PLAYERX)
#returned bad move (-1, (2, 2))    
                

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
