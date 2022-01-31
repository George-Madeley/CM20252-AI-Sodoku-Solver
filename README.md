# AI Sodoku Solver
## Introduction
The Task was to design an agent to solve given Sudoku puzzles of varying difficulty and solve them under a minute. The program represented the Sudoku puzzles using a 9x9 NumPy array where 0 represented blanks. Each Difficulty, very easy, easy, medium, and hard had fifteen puzzles to solve.

## Method
The design incorporated a backtracking depth-first search with constraint satisfaction. A state class was created with methods to update all the domains, check if the state was a goal state, and remove given values from a given domain.
A function called `sudoku_solver()` used the given sudoku NumPy array to create the initial state. The class constructor would create a NumPy array variable containing all of the sudoku values called stateArray. In addition to this, a list called `stateDomains` stored the domains containing the possible values for each sudoku puzzle element. Initially, the domains store values 1 through 9. The program utilised the equation below to determine the index range for the domain of a given sudoku element from the stateDomain list. 

`tempDomainLowerBound = ((row*81)+(col*9))`
`tempDomainUpperBound = ((row*81)+(col*9))+9`

Where `row` and `col` are the rows and column indexes for the given sudoku element, respectively.
The program updates each domain by checking the row, column and 3x3 square relative to each sudoku element after it created the domains.  The program only used the domains of non-constants(zeros on the given sudoku array) to optimise the program. The update process would remove all non-zero values from the domain apart from the sudoku element's current value. i.e. if the sudoku element had a value of 7, then the update process would remove every other element apart from 7 if the sudoku element was in a complete and valid row, column, or 3x3 square.
The program added the initial state to the frontier after the program created it. Before running the while loop to determine the sudoku's goal state, the program checked the initial state's domains to ensure none of them were empty. If any of them were, the initial state was invalid, and the function would return a 9x9 NumPy array filled with -1.
The while loop would only run if the current state were not the goal state. If the current state satisfied that condition, all the state's possible children were found and appended to the frontier list. The `GetPossibleChildren()` function was responsible for this.
This function would search the current state for the first value, a non-constant and zero. From this, the program calculated the upper and lower bounds for that sudoku element and used them to fetch its domain from the current states domain list. The program replaced the selected sudoku element value with each non-zero value in that element domain. From this, the program updated the surrounding elements domains. The program removed the new value from the element's domains to improve the algorithm's performance. These elements had to be in the same column, row, or 3x3 square as the chosen element. If there were no values in any domain, that new state would not be valid and not added to the list of possible child states. Once all possible domain values were checked and added to the list of possible child states depending on their validity, the function would return that list, and it would get appended to the frontier. 
If the frontier's length were now zero, the while loop would break, and the `sudoku_solver()` function would return a 9x9 NumPy array of -1. If the frontier still contained values, the program replaced the current state value with the most recently added state.
This cycle would repeat until the program found the goal state or the frontier ran out of states. 

## Results
From running this algorithm on a personal computer, the average time for each puzzle difficulty was:
-	Very Easy: 0.026 seconds to solve
-	Easy: 0.019 seconds to solve
-	Medium: 0.025 seconds to solve
-	Hard: 22.370 seconds to solve
However, the program did not solve all hard puzzles under the 30 second time limit.

## Discussion
Initially, the programmer defined the two classes for the solution; a `State` class represented each state of the sudoku problem, a `cell` class that would hold each sudoku cell's value. The program would alter the given sudoku NumPy array into a 9x9 NumPy array of `cell` class instances. Each object would hold a value from 0 to 9, a domain containing numbers from 1 to 9, and a bool to determine if the object's value remained constant. By doing this, the program could call the cells `UpdateDomain()` method for a given cell object, and it would update that specific cell domain. This class made the code neater and easier to work with without using the long list for domains.
However, the programmer discontinued this method as copying cell objects from one state array to the next became very inefficient due to custom-made classes' mutability. To copy objects over, `copy.deepcopy()` from the `copy` library would have to have been used or used a for loop to set each value in the new state array to a new `cell` instance. The program set these new cell attributes to a copy of its predecessor cell. This method did work and even took less time with the very easy, easy and medium difficulty puzzles. However, due to the inefficient copying process, the algorithm was slower with the harder difficulties.
As the previous algorithm already solved a very easy, easy, and medium difficulty puzzle within the one-second constraint and had a short speed with the harder difficulty, the programmer chose that algorithm.

The program did not always store the domains of the state as a long list. Instead, they were a 9x9 NumPy array where each element was a domain list for that elements corresponding element in the state array. However, when copying the state array, issues occurred as the `copy()` function only performs a shallow copy which means the references to nested lists and arrays would be copied over and not the values. `Copy.deepcopy()` would have worked, but it proved to be highly inefficient from tests. `Numpy.copy()` was also a shallow copy. The programmer solved the issue with a list without any nested lists used to store all 81 domains calculating to be 729 domains. The domain for a given sudoku element could be found in the list using the equation above.
An issue came with this as removing elements from the list would cause the equations to be ineffective. As a result, elements from domains were not removed but replaced with zero. This method meant that once the program found the goal state, 88.89% of all the domain list values would be zero and no longer need, in the worst case.

## Conclusion
To conclude, the algorithm has room to improve due to the noticeable inefficiencies of storing domains, two hard puzzles not being solved within the 30-second time frame, and other unknown areas. However, the programmer believes that the agent created does meet the requirements set.