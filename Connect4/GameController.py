import numpy as np
# import pygame
import sys
import math

from BoardController import BoardController
from Player import Player
from UIBoard import UIBoard

import pygame
from pygame.locals import *
pygame.init()


class GameController:
	def __init__(self):
		self.rows = 6
		self.columns = 7
		self.area = (700, 600)
		self.turn = -1

		self.screen = pygame.display.set_mode(self.area)
		pygame.display.set_caption('Box Test')
		self.clock = pygame.time.Clock()
		self.clock.tick(60) # 60 FPS
		self.cooldown = 1000

		self.b_controller = BoardController(self.rows, self.columns)
		self.ui = UIBoard(self.b_controller, self.area, pygame, self.screen)
		self.player1 = Player(1, self.b_controller, pygame, self.ui)
		self.player2 = Player(2, self.b_controller, pygame, self.ui)


	def play(self):
		self.reestart_game()
		running = True
		ended = False
		while running:

			if ended:
				moving = self.player1.wait_to_reestart()
				if moving == False:
					running = False

				now = pygame.time.get_ticks()
				if now - start_wait >= self.cooldown:
					ended = False
					self.reestart_game()
					pygame.event.clear()

			else:
				if (self.turn % 2)+1 == 1: #instead of [01] we use [12]
					moving = self.player1.move()
				else:
					moving = self.player2.move()

				if moving == True:
					self.ui.print_board_values(False)
					print('ended turn player {}\n'.format((self.turn % 2)+1))
					winner = self.b_controller.check_winner((self.turn % 2)+1)
					draw = self.b_controller.check_draw()
					if winner:
						print("\nPLAYER {} WINS !!".format(winner))
						self.ui.print_winner((self.turn % 2)+1)
						start_wait = pygame.time.get_ticks()
						ended = True
					elif draw:
						print("\nDRAW...".format(winner))
						self.ui.print_draw()
						start_wait = pygame.time.get_ticks()
						ended = True
					else:
						self.next_turn()
				elif moving == False:
					running = moving

		pygame.quit()

	def next_turn(self):
		self.turn += 1
		self.ui.print_player_screen((self.turn % 2)+1, 0)

	def reestart_game(self):
		initial_board = np.array([  [0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0] ])

		initial_board = np.array([  [0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,0,0,0,0,0,0],
									[0,2,2,2,0,0,0],
									[0,1,1,1,0,0,0] ])

		self.b_controller.set_board(initial_board)
		self.turn = -1
		self.next_turn()
