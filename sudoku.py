from random import randrange as r

def print_mat(mat):
    result = '['
    for i in range(len(mat)):
        result += '['
        for j in range(len(mat[i])):
            if j != len(mat[i]) - 1:
                result += str(mat[i][j]) + ',\t'
            else:
                result += str(mat[i][j]) + ']'
        if i != len(mat) - 1:
            result += '\n '
        else:
            result += ']'
    print(result)

def reveal_hints(arr):
    reveals_in_row = r(1, 4)
    possible_reveals = [i for i in range(1, 10)]
    possible_spots = [i for i in range(9)]
    for j in range(reveals_in_row):
        reveal, spot = r(1, 10), r(9)
        while reveal not in possible_reveals:
            reveal = r(1, 10)
        while spot not in possible_spots:
            spot = r(9)
        possible_reveals.remove(reveal)
        possible_spots.remove(spot)
        arr.insert(spot, reveal)
        arr.pop()

def make_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(len(board)):
        reveal_hints(board[i])
    return board

def legal_board(s):
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == 0:
                continue
            for di in range(i):
                if s[di][j] == s[i][j]:
                    return False
            for di in range(i + 1, 9):
                if s[di][j] == s[i][j]:
                    return False
            for dj in range(j):
                if s[i][dj] == s[i][j]:
                    return False
            for dj in range(j + 1, 9):
                if s[i][dj] == s[i][j]:
                    return False
    for i in range(0, len(s), 3):
        for j in range(0, len(s[i]), 3):
            nums = {}
            for di in range(i, i + 3):
                for dj in range(j, j + 3):
                    if s[di][dj] == 0:
                        continue
                    if s[di][dj] not in nums.keys():
                        nums[s[di][dj]] = 1
                    else:
                        return False
    return True

def get_box_idxs(s):
    boxes = {}
    counter = 0
    for i in range(0, len(s), 3):
        for j in range(0, len(s[i]), 3):
            counter += 1
            boxes[counter] = []
            for di in range(3):
                for dj in range(3):
                    boxes[counter].append((i + di, j + dj))
    return boxes

def num_in_box(num, box, sudoku):
    for i, j in box:
        if sudoku[i][j] == num:
            return True
    return False

def place(num, box, idxs, sudoku):
    if num_in_box(num, idxs[box], sudoku):
        if box < 9:
            return place(num, box + 1, idxs, sudoku)
        elif num < 9:
            return place(num + 1, 1, idxs, sudoku)
        else:
            return True
    for i, j in idxs[box]:
        if sudoku[i][j] == 0:
            sudoku[i][j] = num
            if not legal_board(sudoku):
                sudoku[i][j] = 0
                continue
            if box < 9:
                if place(num, box + 1, idxs, sudoku):
                    return True
            elif num < 9:
                if place(num + 1, 1, idxs, sudoku):
                    return True
            else:
                return True
            sudoku[i][j] = 0
    return False

def sudoku_solver():
    while True:
        sudoku = make_sudoku()
        if legal_board(sudoku):
            print('Hints')
            print_mat(sudoku)
            print()
            break
    idxs = get_box_idxs(sudoku)
    if place(1, 1, idxs, sudoku):
        print('Solution:')
        print_mat(sudoku)
    else:
        print('No Solutions')

sudoku_solver()
