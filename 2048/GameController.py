from BoardController import BoardController
from Player import Player
from UIBoard import UIBoard

import pygame
from pygame.locals import *

import numpy as np

class GameController:
	def __init__(self, rows, cols):
		pygame.init()

		self.rows = rows
		self.columns = cols
		self.area = (600, 600)

		self.screen = pygame.display.set_mode(self.area)
		pygame.display.set_caption('2048')
		self.clock = pygame.time.Clock()
		self.clock.tick(30) # 60 FPS
		self.cooldown = 1000 #1s to wait when game ended

		self.b_controller = BoardController(self.rows, self.columns)
		self.ui = UIBoard(self.b_controller, self.area, pygame, self.screen)
		self.player = Player(self.b_controller, pygame, self.ui)


	def play(self):
		running = True
		ended = False

		self.reestart_game()

		moves = 0
		start = pygame.time.get_ticks()
		while running:
			if ended:
				moving = self.player.wait_to_reestart()
				if moving == False:
					running = False

				now = pygame.time.get_ticks()
				if now - start_wait >= self.cooldown:
					ended = False
					self.reestart_game()
					pygame.event.clear()
					start = 0

			else:

				now = pygame.time.get_ticks()
				time_playing = self.ticks2time(now - start)
				self.ui.set_time_moves(time_playing, moves)
				self.ui.print_base_screen()
				moving = self.player.move()
				if moving == True:
					print('next move')
					moves += 1
					self.ui.print_board_values()
					r, c = self.b_controller.appear_piece()
					self.ui.new_piece(r, c)
					if self.b_controller.check_winner():
						print('WINNER!')
						self.ui.print_win()
						start_wait = pygame.time.get_ticks()
						ended = True
					elif self.b_controller.check_nomoves():
						print('NO MORE MOVES')
						self.ui.print_loss()
						start_wait = pygame.time.get_ticks()
						ended = True

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

	def reestart_game(self):
		self.b_controller.reestart_board()
		self.ui.print_board_values()

		for _ in range(2):
			r, c = self.b_controller.appear_piece()
			self.ui.new_piece(r, c)

		# initial_board = np.array([  [1024,1024,512,4],
		# 							[4,0,2,4],
		# 							[2,4,2,4],
		# 							[4,2,4,2]])
		# self.b_controller.set_board(initial_board)
		# self.ui.print_board_values()
