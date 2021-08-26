import numpy as np
# import pygame
import sys
import math

from Piece import Piece

class BoardPiece:
    def __init__(self):
        self.piece = Piece.BLACK

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def get_piece_color(self):
        return self.piece.value
