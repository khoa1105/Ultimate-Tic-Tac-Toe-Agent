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

	def no_space(self, board):
		for k in range(9):
			for i in range(3):
				for j in range(3):
					if board[k][i][j] == 0:
						return False
		return True

	def terminal(self, board):
		for k in range(9):
			victory = self.check_victory(board[k])
			if victory == 1:
				return 1
			elif victory == 2:
				return 2
		if self.no_space(board):
			return 3
		return 0

	def play(self):
		moves = [1,2,3,4,5,6,7,8,9]
		move = np.random.choice(moves, 1)
		row = (move[0]-1) // 3
		column = move[0] - row*3 - 1

		while self._board[self._next_grid-1][row][column] != 0:
			moves.remove(move[0])
			move = np.random.choice(moves, 1)
			row = (move[0]-1) // 3
			column = move[0] - row*3 - 1

		self._board[self._next_grid-1][row][column] = 1
		self._next_grid = move[0]

	def step(self, move):
		row = (move-1) // 3
		column = move - row*3 - 1
		
		#O moves
		#if illegal move
		if self._board[self._next_grid-1][row][column] == 1 or self._board[self._next_grid-1][row][column] == 2:
			reward = -100
			done = 1
			return self.getState(), reward, done
		else:
			self._board[self._next_grid-1][row][column] = 2
			self._next_grid = move

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 1:
			done = True
			reward = -10
			return self.getState(), reward, done
		elif terminal == 2:
			done = True
			reward = 10
			return self.getState(), reward, done
		elif terminal == 3:
			done = True
			reward = 0
			return self.getState(), reward, done
		
		#X move
		self.play()

		#Check for terminal state
		terminal = self.terminal(self._board)
		if terminal == 1:
			done = True
			reward = -10
		elif terminal == 2:
			done = True
			reward = 10
		elif terminal == 3:
			done = True
			reward = 0
		elif terminal == 0:
			done = False
			reward = 0
		return self.getState(), reward, done
