import numpy as np

from BoardController import BoardController
from Player import Player

class BBTANController:
	def __init__(self):

		self.rows = 9
		self.columns = 7
		self.area = (600, 600)

		self.b_controller = BoardController(self.rows, self.columns)
		self.player = Player()


	def play(self):
		lost = False
		self.reestart_game()

		moves = 0
		while not lost:

			print 'Your turn'
			self.player.play_turn()
			self.b_controller.new_line()
			lost = self.b_controller.check_lost()

			self.print_board()
			moves += 1

		print 'You lost at level', self.b_controller.get_level(), '!'


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
		self.b_controller.new_line()

		# initial_board = np.array([  [1024,1024,512,4],
		# 							[4,0,2,4],
		# 							[2,4,2,4],
		# 							[4,2,4,2]])
		# self.b_controller.set_board(initial_board)

	def print_board(self):
		board = self.b_controller.get_board_values()
		print np.matrix(board)
