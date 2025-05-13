#sudoku_table_generator.py

import random

def make_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if make_board(board):
                            return True;
                        board[i][j] = 0
                return False
    return True

def is_valid(board, x, y, num):
    for i in range(9):
        if i != x and board[i][y] == num:
            return False
    for j in range(9):
        if j != y and board[x][j] == num:
            return False
        
    box_x = (x // 3) * 3
    box_y = (y // 3) * 3
    for row in range(3):
        for col in range(3):
            if board[box_x + row][box_y + col] == num:
                return False
    return True

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