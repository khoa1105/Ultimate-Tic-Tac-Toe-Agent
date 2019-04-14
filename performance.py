from keras.models import load_model
import time
import itertools
import numpy as np
from board import UltimateTicTacToe

#Use the neural net to estimate the Q values of each action
def Q_function_approximation(model, state):
	return model.predict(state, verbose=0)
	
#Epsilon greedy policy
def epsilon_greedy(model, nA, epsilon, state):
	A = np.ones(nA) * (epsilon/nA)
	bestA = np.argmax(Q_function_approximation(model, state))
	A[bestA] += (1-epsilon)
	action = np.random.choice(nA, p = A)
	return action

def performance(env, model, num_episodes = 100):
	print("Testing the agent for %d episodes!" % num_episodes)

	rewards = []
	for i in range(num_episodes):
		env.reset()
		state = env.getState()
		for t in itertools.count():
			state = np.asarray(state).reshape(1,82)
			Q_values = model.predict(state)
			legal_moves = env.legalMoves()
			for i in range(Q_values.shape[1]):
				if (i+1) not in legal_moves:
					Q_values[0][i] = -10
			action = np.argmax(Q_values)
			next_state, reward, done, illegal = env.step(action + 1)
			# if illegal:
			# 	raise ValueError("Illegal Move.")
			if done:
				rewards.append(reward)
				break
			state = next_state

	wins = 0
	draws = 0
	loses = 0
	for rw in rewards:
		if rw == 10:
			wins += 1
		elif rw == 0:
			draws += 1
		elif rw == -10:
			loses += 1
	print("Wins: %d  Draws: %d  Loses: %d" % (wins, draws, loses))

def show_games(env, model, num_episodes = 10):
	print("Showing episodes\n\n")

	for i in range(num_episodes):
		env.reset()
		state = env.getState()
		for t in itertools.count():
			state = np.asarray(state).reshape(1,82)
			Q_values = model.predict(state)
			legal_moves = env.legalMoves()
			for i in range(Q_values.shape[1]):
				if (i+1) not in legal_moves:
					Q_values[0][i] = -10
			action = np.argmax(Q_values)
			next_state, reward, done, illegal = env.step(action + 1)

			env.printBoard()
			print("Current Grid: %d" % env.getNextGrid())
			print("Legal moves:", end = " ")
			print(legal_moves)
			print("Move: %d" % (action + 1))
			time.sleep(30)
			if done:
				if reward == 10:
					print("You win!")
				elif reward == -10:
					print("You lost!")
				elif reward == 0:
					print("Draw!")
				else:
					raise ValueError("Invalid reward value")
				break

			state = next_state




env = UltimateTicTacToe()
model = load_model("TTTAgent.h5")

performance(env, model)
#show_games(env, model)