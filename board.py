import numpy as np

class UltimateTicTacToe():
	def __init__(self):
		self._board = np.zeros((9,3,3), dtype = "int8")
		self._next_grid = np.random.randint(1,10)
		self.play()

	def printBoard(self):
		for i in range(9):
			print("Grid %d" % (i+1))
			print(self._board[i])

	def legalMoves(self):
		legals = []
		for i in range(3):
			for j in range(3):
				if self._board[self._next_grid-1][i][j] == 0:
					legals.append(i * 3 + (j+1))
		return legals

	def getBoard(self):
		return self._board

	def getNextGrid(self):
		return self._next_grid

	def getState(self):
		state = []
		for k in range(9):
			for i in range(3):
				for j in range(3):
					state.append(self._board[k][i][j] / 2)
		state.append(self._next_grid / 9)
		return state

	def reset(self):
		self._board = np.zeros((9,3,3), dtype = "int8")
		self._next_grid = 0
		self.play()

	def check_victory(self, grid):
		#Check rows
		for i in range(3):
			count = {"1": 0, "2": 0}
			for j in range(3):
				if grid[i][j] == 1:
					count["1"] += 1
				elif grid[i][j] == 2:
					count["2"] += 1
			if count["1"] == 3:
				return 1
			elif count["2"] == 3:
				return 2

		#Check columns
		for i in range(3):
			count = {"1": 0, "2": 0}
			for j in range(3):
				if grid[j][i] == 1:
					count["1"] += 1
				elif grid[i][j] == 2:
					count["2"] += 1
			if count["1"] == 3:
				return 1
			elif count["2"] == 3:
				return 2

		#Check diagonals
		if (grid[0][0] == 1 and grid[1][1] == 1 and grid[2][2] == 1) or (grid[0][2] == 1 and grid[1][1] == 1 and grid[2][0] == 1):
			return 1
		if  (grid[0][0] == 2 and grid[1][1] == 2 and grid[2][2] == 2) or (grid[0][2] == 2 and grid[1][1] == 2 and grid[2][0] == 2):
			return 2

		return 0

	def no_space(self):
		for i in range(3):
			for j in range(3):
				if self._board[self._next_grid-1][i][j] == 0:
					return False
		return True

	def terminal(self, board):
		for k in range(9):
			victory = self.check_victory(board[k])
			if victory == 1:
				return 1
			elif victory == 2:
				return 2
		if self.no_space():
			return 3
		return 0

	def play(self):
		moves = self.legalMoves()
		move = np.random.choice(moves, 1)[0]

		row = (move-1) // 3
		column = move - row*3 - 1

		self._board[self._next_grid-1][row][column] = 1
		self._next_grid = move

	def step(self, move):
		row = (move-1) // 3
		column = move - row*3 - 1
		
		#O moves
		#if illegal, ignore and return the same state
		if move < 1 or move > 9 or self._board[self._next_grid-1][row][column] != 0:
			done = False
			reward = 0
			illegal = True
			return self.getState(), reward, done, illegal
		else:
			self._board[self._next_grid-1][row][column] = 2
			self._next_grid = move

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 1:
			done = True
			reward = -10
			illegal = False
			return self.getState(), reward, done, illegal
		elif terminal == 2:
			done = True
			reward = 10
			illegal = False
			return self.getState(), reward, done, illegal
		elif terminal == 3:
			done = True
			reward = 0
			illegal = False
			return self.getState(), reward, done, illegal
		
		#X move
		self.play()

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 0:
			done = False
			reward = 0
			illegal = False
		elif terminal == 1:
			done = True
			reward = -10
			illegal = False
		elif terminal == 2:
			done = True
			reward = 10
		elif terminal == 3:
			done = True
			reward = 0
			illegal = False

		return self.getState(), reward, done, illegal