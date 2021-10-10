class Game3RowEnv(gym.Env):
	"""
	Custom Environment to play 3 in a row.
	"""
	metadata = {'render.modes': ['human', 'terminal']}

	def __init__(self, rows, cols, reward=1, vsAI = 1):
		super(Game3RowEnv, self).__init__()

		self.rows = rows
		self.cols = cols
		# Size of the 1Dgame grid
		self.grid_size = rows*cols
		self.moves = 0
		self.player = 1
		self.rival = 2

		self.b_controller = BoardController(self.rows, self.cols)
		self.ui = UIBoard(self.b_controller)

		# Define action and observation space
		n_actions = 9
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(low=0, high=2,
											shape=(self.rows*self.cols, ), dtype=np.float32)

		self.list_moves = []
		self.list_states = []
		self.type_reward = reward
		self.type_AI = vsAI
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

		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs

	def step(self, action):
		move_row = int(action/3)
		move_col = action % 3

		validmove = self.b_controller.put_piece(move_row, move_col, self.player)

		self.list_states.append(self.b_controller.get_board_values())
		self.list_moves.append(action)
		self.moves += 1

		# Optionally we can pass additional info, we are not using that for now
		info = {'finished':False, 'list_moves':self.list_moves, 'list_states':self.list_states, 'step':self.moves}

		if validmove:
			winner = self.b_controller.check_winner(self.player)
			draw = False
			if not winner: #if it hasn't win, check draw
				draw = self.b_controller.check_nomoves()


			if not draw and not winner: #if it hasn't win nor draw, move the rival
				self.moveAI()
				loser = self.b_controller.check_winner(self.rival)
				if not loser: #if the rival hasn't won, check draw
					draw = self.b_controller.check_nomoves()


		done = False
		if self.type_reward == 1 or self.type_reward == 2:
			# REWARD: 1 if win, -1 if loss, 0 rest, if invalid move -10
			if not validmove:
				reward = -10
				if self.type_reward == 1:
					info['finished'] = 'invalid'
					done = True
			elif winner:
				info['finished'] = 'win'
				reward = 1
				done = True
			elif draw:
				info['finished'] = 'draw'
				reward = 0
				done = True
			elif loser:
				info['finished'] = 'lose'
				reward = -1
				done = True
			else:
				reward = 0

			if self.type_reward == 2 and self.moves > 15:
				info['finished'] = 'invalid'
				done = True

		else:
			raise ValueError("Wrong reward value provided")

		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs, reward, done, info

	def moveAI(self):
		if self.type_AI == 0: # no movements (vs person)
			pass
		elif self.type_AI == 1:  # AI 1 = random AI
			self.move_randomAI()
		elif self.type_AI == 2:
			self.move_instantAI() # AI 2 = random AI + avoids/goes for automatic loses/wins
		else:
			print('Incorrect type AI')

	def move_randomAI(self):
		rivallvalidmove = False
		while not rivallvalidmove:
			action_rival = random.randint(1, 9)
			rival_row = int(action_rival / 3) -1
			rival_col = (action_rival % 3) -1
			rivallvalidmove = self.b_controller.put_piece(rival_row, rival_col, self.rival)

	def move_instantAI(self):
		r_move = None
		c_move = None
		# Checks to avoid losing
		for r in range(3):
			for c in range(3):
				controller_check = copy.deepcopy(self.b_controller)
				rivallvalidmove = controller_check.put_piece(r,c,1)
				if rivallvalidmove:
					if controller_check.check_winner(1):
						r_move, c_move = r,c
		# Checks to win (Priority)
		for r in range(3):
			for c in range(3):
				controller_check = copy.deepcopy(self.b_controller)
				rivallvalidmove = controller_check.put_piece(r,c,2)
				if rivallvalidmove:
					if controller_check.check_winner(2):
						r_move, c_move = r,c

		if r_move != None and c_move != None:
			rivallvalidmove = self.b_controller.put_piece(r_move, c_move, self.rival)
		else:
			self.move_randomAI()


	def get_video(self):
		return self.video

	def set_specific_table(self, table):
		self.b_controller.set_board(table)


	def render(self, mode='None', specific_table = False):

		if mode == 'human':
			self.ui.clear_terminal()
			self.ui.print_board_values()

		elif mode == 'terminal':
			self.ui.print_board_values()

		elif mode == 'colab':
			IPython.display.clear_output()
			b_values = self.b_controller.get_board_values()
			print(np.matrix(b_values))
			time.sleep(1.5)

		elif mode == 'None':
			pass

		else:
			raise NotImplementedError()

	def close(self):
		pass

	# for the vs player
	def return_board(self):
		obs = np.array(self.b_controller.get_board_values())
		flat_obs = obs.flatten(order='C')
		return flat_obs

	def player_move(self, position):
		position -= 1
		move_row = int(position / 3)
		move_col = (position % 3)
		print('move', move_row, move_col)
		validmove = self.b_controller.put_piece(move_row, move_col, self.rival)
		return validmove

	def check_winner(self):
		return self.b_controller.check_winner(self.rival)
	def check_draw(self):
		return self.b_controller.check_nomoves()
