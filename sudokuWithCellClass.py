import numpy

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
    initialState = State(previousStateArray=sudoku, initial=True)

    frontier = [initialState]
    currentState = frontier.pop(0)
    if currentState.IsValid():
        while not currentState.IsGoalState():
            # print("--------------------")
            # print(currentState)
            possibleChildren = GetPossibleChildren(state=currentState)
            frontier.extend(possibleChildren)
            if len(frontier) == 0:
                return (numpy.zeros(shape=(9, 9)) - 1)
            currentState = frontier.pop()
        solved_sudoku = currentState.ToPrint()
        return solved_sudoku
    else:
        return (numpy.zeros(shape=(9, 9)) - 1)




def GetPossibleChildren(state):
    possibleChildren = []
    for cell in range(9*9):
        row = cell // 9
        col = cell % 9
        if state.stateArray[row, col].constant == False and state.stateArray[row, col].value == 0:
            for value in state.stateArray[row, col].domain:
                tempState = State(previousStateArray=state.stateArray)
                tempState.stateArray[row,col].value = value
                if tempState.UpdateDomains(changedCell=tempState.stateArray[row, col]):
                    #print("Here: ", value)
                    possibleChildren.append(tempState)
            break
    return possibleChildren






class State:

    name = 0
    stateArray = numpy.empty(shape=(9,9), dtype = object)

    def __init__(self, previousStateArray, initial=False, name=-1):
        self.name = name
        self.stateArray = numpy.empty(shape=(9,9), dtype = Cell)
        if initial:
            for row in range(9):
                for col in range(9):
                    if previousStateArray[row, col] == 0:
                        self.stateArray[row, col] = Cell(
                            constant=False,
                            value=previousStateArray[row, col],
                            row=row,
                            col=col,
                            square=((row//3)*3 + col//3))
                    else:
                        self.stateArray[row, col] = Cell(
                            constant=True,
                            value=previousStateArray[row, col],
                            row=row,
                            col=col,
                            square=((row//3)*3 + col//3))
            self.UpdateDomains()
        else:
            for row in range(9):
                for col in range(9):
                    self.stateArray[row, col] = Cell(
                        constant=previousStateArray[row, col].constant,
                        value=previousStateArray[row, col].value,
                        row=previousStateArray[row, col].cellRow,
                        col=previousStateArray[row, col].cellCol,
                        square=previousStateArray[row, col].cellSquare
                        )
                    self.stateArray[row, col].domain = previousStateArray[row, col].domain.copy()

    def __eq__(self, other):
        if isinstance(other, State):
            return self.stateArray == other.stateArray

    def __str__(self):
        tempArray = numpy.empty(shape=(9,9))
        for row in range(9):
            for col in range(9):
                tempArray[row, col] = self.stateArray[row, col].value
        return str(tempArray)

    def ToPrint(self):
        tempArray = numpy.empty(shape=(9,9))
        for row in range(9):
            for col in range(9):
                tempArray[row, col] = self.stateArray[row, col].value
        return tempArray

    def UpdateDomains(self, changedCell=None):
        for cell in range(9*9):
            row = cell // 9
            col = cell % 9
            if changedCell == None:
                if self.stateArray[row, col].constant == False:
                    if not self.stateArray[row, col].UpdateDomain(self.stateArray):
                        return False
            else:
                if self.stateArray[row, col].constant == False:
                    if ((self.stateArray[row, col].cellCol == changedCell.cellCol
                    or self.stateArray[row, col].cellRow == changedCell.cellRow
                    or self.stateArray[row, col].cellSquare == changedCell.cellSquare)
                    and not (self.stateArray[row, col].cellCol == changedCell.cellCol
                    and self.stateArray[row, col].cellRow == changedCell.cellRow)):
                        if not self.stateArray[row, col].UpdateDomain(self.stateArray, changedCell=changedCell):
                            return False
        return True


    def IsGoalState(self):
        """
        checks if the state is valid and if there are no zeros
        """
        if not self.__CountZero():
            return True
        return False

    def __CountZero(self):
        """
        Counts the number of zeroes in the state and returns True if there are any zeros present, else if returns false
        """
        for row in range(9):
            for col in range(9):
                if self.stateArray[row, col].value == 0:
                    return True
        return False


    def IsValid(self):

        #Check each row is valid
        for colNum in range(9):
            tempDomains = list(range(1, 10))
            for rowNum in range(9):
                try:
                    if self.stateArray[rowNum, colNum].value != 0:
                        tempDomains.remove(self.stateArray[rowNum, colNum].value)
                except:
                    #print("ERROR: Invalid Row")
                    return False
        
        #Check each column is valid
        for rowNum in range(9):
            tempDomains = list(range(1, 10))
            for colNum in range(9):
                try:
                    if self.stateArray[rowNum, colNum].value != 0:
                        tempDomains.remove(self.stateArray[rowNum, colNum].value)
                except:
                    #print("ERROR: Invalid Column")
                    return False

        #check each square is valid
        for squareNum in range(9):
            tempDomains = list(range(1, 10))
            for squareColNum in range((squareNum%3)*3, (squareNum%3)*3 + 3):
                for squareRowNum in range((squareNum//3)*3, (squareNum//3)*3 + 3):
                    ##print("Row: ", squareRowNum, " Col: ", squareColNum)
                    try:
                        if self.stateArray[squareRowNum, squareColNum].value != 0:
                            tempDomains.remove(self.stateArray[squareRowNum, squareColNum].value)
                    except:
                        #print("ERROR: Invalid Square")
                        return False
        
        return True










class Cell:

    cellRow = 0
    cellCol = 0
    cellSquare = 0
    value = 0
    constant = True
    domain = [range(1,10)]
    exploredDomains = [0]

    def __init__(self, constant, value, row, col, square):
        self.domain = list(range(1,10))
        self.constant = constant
        self.value = value
        self.cellCol = col
        self.cellRow = row
        self.cellSquare = square

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.value == other.value
        elif isinstance(other, int):
            return int(self.value) == other

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __lt__(self, other):
        if isinstance(other, Cell):
            return self.value < other.value

    def UpdateDomain(self, stateArray, changedCell = None):
        if changedCell == None:
            # checking column
            for row in range(9):
                if row != self.cellRow:
                    try:
                        self.domain.remove(stateArray[row, self.cellCol].value)
                    except:
                        pass
            # checking row
            for col in range(9):
                if col != self.cellCol:
                    try:
                        self.domain.remove(stateArray[self.cellRow, col].value)
                    except:
                        pass
            # checking square
            squareColBound = ((self.cellCol//3)*3)
            squareRowBound = ((self.cellRow//3)*3)
            for square in range(9):
                if square != self.cellCol%3 and square//3 != self.cellRow%3:
                    try:
                        self.domain.remove(stateArray[squareRowBound + (square//3), squareColBound + (square%3)].value)
                    except:
                        pass
        else:
            try:
                # print("Changed Cell: ", changedCell.value)
                # print("Value: ", self.value)
                # print("Row: ", self.cellRow, " Col: ", self.cellCol, " Square: ", self.cellSquare)
                # print("Before: ", self.domain)
                self.domain.remove(changedCell.value)
                # print("After:  ", self.domain)
            except:
                # print("Error:  ", self.domain)
                pass
        if len(self.domain) <= 0:
            return False
        return True




SKIP_TESTS = False
stateNumber = 1

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = numpy.load(f"data/{difficulty}_puzzle.npy")
        solutions = numpy.load(f"data/{difficulty}_solution.npy")
        totalTime = 0
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            
            
            #print("Is your solution correct?")
            if numpy.array_equal(your_solution, solutions[i]):
                #print("Yes! Correct solution.")
                count += 1
            else:
                print("======================")
                print(sudoku)
                print(f"This is your solution for {difficulty} sudoku number", i)
                print(your_solution)
                print("No, the correct solution is:")
                print(solutions[i])
                print("======================")
            totalTime += end_time-start_time
            

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        print("This sudoku difficulty took an average of ", totalTime/len(sudokus), "seconds to solve.\n")
        if count < len(sudokus):
            break





"""
# Load sudokus
sudoku = numpy.load("data/very_easy_puzzle.npy")
print()
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print("sudoku.shape:", {sudoku.shape}, " sudoku[0].shape: ", {sudoku[0].shape}, " sudoku.dtype: ", {sudoku.dtype})

# Load solutions for demonstration
solutions = numpy.load("data/very_easy_solution.npy")
print()
#print("Random value:", sudoku)

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")

# ...and its solution
print("Solution of first sudoku:")
print(solutions[0], "\n")
numberOfSolutionsFound = 0

for puzzleNumber in range(15):
    numberOfSolutionsFound += 1
    print("A.I. Solution:")
    print(sudoku_solver(sudoku[puzzleNumber]))
print("Number of Solutions Found: ", numberOfSolutionsFound)
"""

