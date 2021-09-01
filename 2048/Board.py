import numpy as np
# import pygame
import sys
import math

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

    def get_empty_pos(self):
        empty_r = []
        empty_c = []

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].get_value() == 0:
                    empty_r.append(r)
                    empty_c.append(c)

        return empty_r, empty_c

    def move_piece(self, old_r, old_c, new_r, new_c):

        piece_o = self.get_piece(old_r, old_c)
        piece_d = self.get_piece(new_r, new_c)

        if piece_o.get_value() == 0:
            raise ValueError('Old position ({}, {}) empty!'.format(old_r, old_c))
        if piece_d.get_value() != 0:
            raise ValueError('New position ({}, {}) already ocupied!'.format(new_r, new_c))

        self.put_piece(new_r, new_c, piece_o)
        self.put_piece(old_r, old_c, Piece())

    def merge_pieces(self, row1, col1, row2, col2):
        self.board[row1][col1].value_upgrade()
        self.remove_piece(row2, col2)
        return self.board[row1][col1].get_value()
