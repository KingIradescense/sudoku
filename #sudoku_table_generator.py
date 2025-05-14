#sudoku_table_generator.py

import random

# difficulty ranges for games

difficulty_clue_ranges = {
    "very easy": (40, 50),
    "easy": (36, 39),
    "medium": (32, 35),
    "hard": (28, 31),
    "extreme": (17, 27)
}

# determine the number of clues a board will have from the difficulty ranges

def get_target_clue_count(difficulty):
    low, high = difficulty_clue_ranges[difficulty]
    return random.randint(low, high)

# create starting puzzle from given board

def make_puzzle(board, num):
    # generate and then randomize the list of all coodinates in the board
    coords = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(coords)

    permanent_removed = [] 
    temp_failed = []
    num_removed = 0

    retry_cycles = 0
    max_retry_cycles = 3
    # iterate through each coord, attempting to remove and determining if it increases the number of solutions
    for i, j in coords:
        if num_removed >= num:
            print(f"All intended cells removed")
            break
        # debug print
        print(f"Removed so far: {len(permanent_removed)} / {num}")

        saved = try_remove_cell(board, i, j)

        # if this cell can be successfully removed, do so
        if count_solutions(board) == 1:
            permanent_removed.append((i, j))
            # rebuild remaining possible coords for next pass through
            #? make permanent_removed a set for O(1) lookup time? but order may be needed later for hints system. revisit
            coords = [(i, j) for i in range(9) for j in range(9) if (i, j) not in permanent_removed]
            random.shuffle(coords)
            temp_failed = []
            num_removed += 1
            retry_cycles = 0
            print(f"Removed: ({i}, {j}) - total: {len(permanent_removed)} / {num}")
        # if this cell cannot be successfully removed, put the value back
        else:
            board[i][j] = saved
            # keep track of non-candidate cells until next successful candidate found
            temp_failed.append((i, j))

            # if we have failed to remove anything recently, stall out and reset temp_failed values, to avoid coords exhausting preemptively
            if len(temp_failed) >= len(coords):
                retry_cycles += 1
                if(retry_cycles > max_retry_cycles):
                    print(f"Gave up after too many retry loops")
                    print(f"Final failed coords:", temp_failed)
                    break
                print(f"Stalling out- resetting temp_failed")
                coords += temp_failed[:]
                temp_failed = []
                random.shuffle(coords)
    
    return board

# helper function for make_puzzle- wraps change state

def try_remove_cell(board, i, j):
    saved = board[i][j]
    board[i][j] = 0
    return saved

# check number of possible solutions for different phases of puzzle in make_puzzle

def count_solutions(board):
    count = 0

    def solve(b):
        nonlocal count
        # if there is more than one solution, terminate
        if count > 1:
            return
        
        # basically, explore all valid first moves and recursively go down all paths from those
        for i in range(9):
            for j in range(9):
                if b[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(b, i, j, num):
                            b[i][j] = num
                            solve(b)
                            b[i][j] = 0
                    # only go one layer deep per empty cell into recursion
                    return
        # if the board is filled, it is +one valid solution
        count += 1

    # use a copy so we don't mutate the original
    solve([row[:] for row in board])
    return count

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
            if (box_x + row, box_y + col) != (x, y) and board[box_x + row][box_y + col] == num:
                return False
    return True

#check if full board is valid

def is_board_valid(board):
    for i in range(9):
        for j in range(9):
            # check for lingering zeros
            if board[i][j] == 0:
                print(f"Zero found at ({i}, {j})")
                return False
            # check if number in cell is valid for row/column/3x3
            elif not is_valid(board, i, j, board[i][j]):
                print(f"Invalid placement at ({i}, {j}) with {board[i][j]}")
                return False
    # board is valid
    print(f"Board has valid configuration")
    print()
    return True

# print the board to the console

def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end = " ")
        print()
    print()

if __name__ == "__main__":
    solution = [[0 for _ in range(9)] for _ in range(9)]
    make_board(solution)
    print_board(solution)
    is_board_valid(solution)
    target_clues = get_target_clue_count("very easy")
    cells_to_remove = 81 - target_clues
    puzzle = make_puzzle(solution, cells_to_remove)
    print_board(puzzle)