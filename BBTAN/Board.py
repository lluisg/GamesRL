import random

from Piece import Piece

class Board:
    MONEY = -1
    RANDOM = -2
    LINE = -3
    COLUMN = -4

    def __init__(self, rows, cols):
        self.cols = cols #7
        self.rows = rows #9 first and last empty

        self.board = []
        for r in range(self.rows):
            self.board.append([])
            for c in range(self.cols):
                self.board[r].append(Piece())

    def get_board_values(self):
        b = []
        for r in range(self.rows):
            b.append([])
            for c in range(self.cols):
                b[r].append(self.board[r][c].get_value())
        return b

    def get_piece(self, row, col):
        return self.board[row][col]

    def put_piece(self, row, col, piece):
        self.board[row][col] = piece

    def put_piece_value(self, row, col, value):
        self.board[row][col].set_value(value)

    def remove_piece(self, row, col):
        self.board[row][col].value_remove()

    def decrease_piece(self, row, col):
        self.board[row][col].value_decrease()

    def remove_last_line(self):
        del self.board[-1]

    def add_line(self, level):

        newline = self.create_line(level)
        self.board[0] = [Piece(x) for x in newline]
        newzeros = self.create_line_zeros()
        self.board.insert(0, [Piece(x) for x in newzeros])

    def create_line(self, level):
        PROB_DOUBLE = 0.005 #probability appear a double block
        PROB_MAX_DOUBLE = 0.001 #probability appear a double block line
        PROB_NORMAL = 0.6 #probability appear a normal block
        PROB_SPECIAL = 0.05 / 3 #probability appear an special block
        REST = 1 - (PROB_DOUBLE+PROB_MAX_DOUBLE+PROB_NORMAL+PROB_SPECIAL)

        row = [-5 for _ in range(self.cols)]
        row[random.randint(0, self.cols-1)] = -1 #mandatory money slot
        for ind_c, c in enumerate(row) :
            if row[ind_c] == -5:
                # row[ind_c] = random.choices([-4, -3, -2, 0, level, level*2], [PROB_SPECIAL, PROB_SPECIAL, PROB_SPECIAL, REST, PROB_NORMAL, PROB_DOUBLE], k=1)
                row[ind_c] = random.choice([-4, -3, -2, 0, level, level * 2])
        return row

    def create_line_zeros(self):
        return [0 for _ in range(self.cols)]
