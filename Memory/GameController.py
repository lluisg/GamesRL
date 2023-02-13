# -*- coding: utf-8 -*-

import os
import numpy as np
from BoardController import BoardController
from Player import Player

class GameController(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.turn = -1
        self.num_turns = 0

        self.fichas = self.width * self.height

        self.board_contr = BoardController(self.width, self.height)

        # self.player1 = Player(1, self.board_contr, pygame, self.ui)
        self.player1 = Player(1, self.board_contr, False, False)
        # self.player2 = Player(2, self.board_contr, pygame, self.ui)
        self.player2 = Player(2, self.board_contr, False, False)

    def play(self):
        self.reestart_game()
        running = True
        ended = False
        while running:
            if ended:
                # moving = self.player1.wait_to_reestart()
                # if moving == False:
                #     running = False
                #
                # now = pygame.time.get_ticks()
                # if now - start_wait >= self.cooldown:
                #     ended = False
                #     self.reestart_game()
                #     pygame.event.clear()
                running = False
                pass

            else:
                print 'turn', self.turn, self.num_turns
                if (self.turn % 2) + 1 == 1:  # instead of [01] we use [12]
                    self.current_player = self.player1
                else:
                    self.current_player = self.player2

                print 'player:', self.current_player.getNumPlayer(), ',', self.current_player.getPoints(), 'points'
                print self.showBoardPlay()
                moving = self.current_player.move()

                if moving == True:
                    pair = self.board_contr.CheckFlipedSame()
                    if pair:
                        p = self.current_player.getPoints()
                        self.current_player.setPoints(p+1)
                        print 'You found a pair!'

                        # all_fliped = self.b_controller.check_allflipped()
                        # if all_fliped:
                        #     self.winner = self.whi_wins()

                    self.board_contr.HideBoard()

                    winner = self.CheckWinner()
                    if winner is not None:
                        if winner == 0:
                            print("\nWE HAVE A DRAW...")
                        else:
                            # print("\nPLAYER {} WINS !!".format(winner))
                            print("\nPLAYER "+str(winner)+" WINS !!")
                        ended = True

                    else:
                        self.next_turn(pair)


                    # self.ui.print_board_values(False)
                    # print('ended turn player {}\n'.format((self.turn % 2) + 1))
                    # winner = self.b_controller.check_winner((self.turn % 2) + 1)
                    # draw = self.b_controller.check_draw()
                    # if winner:
                    #     print("\nPLAYER {} WINS !!".format(winner))
                    #     self.ui.print_winner((self.turn % 2) + 1)
                    #     start_wait = pygame.time.get_ticks()
                    #     ended = True
                    # elif draw:
                    #     print("\nDRAW...".format(winner))
                    #     self.ui.print_draw()
                    #     start_wait = pygame.time.get_ticks()
                    #     ended = True
                    # else:
                    #     self.next_turn()
                elif moving == False:
                    running = moving

    def reestart_game(self):
        self.board_contr.ReestartBoard()

        # initial_board = np.array([[0, 0, 1],
        #                           [1, 2, 2],
        #                           [3, 3, 4],
        #                           [4, 5, 5]])
        initial_board = np.array([[0, 0]])
        self.board_contr.setSpecificBoard(initial_board)
        print self.board_contr.ReturnValues()

        self.turn = -1
        self.next_turn()

    def next_turn(self, pair=False ):
        if pair:
            print 'Repeat Turn'
        else:
            self.turn += 1
            print 'Next Turn'

        self.num_turns += 1
        # self.ui.print_player_screen((self.turn % 2) + 1, 3)



    def showBoard(self):
        board_values = self.board_contr.ReturnValues()
        return board_values

    def showBoardPlay(self):
        board_values = self.board_contr.ReturnValuesPlay()
        return board_values

    def CheckWinner(self):
        finished = self.board_contr.CheckFinished()
        if finished:
            if self.player1.getPoints() > self.player2.getPoints():
                return 1
            elif self.player1.getPoints() < self.player2.getPoints():
                return 2
            else:
                return 0

        return None





    def RollPosition(self, row, col):
        if row > self.height-1 or col > self.width-1:
            print 'invalid position:', row,  col

        else:
            self.board_contr.ShowPiece(row, col)
