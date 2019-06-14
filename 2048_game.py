"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def slide(lst):
    """
    Slides numbers in the list to the left
    """
    
    result = []
    for num in range(0,len(lst)):
        result.append(0)
    index_result = 0 
    for num in lst:
        if num != 0:
            result[index_result] = num
            index_result += 1
    return result        
    
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = slide(line)
    new_result = list(result)        
    for num in range(0,len(result)-1):
        if result[num] == result[num +1]:
            new_result[num] = result[num]*2
            new_result[num +1] = 0
            result[num +1] = 0
    new_result = slide(new_result)        
    return new_result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):        
        self._grid_height = grid_height
        self._grid_width = grid_width
        indices_directions = {}
        
        up_ind = []
        down_ind = []
        for col in range(grid_width):
            up_ind.append((0,col))
            down_ind.append((grid_height-1,col))             
            
        left_ind = []
        right_ind = []
        for row in range(grid_height):
            left_ind.append((row,0))
            right_ind.append((row,grid_width-1))
        
        indices_directions[UP] = up_ind
        indices_directions[DOWN] = down_ind
        indices_directions[LEFT] = left_ind
        indices_directions[RIGHT] = right_ind
        self._indices_directions = indices_directions
            
        self.reset()

    def reset(self):
        """
        Resets the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [[0 for dummy_col in range(self._grid_width)]
                           for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

        
    def __str__(self):
        """
        Returns a string representation of the grid for debugging.
        """
        return "The board is" + str(self._cells) + str(self._indices_directions)


    def get_grid_height(self):
        """
        Gets the height of the board.
        """
        return self._grid_height

    
    def get_grid_width(self):
        """
        Gets the width of the board.
        """
        return self._grid_width

    
    def move(self, direction):
        """
        Moves all tiles in the given direction and adds
        a new tile if any tiles moved.
        """
        
        if direction == UP or direction == DOWN:
            steps = self._grid_height
        else:
            steps = self._grid_width
        changes = 0    
        for tile in self._indices_directions[direction]:            
            one_ind = []
            for step in range(steps):
                row = tile[0]+ step*OFFSETS[direction][0]
                col = tile[1] + step* OFFSETS[direction][1]
                cell = (row,col)
                one_ind.append(cell)   
            temp_values = []    #values in this col/row
            for nom in range(len(one_ind)):
                value = self.get_tile(one_ind[nom][0], one_ind[nom][1])
                temp_values.append(value)
            new_values = merge(temp_values)# merge values
            for nim in range(len(new_values)):#this col/row with new values back to grid             
                if temp_values[nim] != new_values[nim]:
                    self.set_tile(one_ind[nim][0], one_ind[nim][1],new_values[nim])
                    changes += 1
        if changes > 0:
            self.new_tile()    
                       
    def new_tile(self):
        """
        Creates a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_cells = []
        for row in range(self._grid_height):
            for cell in range (self._grid_width):
                if self._cells[row][cell] == 0:
                    empty_cells.append((row,cell))
        chosen = random.choice(empty_cells)
        prob = random.randint(1, 10)
        if prob <= 9:
            self._cells[chosen[0]][chosen[1]]= 2
        else:
            self._cells[chosen[0]][chosen[1]] = 4
        

    def set_tile(self, row, col, value):
        """
        Sets the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

        
    def get_tile(self, row, col):
        """
        Returns the value of the tile at position row, col.
        """
        return self._cells[row][col]


#import user45_g0J17uPiBz_19 as test_suite
#test_suite.run_suite(TwentyFortyEight)
poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
