from keras.models import load_model
from board import UltimateTicTacToe
import numpy as np
import time

#model = load_model("TTTAgent.h5")
env = UltimateTicTacToe()

while True:
	env.printBoard()
	print("Next Grid: %d" % env.getNextGrid())
	print("Your Move:", end = " ")
	action = int(input())
	next_state, reward, done, illegal = env.step(action)
	if done == 1:
		break

if reward == 10:
	print("You win!")
elif reward == -10:
	print("You lost!")
elif reward == -100:
	print("Illegal Move")
else:
	print("Draw")
