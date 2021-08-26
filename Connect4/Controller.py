import numpy as np
# import pygame
import sys
import math

from Board import Board
from BoardController import BoardController
from Piece import Piece
from Player import Player
from UIBoard import UIBoard
import logging
logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, rows, cols):
        self.rows = rows
        self.columns = cols
        self.turn = 0

    def play(self):
        print("To quit write 'q' when asked to move\n")
        b_controller = BoardController(self.rows, self.columns)
        ui = UIBoard(b_controller)
        player1 = Player(1, b_controller)
        player2 = Player(2, b_controller)

        # first print, when everything is still 0
        ui.print_board_values(True)

        # print after changing to our use case
        # B = np.array([  [0,0,1,0,0,0,0],
        #                 [1,0,0,0,0,2,0],
        #                 [0,0,1,0,0,0,1],
        #                 [0,0,0,2,0,1,0],
        #                 [0,0,0,0,1,0,0],
        #                 [0,0,0,1,0,1,0] ])
        #
        # b_controller.set_board(B)
        # ui.print_board_values(True)

        try:
            winner = False
            while winner == False:
                if self.turn % 2 == 0:
                    player1.move()
                    ui.print_board_values(True)
                    winner = b_controller.winning_move(1)
                else:
                    player2.move()
                    ui.print_board_values(True)
                    winner = b_controller.winning_move(2)

                self.turn += 1

            print("\nPLAYER {} WINS !!".format(winner))

        except ValueError as e:
            logger.error(e)
