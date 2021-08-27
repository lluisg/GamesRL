import numpy as np
# import pygame
import sys
import math

from Piece import Piece

class Board:
    def __init__(self, rows, cols):
        self.columns = cols
        self.rows = rows

        self.board = []

        for r in range(rows):
            self.board.append([])
            for c in range(cols):
                self.board[r].append(Piece())

    def get_board_values(self):
        b = []
        for r in range(self.rows):
            b.append([])
            for c in range(self.columns):
                b[r].append(self.board[r][c].get_piece())
        return b

    def get_position(self, row, col):
        return self.board[row][col]

    def set_specific_board(self, new_board):
        for ind_r, r in enumerate(new_board):
            for ind_c, c in enumerate(r):
                self.board[ind_r][ind_c].set_piece(c)

    def put_piece(self, row, col, value):
        self.board[row][col].set_piece(value)
