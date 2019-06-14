"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
    
def mc_trial(board, player):
    """
    Plays a single game
    """
    winner = None
    curplayer = player
    while winner == None: 
        row = random.randrange(board.get_dim())
        col = random.randrange(board.get_dim())
        if board.square(row,col)== provided.EMPTY:
            board.move(row,col,curplayer)
            winner = board.check_win()
            curplayer = provided.switch_player(curplayer)

def mc_update_scores(scores,board,player):
    """
    The function scores the completed board and updates the scores grid
    """
    winner = board.check_win()
    if winner == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == player:
                    scores[row][col] += SCORE_CURRENT
                if board.square(row,col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
    if winner == provided.switch_player(player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == player:
                    scores[row][col] -= SCORE_CURRENT 
                if board.square(row,col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER
        
def get_best_move(board,scores):
    """
    Finds all of the empty squares with the maximum score 
    and randomly returns one of them as a (row,column) tuple
    """
    
    empty_list = board.get_empty_squares()
    empty_max_score = []
    if len(empty_list) > 0:
        best_square = empty_list[0]
        for square in empty_list:       
            if scores[square[0]][square[1]] > scores[best_square[0]] [best_square[1]]:
                best_square = square
                empty_max_score = []
            if scores[square[0]][square[1]] == scores[best_square[0]] [best_square[1]]:
                best_square = square
            empty_max_score.append(best_square)   
        return random.choice(empty_max_score)
        


def mc_move(board,player,trials):
    """
    Monte carlo simulation chooses the best_move
    """
    scores = [[0 for dummycol in range(board.get_dim())] 
                      for dummyrow in range(board.get_dim())] 
    for _ in range(trials):
        current_board = board.clone()
        mc_trial(current_board,player)
        mc_update_scores(scores,current_board,player)
    return get_best_move(board,scores)    
                

# test for mc_trial function            
#board = provided.TTTBoard(3)
#mc_trial(board, provided.PLAYERX)
#print str(board)
#print provided.STRMAP[board.check_win()]
#
##test for  mc_update_scores function
#test_scores = [[0 for dummycol in range(3)] 
#                      for dummyrow in range(3)] 
#print test_scores
#mc_update_scores(test_scores,board,provided.PLAYERX)
#print test_scores
#
## test best_move
#print get_best_move(provided.TTTBoard(3, False, 
#                                [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], 
#                                 [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], 
#                                 [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), 
#              [[3, 2, 5], [8, 2, 8], [4, 0, 2]])
                       
        
# Test game with the console or the GUI. 

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
  
    
   
