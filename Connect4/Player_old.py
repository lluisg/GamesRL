import numpy as np
# import pygame
import sys
import math

from Piece import Piece

class Player:
    def __init__(self, player, b_control):
        self.player = player
        if player == 1:
            self.piece = Piece.RED
        elif player == 2:
            self.piece = Piece.YELLOW
        else:
            print('ONLY 2 POSSIBLE PLAYERS!!')

        self.b_controller = b_control

    def move(self):
        col = input("\nPlayer {} select column: ".format(self.player))

        while not self.check_column_input(col):
            if col.lower() == 'q':
                raise ValueError("Player {} left the match".format(self.player))

            col = input('Error, use a number between 1 and 7:')


        col = int(col)
        self.b_controller.drop_piece(col-1, self.player)

    def check_column_input(self, input):
        if input.isnumeric():
            if int(input) < 1:
                return False
            elif int(input) > 7:
                return False

        else:
            return False

        return True
