import numpy as np

from BoardController import BoardController
from Player import Player
from UIBoard import UIBoard

class Controller3Row:
	def __init__(self):

		self.rows = 3
		self.columns = 3

		self.b_controller = BoardController(self.rows, self.columns)
		self.ui = UIBoard(self.b_controller)
		self.player1 = Player(1, self.b_controller)
		self.player2 = Player(2, self.b_controller)

		self.turn = 0


	def play(self):
		end = False
		self.reestart_game()
		self.ui.print_board_values()

		moves = 0
		while not end and moves < 5:

			self.turn = self.turn % 2 +1

			if self.turn == 1:
				print 'Turn', moves, ': player 1'
				self.player1.play_turn()
				winner = self.b_controller.check_winner(self.player1.get_number())
			elif self.turn == 2:
				print 'Turn', moves, ': player 2'
				self.player2.play_turn()
				winner = self.b_controller.check_winner(self.player2.get_number())

			self.ui.print_board_values()
			if winner:
				if self.turn == 1:
					print 'Player 1 won!!'
				elif self.turn == 2:
					print 'Player 2 won!!'
				end = True
			else:
				draw = self.b_controller.check_nomoves()
				if draw:
					end = True
					print 'Draw!!'

			moves += 1


	def ticks2time(self, ticks):
		seconds = int((ticks/1000) % 60)
		minutes = int((ticks/(1000*60)) % 60)
		hours = int((ticks/(1000*60*60)) % 24)

		if hours > 0:
			return "{}:{}:{:02d}".format(hours, minutes, seconds)
		else:
			return "{}:{:02d}".format(minutes, seconds)

	def reestart_game(self):
		# self.b_controller.reestart_board()
		# initial_board = np.array([  [2,1,2],
		# 							[2,1,2],
		# 							[1,2,0]])
		self.b_controller.set_board(initial_board)

