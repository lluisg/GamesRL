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

class Game2048Env(gym.Env):
	"""
	Custom Environment to play 2048.
	"""
	metadata = {'render.modes': ['human', 'terminal']}
	# Define constants for clearer code
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3

	def __init__(self, rows, cols, reward, showing=False):
		super(Game2048Env, self).__init__()
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
			pygame.display.set_caption('2048')

			self.ui = UIBoard(self.b_controller, self.area, pygame, self.screen)
			self.ui.set_time_moves(self.time, self.moves)
		else:
			self.ui = []
		# --------------------------------------------------------------------------

		# Define action and observation space
		n_actions = 4
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(low=0, high=2048,
											shape=(self.rows*self.cols, ), dtype=np.float32)

		self.viewer = None
		self.list_moves = []
		self.list_states = []
		self.type_reward = reward
		self.video = []

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
		# self.ui.set_time_moves(self.time, self.moves)
		self.start = pygame.time.get_ticks()
		# self.ui.print_base_screen()

		for _ in range(2):
			r, c = self.b_controller.appear_piece()
			# self.ui.new_piece(r, c)

		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs

	def step(self, action):
		MAX_MOVES = 1000
		if action == self.LEFT:
				movements, merged = self.b_controller.move_left()
				self.list_moves.append('left')
		elif action == self.RIGHT:
				movements, merged = self.b_controller.move_right()
				self.list_moves.append('right')
		elif action == self.UP:
				movements, merged = self.b_controller.move_up()
				self.list_moves.append('up')
		elif action == self.DOWN:
				movements, merged = self.b_controller.move_down()
				self.list_moves.append('down')
		else:
			raise ValueError("Received invalid action={} which is not part of the action space".format(action))

		self.list_states.append(self.b_controller.get_board_values())

		now = pygame.time.get_ticks()
		self.time = self.ticks2time(now - self.start)
		# self.ui.set_time_moves(time_playing, self.moves)

		if movements != 0:
			# self.ui.print_base_screen()
			r, c = self.b_controller.appear_piece()
			# self.ui.new_piece(r, c)

		self.moves += 1

		# Optionally we can pass additional info, we are not using that for now
		info = {'finished':False, 'max_v':0, 'list_moves':self.list_moves, 'list_states':self.list_states, 'stopped':'idk', 'step':self.moves}

		if self.type_reward == 1:
			# REWARD: sum of values in screen - 1 per each move
			# if finished the score multiplied by 2, to try to reduce moves
			reward = self.b_controller.get_score() - 1*self.moves
			if self.b_controller.check_winner():
				reward *= 2

		elif self.type_reward == 2:
			# REWARD: sum of the maximum value on screen plus 1/10 of the sum of all the values
			# if the move is invalid a negative reward, if finished 5k of reward
			reward = 0.1*self.b_controller.get_score() + self.b_controller.get_max_value()
			if movements == 0:
				reward = -100
			if self.b_controller.check_winner():
				reward = 5000
			# print('r1', self.b_controller.get_board_values())
			# print('r2', self.b_controller.get_score(), self.b_controller.get_max_value(), reward)

		elif self.type_reward == 3:
			# REWARD: the value of the new merged values
			reward = merged

		elif self.type_reward == 4:
			# REWARD: the value of the new merged values, penalizing if invalid move
			reward = merged
			if movements == 0:
				reward = -100
			else:
				reward += 1

		elif self.type_reward == 5:
			# REWARD: the value of the new merged values plus extra if the max is in the left upper corner
			reward = merged
			maxx, maxy = self.b_controller.get_max_value_position()
			if maxx == 0 and maxy == 0:
				reward += self.b_controller.get_max_value()

			if movements == 0:
				reward = -100

		elif self.type_reward == 6:
			# REWARD: the value of the new merged values plus extra if the max is in the left upper corner
			# plus 3/4 max value if max values together
			reward = merged
			maxx, maxy = self.b_controller.get_max_value_position()
			max_v = self.b_controller.get_max_value()
			if maxx == 0 and maxy == 0:
				reward += max_v

			together = False
			if maxx > 0:
				if maxy > 0:
					if self.b_controller.get_score_position(maxx-1, maxy-1) == max_v:
						together = True
				elif maxy < self.rows-1:
					if self.b_controller.get_score_position(maxx-1, maxy+1) == max_v:
						together = True
			elif maxx < self.cols-1:
				if maxy > 0:
					if self.b_controller.get_score_position(maxx+1, maxy-1) == max_v:
						together = True
				elif maxy < self.rows-1:
					if self.b_controller.get_score_position(maxx-1, maxy+1) == max_v:
						together = True
			if together:
				reward += int(max_v*3/4)

			if movements == 0:
				reward = -100

		done = False
		# print(self.moves, self.b_controller.check_winner(), self.b_controller.check_nomoves())
		if self.b_controller.check_winner():
			info['finished'] = True
			info['stopped'] = 'Winner'
			done = True
		if self.b_controller.check_nomoves():
			info['stopped'] = 'No moves'
			done = True
		if self.moves >= MAX_MOVES:
			info['stopped'] = 'Max moves'
			done = True
		# if movements == 0:
		# 	info['stopped'] = 'Ilegal move'
		# 	done = True

		if done == True:
			info['max_v'] = self.b_controller.get_max_value()

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
