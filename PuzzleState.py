class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []
        
        self.heap_order = {'Up' : 0, 'Down' : 1, 'Left' : 2, 'Right' : 3 }

        # Get the index and (row, col) of empty block
        self.blank_index = config.index(0)//n , config.index(0)%n

    def __lt__(self, other):
        return (calculate_total_cost(self), self.heap_order[self.action]) < (calculate_total_cost(other), other.heap_order[other.action])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        row,col = self.blank_index
        row_new, col_new = row-1, col
        
        if row_new >= 0:        
            
            new_config = list(self.config)
            
            #swap values in puzzle
            new_config[col+row*self.n] = new_config[col_new+row_new*self.n]
            new_config[col_new+row_new*self.n] = 0
            
            return PuzzleState(new_config, self.n, self, action = "Up", cost = self.cost + 1)
        
        return None

      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        row,col = self.blank_index
        row_new, col_new = row+1, col

        if row_new < self.n:        
            new_config = list(self.config)
          
            #swap values in puzzle
            new_config[col+row*self.n] = new_config[col_new+row_new*self.n]
            new_config[col_new+row_new*self.n] = 0

            return PuzzleState(new_config, self.n, self, action = "Down", cost = self.cost + 1)
        
        return None
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        row,col = self.blank_index
        row_new, col_new = row, col-1
        
        if col_new >= 0:        
            new_config = list(self.config)
       
            #swap values in puzzle
            new_config[col+row*self.n] = new_config[col_new+row_new*self.n]
            new_config[col_new+row_new*self.n] = 0

            return PuzzleState(new_config, self.n, self, action = "Left", cost = self.cost + 1)
        
        return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        row,col = self.blank_index
        row_new, col_new = row, col+1
        
        if col_new < self.n:        
            new_config = list(self.config)
      
            #swap values in puzzle
            new_config[col+row*self.n] = new_config[col_new+row_new*self.n]
            new_config[col_new+row_new*self.n] = 0
            

            return PuzzleState(new_config, self.n, self, action = "Right", cost = self.cost + 1)
        
        return None

    def expand(self):
        """ Generate the children of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children
    
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    sum = 0
    for i in range(0, len(state.config)):
        if state.config[i]!=0:
            sum += calculate_manhattan_dist(i,state.config[i],state.n)
    return sum + state.cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    row,col = idx//n, idx%n
    correct_row, correct_col = value//n, value%n 
    return abs(row-correct_row)+abs(col-correct_col)