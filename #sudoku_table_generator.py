#sudoku_table_generator.py

import random

# recursive method which generates a legitimate Sudoku board

def make_board(board): 
    # loop through the board to find the next empty cell
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                # try placing a shuffled list of numbers in the empty cell
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        # recursive call to solve the next empty cell
                        if make_board(board):
                            return True;
                        # if current candidate didn't work, undo it
                        board[i][j] = 0
                # if no possible candidate worked in this cell, backtrack
                return False
    # if no empty cells remain, the board is solved
    return True

# determine if x,y is a valid position for num in board

def is_valid(board, x, y, num):
    # determine if num already exists in y-th column, excluding x,y
    for i in range(9):
        if i != x and board[i][y] == num:
            return False
    # determine if num already exist in the x-th row, excluding x,y
    for j in range(9):
        if j != y and board[x][j] == num:
            return False
    
    # determine index of the top left cell of the 3x3 square x,y is in
    box_x = (x // 3) * 3
    box_y = (y // 3) * 3
    # iterate through the 3x3 box to check for validity of num in x,y
    for row in range(3):
        for col in range(3):
            if board[box_x + row][box_y + col] == num:
                return False
    return True

# print the board to the console

def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end = " ")
        print()
    print()

if __name__ == "__main__":
    for _ in range(100):
        board = [[0 for _ in range(9)] for _ in range(9)]
        make_board(board)
        print_board(board)