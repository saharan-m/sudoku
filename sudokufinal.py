import time
start_time = time.time()
import copy
from random import randint
board = [
    ".........",
    ".........",
    ".........",
    ".........",
    ".........",
    ".........",
    ".........",
    ".........",
    "........."
]

#Prepares the board, then calls solve() before displaying and returning the result.
def main2():
    global board
    for idx,line in enumerate(board):
        board[idx] = list(line)
    solve()
    printBoard()
    return board


# this function prints out the solved board using the unsolved board created using the main() method
def main3():
    global board
    for idx,line in enumerate(board):
        board[idx] = list(line)
    solve()
    printBoard()
    

#The main workhorse of our program – This function tries to solve for all “obvious” solutions 
#first by making a call to fillAllObvious().
#If required, it fills in a cell by guessing, before making a recursive call to itself.
#solve() returns true if the puzzle has been solved, and false if it has encountered a contradiction, which indicates a wrong guess.
def solve():
    global board
    try:
        fillAllObvious()
    except:
        return False
    if isComplete():
        return True
    i,j = 0,0
    for rowIdx,row in enumerate(board):
        for colIdx,col in enumerate(row):
            if col == ".":
                i,j = rowIdx, colIdx
    possibilities = getPossibilities(i,j)
    for value in possibilities:
        snapshot = copy.deepcopy(board)
        board[i][j] = value
        result = solve()
        if result == True:
            return True
        else:
            board = copy.deepcopy(snapshot)
    return False


#This function loops through all the cells on the board.
#For empty cells, it tries to find what numbers are possible at the cell by using getPossibilities().
#If only one number is possible, the number is filled onto the board.
#This process is repeated until no more cells can be filled by the function.
#If at any point of time we encounter a cell in which no numbers are possible, it indicates that there has been an incorrect value inserted somewhere.
#As such, it raises an exception.
def fillAllObvious():
    global board
    while True:
        somethingChanged = False
        for i in range(0,9):
            for j in range(0,9):
                possibilities = getPossibilities(i,j)
                if possibilities == False:
                    continue
                if len(possibilities) == 0:
                    raise RuntimeError("No moves left")
                if len(possibilities) == 1:
                    board[i][j] = possibilities[0]
                    somethingChanged = True
        if somethingChanged == False:
            return

        
#This function checks which values are possible at a particular cell as indicated by “i” and “j”.
#By starting off with a set, this function works by taking away values it encounters while looping through the row “i” and column “j”, in addition to the square associated with (i,j). 
#The result is cast to a list and returned
def getPossibilities(i,j):
    global board
    if board[i][j] != ".":
        return False
    possibilities = {str(n) for n in range(1,10)}
    for val in board[i]:
        possibilities -= set(val)
    for idx in range(0,9):
        possibilities -= set( board[idx][j] )
    iStart = (i // 3)*3
    jStart = (j // 3)*3
    for row in range(iStart, iStart+3):
        for col in range(jStart, jStart+3):
            possibilities -= set(board[row][col])
    return list(possibilities)


#This function prints out the board after calling makeBoard() i.e. after omitting certain squares to create the puzzle
def main():
    global board
    for idx, line in enumerate(board):
        board[idx] = list(line)
    makeBoard()
    printBoard()
    
    
#According to the difficulty level given by the user, it omits certain squares and creates the actual sudku puzzle 
#by taking the input as a completed board from the main2() method.
def makeBoard():
    global board
    difficulty = input("enter the difficulty level from 1 to 8 : ")
    for square_row in [0,3,6]:
        for square_col in [0,3,6]:
            c1_coo = 0
            c2_coo = 0
            c3_coo = 0
            r_coo = 0
            for val in range(1, int(difficulty)+1):
                if val > 0 and val < 4 :
                    board[r_coo + square_row][c1_coo + square_col] = "."
                    r_coo = 0
                    c1_coo = c1_coo + 1
                if val > 3 and val < 7 :
                    r_coo = 1
                    board[r_coo + square_row][c2_coo + square_col] = "."
                    c2_coo = c2_coo + 1
                if val > 6:
                    r_coo = 2
                    board[r_coo + square_row][c3_coo + square_col] = "."
                    c3_coo = c3_coo + 1


#Loops through all the cells of the board and displays their values.
def printBoard():
    global board
    for row in board:
        for col in row:
            print(col, end="")
        print("")

        
#Checks every cell on the board.
#If no more empty cells (indicated by dots) are encountered, the function returns true. Otherwise, it returns false.        
def isComplete():
    for row in board:
        for col in row:
            if (col == "."):
                return False
    return True

main2()
main()
print()
main3()

end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))