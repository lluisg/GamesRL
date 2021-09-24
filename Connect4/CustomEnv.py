import numpy as np
import time
import cv2
import gym
from gym import spaces
from gym.envs.classic_control import rendering

import pygame
from pygame.locals import *

from BoardController import BoardController
from UIBoard import UIBoard
from MachinePlayer import MPlayer

class GameConnect4Env(gym.Env):
	"""
	Custom Environment to play 2048.
	"""
	metadata = {'render.modes': ['human', 'terminal']}
	# Define constants for clearer code

	def __init__(self, rows=6, cols=7, reward=1, showing=False):
		super(GameConnect4Env, self).__init__()
		pygame.init()

		self.rows = rows
		self.cols = cols
		# Size of the 1Dgame grid
		self.grid_size = rows*cols
		self.moves = 0
		self.time = '0:00'

		self.b_controller = BoardController(self.rows, self.cols)

		# PRINTING PARAMETERS ------------------------------------------------------
		self.area = (600, 600)

		self.clock = pygame.time.Clock()
		self.clock.tick(30) # 30 FPS

		if showing:
			self.screen = pygame.display.set_mode(self.area)
			pygame.display.set_caption('Connect4')

			self.ui = UIBoard(self.b_controller, self.area, pygame, self.screen)
			self.ui.set_time_moves(self.time, self.moves)
		else:
			self.ui = []
		# --------------------------------------------------------------------------

		# Define action and observation space
		n_actions = 7
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(low=0, high=2,
											shape=(self.rows*self.cols, ), dtype=np.float32)

		self.list_moves = []
		self.list_states = []
		self.type_reward = reward
		self.video = []

		self.rival = MPlayer()
		self.player = 1
		self.player2 = 2

	def reset(self):
		"""
		Important: the observation must be a numpy array
		:return: (np.array)
		"""
		self.b_controller.reestart_board()

		self.list_moves = []
		self.list_states = []

		self.moves = 0
		self.time = '0:00'

		self.start = pygame.time.get_ticks()

		self.b_controller.reestart_board()
		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs

	def step(self, action):

		# self.ui.print_drop_piece(self.player, action)
		self.b_controller.drop_piece(action, self.player)
		# self.list_moves.append(str(action))
		# self.list_states.append(self.b_controller.get_board_values())

		winner = self.b_controller.check_winner(self.player)
		draw = self.b_controller.check_draw()
		print('move:', action)

		if not winner and not draw:
			move_rival = self.rival.select_move_random()
			self.b_controller.drop_piece(move_rival, self.player2)
			print('move_rival:', move_rival)

			loser = self.b_controller.check_winner(self.player2)
			draw = self.b_controller.check_draw()


		if self.type_reward == 1:
			done = True
			if winner:
				reward = float(10)
			elif draw:
				reward = float(1)
			elif loser:
				reward = float(-10)
			else:
				reward = 1.0/42.0
				done = False

		now = pygame.time.get_ticks()
		self.time = self.ticks2time(now - self.start)
		self.moves += 1

		# Optionally we can pass additional info, we are not using that for now
		info = {'finished':done, 'list_moves':self.list_moves, 'list_states':self.list_states, 'stopped':'idk', 'step':self.moves}

		if winner:
			info['stopped'] = 'Winner'
		elif loser:
			info['stopped'] = 'Loser'
		elif draw:
			info['stopped'] = 'Draw'

		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs, reward, done, info

	def get_video(self):
		return self.video

	def get_state(self):
		state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
			pygame.display.get_surface()).astype(np.uint8))))
		return state

	def set_specific_table(self, table):
		self.b_controller.set_board(table)


	def render(self, mode='None', specific_table = False):

		if mode == 'human':
			self.ui.set_time_moves(self.time, self.moves)
			self.ui.print_base_screen()
			pygame.time.wait(400)

		elif mode == 'colab':
			self.ui.set_time_moves(self.time, self.moves)
			self.ui.print_base_screen()
			#convert image so it can be displayed in OpenCV
			view = pygame.surfarray.array3d(self.screen)
			#  convert from (width, height, channel) to (height, width, channel)
			view = view.transpose([1, 0, 2])
			#  convert from rgb to bgr
			img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
			#Display image, clear cell every 0.5 seconds
			cv2_imshow(img_bgr)
			pygame.time.wait(400)
			output.clear()

		elif mode == 'video':
			self.ui.set_time_moves(self.time, self.moves)
			self.ui.print_base_screen()
			#convert image so it can be displayed in OpenCV
			view = pygame.surfarray.array3d(self.screen)
			#  convert from (width, height, channel) to (height, width, channel)
			view = view.transpose([1, 0, 2])
			#  convert from rgb to bgr
			img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
			#Display image, clear cell every 0.5 seconds
			self.video.append(img_bgr)
			# cv2_imshow(img_bgr)
			# pygame.time.wait(100)
			# output.clear()

		elif mode == 'terminal':
			b_values = self.b_controller.get_board_values()
			print(np.matrix(b_values))

		elif mode == 'None':
			pass

		else:
			raise NotImplementedError()

	def close(self):
		pass

	def print(self):
		self.ui.print_base_screen()
		pygame.time.wait(100)

	def ticks2time(self, ticks):
		seconds = int((ticks/1000) % 60)
		minutes = int((ticks/(1000*60)) % 60)
		hours = int((ticks/(1000*60*60)) % 24)

		if hours > 0:
			return "{}:{}:{:02d}".format(hours, minutes, seconds)
		else:
			return "{}:{:02d}".format(minutes, seconds)
