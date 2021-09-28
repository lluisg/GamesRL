import random

from Piece import Piece

class Board:
    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows

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
                b[r].append(self.board[r][c].get_player())
        return b

    def get_piece(self, row, col):
        return self.board[row][col]

    def put_piece(self, row, col, piece):
        self.board[row][col] = piece
