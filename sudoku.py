from random import randrange as r

class Puzzle:
    def __init__(self, random=True, min_row_hints=1, max_row_hints=3):
        if random:
            if max_row_hints > 9:
                max_row_hints = 5
            if min_row_hints > max_row_hints:
                min_row_hints = 5
            while True:
                self.board = self.make_random_board(min_row_hints, max_row_hints)
                if self.legal_board():
                    print('Hints:')
                    print(self)
                    print()
                    break
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self.hint_input()
            print('Hints:')
            print(self)
            print()

    def make_random_board(self, mnhs, mxhs):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(len(board)):
            reveals_in_row = r(mnhs, mxhs + 1)
            possible_reveals = [num for num in range(1, 10)]
            possible_spots   = [num for num in range(9)]
            for _ in range(reveals_in_row):
                reveal, spot = r(1, 10), r(9)
                while reveal not in possible_reveals:
                    reveal = r(1, 10)
                while spot not in possible_spots:
                    spot = r(9)
                possible_reveals.remove(reveal)
                possible_spots.remove(spot)
                board[i].insert(spot, reveal)
                board[i].pop()
        return board

    def legal_board(self):
        s = self.board
        for i in range(len(s)):
            for j in range(len(s[i])):
                num = s[i][j]
                if num != 0:
                    for di in range(len(s)):
                        if di != i:
                            if s[di][j] == num:
                                return False
                    for dj in range(len(s[i])):
                        if dj != j:
                            if s[i][dj] == num:
                                return False
        for i in range(0, len(s), 3):
            for j in range(0, len(s[i]), 3):
                nums = {}
                for di in range(i, i + 3):
                    for dj in range(j, j + 3):
                        if s[di][dj] != 0:
                            if s[di][dj] not in nums.keys():
                                nums[s[di][dj]] = 1
                            else:
                                return False
        return True

    def __str__(self):
        mat = self.board
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
        return result

    def hint_input(self):
        while True:
            try:
                hint = eval(input('Enter hint value (1-9), row number (1-9), and column number (1-9) comma separated (-1 to end): '))
                if hint == -1:
                    print()
                    break
                s, i, j = self.board, hint[1] - 1, hint[2] - 1
                s[i][j] = hint[0]
            except:
                exit = input('Invalid input. Try again (y/n)? ')
                if exit != 'y':
                    print()
                    break

class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.board = puzzle.board
        self.idxs = self.get_box_idxs()

    def get_box_idxs(self):
        boxes = {}
        counter = 0
        for i in range(0, len(self.board), 3):
            for j in range(0, len(self.board[i]), 3):
                counter += 1
                boxes[counter] = []
                for di in range(3):
                    for dj in range(3):
                        boxes[counter].append((i + di, j + dj))
        return boxes

    def num_in_box(self, num, box):
        for i, j in box:
            if self.board[i][j] == num:
                return True
        return False

    def place(self, num, box):
        if self.num_in_box(num, self.idxs[box]):
            if box < 9:
                return self.place(num, box + 1)
            elif num < 9:
                return self.place(num + 1, 1)
            else:
                return True
        for i, j in self.idxs[box]:
            if self.board[i][j] == 0:
                self.board[i][j] = num
                if not self.puzzle.legal_board():
                    self.board[i][j] = 0
                    continue
                if box < 9:
                    if self.place(num, box + 1):
                        return True
                elif num < 9:
                    if self.place(num + 1, 1):
                        return True
                else:
                    return True
                self.board[i][j] = 0
        return False

    def solve(self):
        print('Solution:')
        if self.place(1, 1):
            print(self.puzzle)
        else:
            print('Does Not Exist')

# def print_mat(mat):
#     result = '['
#     for i in range(len(mat)):
#         result += '['
#         for j in range(len(mat[i])):
#             if j != len(mat[i]) - 1:
#                 result += str(mat[i][j]) + ',\t'
#             else:
#                 result += str(mat[i][j]) + ']'
#         if i != len(mat) - 1:
#             result += '\n '
#         else:
#             result += ']'
#     print(result)
#
# def reveal_hints(arr):
#     reveals_in_row = r(1, 4)
#     possible_reveals = [i for i in range(1, 10)]
#     possible_spots = [i for i in range(9)]
#     for j in range(reveals_in_row):
#         reveal, spot = r(1, 10), r(9)
#         while reveal not in possible_reveals:
#             reveal = r(1, 10)
#         while spot not in possible_spots:
#             spot = r(9)
#         possible_reveals.remove(reveal)
#         possible_spots.remove(spot)
#         arr.insert(spot, reveal)
#         arr.pop()
#
# def make_sudoku():
#     board = [[0 for _ in range(9)] for _ in range(9)]
#     for i in range(len(board)):
#         reveal_hints(board[i])
#     return board
#
# def legal_board(s):
#     for i in range(len(s)):
#         for j in range(len(s[i])):
#             if s[i][j] == 0:
#                 continue
#             for di in range(i):
#                 if s[di][j] == s[i][j]:
#                     return False
#             for di in range(i + 1, 9):
#                 if s[di][j] == s[i][j]:
#                     return False
#             for dj in range(j):
#                 if s[i][dj] == s[i][j]:
#                     return False
#             for dj in range(j + 1, 9):
#                 if s[i][dj] == s[i][j]:
#                     return False
#     for i in range(0, len(s), 3):
#         for j in range(0, len(s[i]), 3):
#             nums = {}
#             for di in range(i, i + 3):
#                 for dj in range(j, j + 3):
#                     if s[di][dj] == 0:
#                         continue
#                     if s[di][dj] not in nums.keys():
#                         nums[s[di][dj]] = 1
#                     else:
#                         return False
#     return True
#
# def get_box_idxs(s):
#     boxes = {}
#     counter = 0
#     for i in range(0, len(s), 3):
#         for j in range(0, len(s[i]), 3):
#             counter += 1
#             boxes[counter] = []
#             for di in range(3):
#                 for dj in range(3):
#                     boxes[counter].append((i + di, j + dj))
#     return boxes
#
# def num_in_box(num, box, sudoku):
#     for i, j in box:
#         if sudoku[i][j] == num:
#             return True
#     return False
#
# def place(num, box, idxs, sudoku):
#     if num_in_box(num, idxs[box], sudoku):
#         if box < 9:
#             return place(num, box + 1, idxs, sudoku)
#         elif num < 9:
#             return place(num + 1, 1, idxs, sudoku)
#         else:
#             return True
#     for i, j in idxs[box]:
#         if sudoku[i][j] == 0:
#             sudoku[i][j] = num
#             if not legal_board(sudoku):
#                 sudoku[i][j] = 0
#                 continue
#             if box < 9:
#                 if place(num, box + 1, idxs, sudoku):
#                     return True
#             elif num < 9:
#                 if place(num + 1, 1, idxs, sudoku):
#                     return True
#             else:
#                 return True
#             sudoku[i][j] = 0
#     return False
#
# def sudoku_solver():
#     while True:
#         sudoku = make_sudoku()
#         if legal_board(sudoku):
#             print('Hints')
#             print_mat(sudoku)
#             print()
#             break
#     idxs = get_box_idxs(sudoku)
#     print()
#     if place(1, 1, idxs, sudoku):
#         print('Solution:')
#         print_mat(sudoku)
#     else:
#         print('No Solutions')

#sudoku_solver()

def main():
    s = Puzzle(random=True)
    t = SudokuSolver(s)
    t.solve()

if __name__ == '__main__': main()
