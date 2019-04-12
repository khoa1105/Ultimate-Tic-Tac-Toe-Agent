import numpy as np
from abc import ABC, abstractmethod
import os

class Player():
	def __init__(self):
		pass

	@abstractmethod
	def move(self, board, next_grid):
		pass

class RandomPlayer(Player):
	def __init__(self):
		pass

	def move(self, board, next_grid):
		move = np.random.randint(1,10)
		row = (move-1) // 3
		column = move - row*3 - 1

		while board[next_grid-1][row][column] != 0:
			move = np.random.randint(1,10)
			row = (move-1) // 3
			column = move - row*3 - 1

		return move



