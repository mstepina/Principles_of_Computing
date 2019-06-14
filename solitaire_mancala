"""
Solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Creates Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        List configuration of initial number of seeds for given houses.
        House zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """

        self._board = list(configuration)     
    
    def __str__(self):
        """
        Returns string representation for Mancala board
        """
        a_mancala = list(self._board)
        a_mancala.reverse()
        return str(a_mancala)
    
    def get_num_seeds(self, house_num):
        """
        Returns the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Checks to see if all houses but house zero are empty
        """
        return sum(self._board[1:]) == 0
    
    def is_legal_move(self, house_num):
        """
        Checks whether a given move is legal
        """
        if house_num == 0:
            return False
        return self._board[house_num] == house_num

   
    def apply_move(self, house_num):
        """
        Moves all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            for index in range(house_num):
                self._board[index] += 1
                self._board[house_num] -= 1   
        return self._board               

    def choose_move(self):
        """
        Returns the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for index in range(1, len(self._board)):
            if self.is_legal_move(index):
                return index
        return 0

    
    def plan_moves(self):
        """
        Returns a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        plan = []
        temp_game = SolitaireMancala()
        temp_game.set_board(self._board)
        move = temp_game.choose_move()
        while move != 0:
            temp_game.apply_move(move)
            plan.append(move)
            move = temp_game.choose_move()      
        return plan
       

# tests

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    owl_game = SolitaireMancala()
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1) 
    config2 = [0, 1, 2, 3]
    owl_game.set_board(config2)
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(1),"Expected: False"
    print "Testing choose move - Computed:", my_game.choose_move(),"Expected: 5"
    print "Testing apply_move - Computed:", my_game.apply_move(5),"Expected: [1,1,2,2,4,0,0]"
    print "Testing plan_moves - Computed:", my_game.plan_moves(),"Expected: [5,1,2,1,4,1,3,1,2,1]"
    print "Testing plan_moves - Computed:", owl_game.plan_moves(),"Expected: [1,2,1,3,1]"
test_mancala()


# Import GUI code 
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())
