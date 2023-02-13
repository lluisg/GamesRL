# -*- coding: utf-8 -*-

import os
import random
import numpy as np
from Piece import Piece
from Board import Board

class BoardController(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.num_fichas = self.width * self.height
        self.ReestartBoard()

    def GetRowCols(self):
        return self.height, self.width


    def ReestartBoard(self):
        self.board = Board(self.width, self.height)
        fichas = self.PrepareValueFichas()
        self.board.setSpecificBoard(fichas)

    def setSpecificBoard(self, fichas):
        self.board.setSpecificBoard(fichas)

    def PrepareValueFichas(self):
        lista_fichas = [x % (self.num_fichas / 2) for x in range(self.num_fichas)]
        random.shuffle(lista_fichas)

        board_fichas = [lista_fichas[i:i + self.width] for i in range(0, len(lista_fichas), self.width)]
        return board_fichas

    def ReturnValues(self):
        return self.board.getBoardValues()

    def ReturnValuesPlay(self):
        return self.board.getBoardValuesPlay()

    def FlipPosition(self, row, col):
        try:
            pos = self.board.getPosition(row, col)
        except:
            return 'pos'

        if pos.getFound():
            return 'found'
        elif pos.getVisible():
            return 'visible'

        self.board.SetPieceVisible(row, col)
        val = self.board.getPosition(row, col)
        return val.getValue()

    def CheckFlipedSame(self):
        visibles = []
        for r in range(self.height):
            for c in range(self.width):
                if self.board.getPosition(r, c).getVisible():
                    visibles.append(self.board.getPosition(r, c))

        if len(visibles) != 2:
            print 'ayaya error'
        else:
            if visibles[0].getValue() == visibles[1].getValue():
                visibles[0].setFound(True)
                visibles[1].setFound(True)
                return True
            else:
                return False


    def HideBoard(self):
        self.board.HideBoard()

    def CheckFinished(self):

        for r in range(self.height):
            for c in range(self.width):
                if not self.board.getPosition(r, c).getFound():
                    return False
        return True

