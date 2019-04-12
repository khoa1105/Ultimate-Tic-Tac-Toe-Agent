from keras.models import load_model
from board import UltimateTicTacToe

model = load_model("TTTAgent.h5")
env = UltimateTicTacToe()

while True:
	env.printBoard()
	print("Next Grid: %d" % env.getNextGrid())
	print("Your Move:", end = " ")
	move = int(input())
	next_state, reward, done = env.step(move)
	if done == 1:
		break

print(reward)
