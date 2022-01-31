import numpy as np

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    ### YOUR CODE HERE
    initialState = State(previousState=sudoku, initial=True)

    frontier = [initialState]
    currentState = frontier.pop(0)
    if currentState.CheckAllDomains(rootState=initialState):
        while not currentState.IsGoalState():
            possibleChildren = GetPossibleChildren(state=currentState, rootState=initialState)
            frontier.extend(possibleChildren)
            if len(frontier) == 0:
                return (np.zeros(shape=(9, 9)) - 1)
            currentState = frontier.pop()
        solved_sudoku = currentState.stateArray
        return solved_sudoku
    else:
        return (np.zeros(shape=(9, 9)) - 1)


def GetPossibleChildren(state, rootState):
    """
    Calculates and returns all of the possible child states of a given state

    Parameters:
        state (State): The Parent state of all the child states to be created.
        rootState (State): The root state, of the algorithm, used ot base the constants off of.

    Returns:
        list: A list of possible child states of the given state. Empty if no possible child states could be found
    """
    possibleChildren = []
    for cell in range(9*9):
        row = cell // 9
        col = cell % 9
        if rootState.stateArray[row][col] == 0 and state.stateArray[row][col] == 0:
            tempDomainUpperBound = ((row*81)+(col*9))+9
            tempDomainLowerBound = ((row*81)+(col*9))
            tempDomain = state.stateDomains[tempDomainLowerBound:tempDomainUpperBound]
            for value in tempDomain:
                if value != 0:
                    tempState = State(previousState=state)
                    tempState.stateArray[row][col] = value
                    #print("Here 1")
                    if tempState.CheckAllDomains(changedCellValue=value, changedCol=col, changedRow=row, changedSquare=(row//3 + ((col//3)*3)), rootState=rootState):
                        possibleChildren.append(tempState)
            break
    return possibleChildren










class State:
    """
    This is a State class containing the informationa and methods of states within the sudoku puzzle

    Attributes:
        stateArray (numpy.array): a 9x9 numpy.array containing the values of the sudoku puzzle at the current state
    """

    stateArray = np.empty(shape=(9,9))

    def __init__(self, previousState, initial=False):
        """
        The constructor fo the State class

        Parameters:
            previousState (State or List): The parent State or list of the this state
            initial (bool): True if this is the root state
        """
        if initial:
            self.stateArray = previousState.copy()
            self.stateDomains = np.tile(list(range(1, 10)), 81)
            self.CheckAllDomains(rootState=self)
        else:
            self.stateDomains = previousState.stateDomains.copy()
            self.stateArray = previousState.stateArray.copy()

    def __eq__(self, other):
        """
        Checks if two states are equal

        Parameters:
            other (State): The other state to be compared

        Returns:
            bool: True if stateArray of both the current and other state are the same.
        """
        if isinstance(other, State):
            return self.stateArray == other.stateArray

    def __str__(self):
        """
        Gets a string of the stateArray

        Returns:
            string: A string of the stateArray
        """
        return str(self.stateArray)

    def CheckAllDomains(self, rootState, changedCellValue=0, changedCol=None, changedRow=None, changedSquare=None):
        """
        Updates all the domains
        This updates all or some of the domains depending on the value of changedCellValue.

        Parameters:
            rootState (State): state, usually the initial state, used to determine where the constant are.
            changedCellValue (int): the value of the cell that was just changed
            changedCol (int): the column number of that changed cell
            changedRow (int): the row number of that changed cell
            changedSquare (int): the square number of that changed cell

        Returns:
            bool: False if a domain returns with no values. True if all domains have atleast one value
        """
        for row in range(9):
            for col in range(9):
                if changedCellValue == 0:
                    if not self.CheckDomain(cellRow=row, cellCol=col):
                        return False
                else:
                    if rootState.stateArray[row][col] == 0:
                        if (col == changedCol or row == changedRow or (row//3 + ((col//3)*3)) == changedSquare) and not (col == changedCol and row == changedRow):
                            if not self.RemoveDomainValue(cellRow=row, cellCol=col, value=changedCellValue):
                                return False
        return True

    def CheckDomain(self, cellRow, cellCol):
        """
        Checks the value of a given cells domain.
        Updates and checks the domain of a given cell to ensure if it is empty or not.

        Paramters:
            cellRow (int): The row number of the cell to have its domain updated
            cellCol (int): The col number of the cell to have its domain updated

        Returns:
            bool: True if the domain still contains non-zero values. False if all the values in the domain are zero
        """

        tempDomain = self.GetDomain(cellCol=cellCol, cellRow=cellRow)
        if np.count_nonzero(tempDomain) == 0:
            return False
        self.stateDomains[((cellRow*81)+(cellCol*9)):((cellRow*81)+(cellCol*9))+9] = tempDomain
        return True

    def GetDomain(self, cellRow, cellCol):
        """
        Gets a new and checked domain of a cell
        It creates a new domain and then updates what domain using the values in the same row, column, and square that the given cell is in

        Parameters:
            cellRow (int): the row number of the cell to have its domain updated
            cellCol (int): the column number of the cell to have its domain updated

        Returns:
            int List: The newly created domain for the given cell
        """
        # checking column
        tempDomain = list(range(1,10))
        for domainRow in range(9):
            if domainRow != cellRow:
                tempDomain = np.where(tempDomain==self.stateArray[domainRow][cellCol], 0, tempDomain)
        # checking row
        for domainCol in range(9):
            if domainCol != cellCol:
                tempDomain = np.where(tempDomain==self.stateArray[cellRow][domainCol], 0, tempDomain)
        # checking square
        squareColBound = ((cellCol//3)*3)
        squareRowBound = ((cellRow//3)*3)
        for square in range(9):
            if squareRowBound + (square//3) != cellRow and squareColBound + (square%3) != cellCol:
                tempDomain = np.where(tempDomain!=self.stateArray[squareRowBound + (square//3)][squareColBound + (square%3)], tempDomain, 0)
        return tempDomain

    def RemoveDomainValue(self, cellRow, cellCol, value):
        """
        Removes a value from a domain.
        Gets a domain of a given cell and removes a given value from it

        Parameters:
            cellRow (int): The row number of the cell to have its domain updated
            cellCol (int): The column number of the cell to have its domain updated
            value (int): The value to be removed from the given cells' domain

        Returns:
            bool: Returns True if the domain still constains non-zero values. False if it contains all zeros.
        """
        tempDomainUpperBound = ((cellRow*81)+(cellCol*9))+9
        tempDomainLowerBound = ((cellRow*81)+(cellCol*9))
        tempDomain = self.stateDomains[tempDomainLowerBound:tempDomainUpperBound]
        tempDomain = np.where(tempDomain==value, 0, tempDomain)
        if np.count_nonzero(tempDomain) == 0:
            return False
        self.stateDomains[tempDomainLowerBound:tempDomainUpperBound] = tempDomain#print("State domain after: ", self.stateDomains[tempDomainLowerBound:tempDomainUpperBound])
        return True

    def IsGoalState(self):
        """
        Checks if the state is a goal state

        Returns:
            bool: Returns True if there are no zero value in the stateArray. Returns False if there is atleast one zero in the stateArray.
        """
        if np.count_nonzero(self.stateArray) == 81:
            return True
        return False


    




SKIP_TESTS = False

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard'] # ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        totalTime = 0
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            #print("=================================")
            print(f"This is {difficulty} sudoku number", i)
            #print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            
            
            
            #print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                #print("Yes! Correct solution.")
                count += 1
            else:
                print(f"This is your solution for {difficulty} sudoku number", i)
                print(your_solution)
                print("No, the correct solution is:")
                print(solutions[i])
            totalTime += end_time-start_time
            

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        print("This sudoku difficulty took an average of ", totalTime/len(sudokus), "seconds to solve.\n")
        if count < len(sudokus):
            break





"""
# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print()
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print("sudoku.shape:", {sudoku.shape}, " sudoku[0].shape: ", {sudoku[0].shape}, " sudoku.dtype: ", {sudoku.dtype})

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()
#print("Random value:", sudoku)

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")

# ...and its solution
print("Solution of first sudoku:")
print(solutions[0], "\n")

print("A.I. Solution:")
print(sudoku_solver(sudoku[0]))
"""

