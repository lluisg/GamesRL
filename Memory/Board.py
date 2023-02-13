# -*- coding: utf-8 -*-

import numpy as np
# import pygame
import sys
import math

from Piece import Piece

class Board:
    def __init__(self, cols, rows):
        self.columns = cols
        self.rows = rows

        self.board = []

        for r in range(rows):
            self.board.append([])
            for c in range(cols):
                self.board[r].append(Piece())


    def getBoardValues(self):
        b = []
        for r in range(self.rows):
            b.append([])
            for c in range(self.columns):
                b[r].append(self.board[r][c].getValue())
        return b

    def getBoardValuesPlay(self):
        b = []
        for r in range(self.rows):
            b.append([])
            for c in range(self.columns):
                if not self.board[r][c].getFound():
                    if self.board[r][c].getVisible():
                        b[r].append(self.board[r][c].getValue())
                    else:
                        b[r].append('--')
                else:
                    b[r].append('xx')

        return b


    def getPosition(self, row, col):
        return self.board[row][col]


    def setSpecificBoard(self, new_board):
        for ind_r, r in enumerate(new_board):
            for ind_c, c in enumerate(r):
                self.board[ind_r][ind_c].setValue(c)


    def putPiece(self, row, col, piece):
        self.board[row][col].setValue(piece)

    def HideBoard(self):
        for ind_r, r in enumerate(self.board):
            for ind_c, c in enumerate(r):
                self.board[ind_r][ind_c].setVisible(False)

    def SetPieceVisible(self, row, col):
        self.board[row][col].setVisible(True)

