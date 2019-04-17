import numpy as np
from keras.models import load_model

class UltimateTicTacToe():
	def __init__(self):
		self._board = np.zeros((9,3,3), dtype = "int8")
		self._next_grid = np.random.randint(1,10)
		self._model = load_model("TTTv1.h5")
		#self.play(self.getState())

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
		#self.play(self.getState())

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

	def play(self,state):
		state = np.asarray(state).reshape(1,82)
		Q_values = self._model.predict(state)
		moves = self.legalMoves()
		probabilities = []

		#mask illegal moves Q values to -100 
		for i in range(Q_values.shape[1]):
			if (i+1) not in moves:
				Q_values[0][i] = -100
		#epsilon greedy
		for i in range(Q_values.shape[1]):
			if (i+1) in moves:
				probabilities.append(0.2/len(moves))
			else:
				probabilities.append(0)

		probabilities[np.argmax(Q_values)] += 0.8

		action = np.random.choice(Q_values.shape[1], p=probabilities)
		move = action + 1

		row = (move-1) // 3
		column = move - row*3 - 1

		if move < 1 or move > 9 or self._board[self._next_grid-1][row][column] != 0:
			raise ValueError("Illegal Bot")
		self._board[self._next_grid-1][row][column] = 2
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
			self._board[self._next_grid-1][row][column] = 1
			self._next_grid = move

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 1:
			done = True
			reward = 10
			illegal = False
			return self.getState(), reward, done, illegal
		elif terminal == 2:
			done = True
			reward = -10
			illegal = False
			return self.getState(), reward, done, illegal
		elif terminal == 3:
			done = True
			reward = 0
			illegal = False
			return self.getState(), reward, done, illegal
		
		#X move
		self.play(self.getState())

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 0:
			done = False
			reward = 0
			illegal = False
		elif terminal == 1:
			done = True
			reward = 10
			illegal = False
		elif terminal == 2:
			done = True
			reward = -10
			illegal = False
		elif terminal == 3:
			done = True
			reward = 0
			illegal = False

		return self.getState(), reward, done, illegal