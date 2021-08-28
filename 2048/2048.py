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
		self.rows = 4
		self.columns = 4
		self.area = (600, 600)

		self.screen = pygame.display.set_mode(self.area)
		pygame.display.set_caption('2048')
		self.clock = pygame.time.Clock()
		self.clock.tick(30) # 60 FPS

		self.b_controller = BoardController(self.rows, self.columns)
		self.ui = UIBoard(self.b_controller, self.area, pygame, self.screen)
		self.player = Player(self.b_controller, pygame, self.ui)


	def play(self):
		running = True
		# self.ui.print_board_values()

		# initial_board = np.array([  [0,  2,  4,   8],
		# 							[16, 32, 64,  128],
		# 							[256,512,1024,2048],
		# 							[0,  0,  0,   0]])
		# initial_board = np.array([  [0,2,2,0],
		# 							[2,0,0,2],
		# 							[2,4,4,4],
		# 							[16,0,16,8]])
		# self.b_controller.set_board(initial_board)
		# self.ui.print_board_values()

		self.b_controller.reestart_board()
		self.ui.print_board_values()
		for _ in range(2):
			r, c = self.b_controller.appear_piece()
			self.ui.new_piece(r, c)

		moves = 0
		start = pygame.time.get_ticks()
		while running:
				now = pygame.time.get_ticks()
				time_playing = self.ticks2time(now - start)
				self.ui.print_base_screen(time_playing, moves)
				moving = self.player.move()
				if moving == True:
					print('next move')
					moves += 1
					self.ui.print_board_values()
					r, c = self.b_controller.appear_piece()
					self.ui.new_piece(r, c)
					if self.b_controller.no_moves():
						print('NO MORE MOVES')
						running = False
				elif moving == False:
					running = False


	def ticks2time(self, ticks):
		seconds = int((ticks/1000) % 60)
		minutes = int((ticks/(1000*60)) % 60)
		hours = int((ticks/(1000*60*60)) % 24)

		if hours > 0:
			return "{}:{}:{:02d}".format(hours, minutes, seconds)
		else:
			return "{}:{:02d}".format(minutes, seconds)


	# 	self.reestart_game()
	# 	running = True
	# 	ended = False
	# 	while running:
	#
	# 		if ended:
	# 			moving = self.player1.wait_to_reestart()
	# 			if moving == False:
	# 				running = False
	#
	# 			now = pygame.time.get_ticks()
	# 			if now - start_wait >= self.cooldown:
	# 				ended = False
	# 				self.reestart_game()
	# 				pygame.event.clear()
	#
	# 		else:
	# 			if (self.turn % 2)+1 == 1: #instead of [01] we use [12]
	# 				moving = self.player1.move()
	# 			else:
	# 				moving = self.player2.move()
	#
	# 			if moving == True:
	# 				self.ui.print_board_values(False)
	# 				print('ended turn player {}\n'.format((self.turn % 2)+1))
	# 				winner = self.b_controller.check_winner((self.turn % 2)+1)
	# 				draw = self.b_controller.check_draw()
	# 				if winner:
	# 					print("\nPLAYER {} WINS !!".format(winner))
	# 					self.ui.print_winner((self.turn % 2)+1)
	# 					start_wait = pygame.time.get_ticks()
	# 					ended = True
	# 				elif draw:
	# 					print("\nDRAW...".format(winner))
	# 					self.ui.print_draw()
	# 					start_wait = pygame.time.get_ticks()
	# 					ended = True
	# 				else:
	# 					self.next_turn()
	# 			elif moving == False:
	# 				running = moving
	#
	# 	pygame.quit()
	#
	# def next_turn(self):
	# 	self.turn += 1
	# 	self.ui.print_player_screen((self.turn % 2)+1, 3)
	#
	# def reestart_game(self):
	# 	initial_board = np.array([  [0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0] ])
	#
	# 	initial_board = np.array([  [0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,0,0,0,0,0,0],
	# 								[0,2,2,2,0,0,0],
	# 								[0,1,1,1,0,0,0] ])
	#
	# 	self.b_controller.set_board(initial_board)
	# 	self.turn = -1
	# 	self.next_turn()


c = GameController()
c.play()
