import numpy as np
from board import UltimateTicTacToe
from player import RandomPlayer
import time
import itertools
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import Adam
import os

#Neural net architecture
def init_model():
	model = Sequential()
	model.add(Dense(512, activation="relu", input_dim = 82))
	model.add(Dense(9, activation="linear"))
	model.compile(loss="mse", optimizer=Adam(lr=0.001))
	return model

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

#Function to get the nth root of number n
def nth_root(num, n):
	return (n ** (1/num))

#Function to train the model from experience
def train_model(model, gamma, action_space, experiences):
	#Get information from experience memory
	exp_state = experiences[0][0]
	exp_action = experiences[0][1]
	exp_reward = experiences[0][2]
	exp_done = experiences[0][3]
	exp_next_state = experiences[0][4]
	for i in range(1, len(experiences)):
		exp_state = np.vstack((exp_state, experiences[i][0]))
		exp_action = np.vstack((exp_action, experiences[i][1]))
		exp_reward = np.vstack((exp_reward, experiences[i][2]))
		exp_done = np.vstack((exp_done, experiences[i][3]))
		exp_next_state = np.vstack((exp_next_state, experiences[i][4]))
	#Predict the Q values
	predicted_Qs = Q_function_approximation(model, exp_state)
	#TD target
	max_Qs_next_state = np.amax(Q_function_approximation(model, exp_next_state), axis=1)
	max_Qs_next_state = max_Qs_next_state.reshape((len(max_Qs_next_state), 1))
	updated_Q = exp_reward + gamma * max_Qs_next_state
	#If the next state is terminal, TD target is the reward
	for i in range(len(experiences)):
		if exp_reward[i] == 10:
			updated_Q[i] = 10
		elif exp_reward[i] == -10:
			updated_Q[i] = -10
	#Labels for traning
	labels = np.copy(predicted_Qs)
	for i in range(labels.shape[0]):
		labels[i][exp_action[i]] = updated_Q[i]

	# for i in range(len(experiences)):
	# 	if exp_reward[i] == 10:
	# 		print(f"{predicted_Qs[i]} {exp_reward[i]} {max_Qs_next_state[i]} {updated_Q[i]} {exp_action[i]} {labels[i]}")
	# 		time.sleep(2)
	#Fit the model
	model.fit(exp_state, labels, batch_size = 32, epochs = 2, verbose = 1)
	print("\n")


def DeepQLearning(env, num_episodes, gamma=0.99, initial_epsilon=1, final_epsilon=0.01):
	#Find epsilon decay rate to get final_epsilon
	epsilon_decay = nth_root(num_episodes, final_epsilon/initial_epsilon)
	#Initilize experience and reward memory
	experiences = []
	rewards = []
	#Initialize model
	if os.path.isfile("TTTAgent.h5") and os.path.isfile("TTTEpisodes.txt"):
		model = load_model("TTTAgent.h5")
		file = open("TTTEpisodes.txt", "r")
		data = file.read()
		start_episode = int(data)
		file.close()
		print("Found a model.")
	else:
		model = init_model()
		start_episode = 1
		print("No pre-trained model found")
	print("Start Training At Episode %d!" % start_episode)
	#Start Training
	for i in range(start_episode, episodes+1):
		#Decay epsilon
		epsilon = initial_epsilon * (epsilon_decay ** i)

		#For every 1k episodes, calculate the avg reward and train the model
		if i % 1000 == 0:
			#Caculating
			if len(rewards) != 0:
				total_reward = 0
				wins = 0
				draws = 0
				loses = 0
				for rw in rewards:
					total_reward += rw
					if rw == 10:
						wins += 1
					elif rw == 0:
						draws += 1
					elif rw == -10:
						loses += 1
				avg_reward = (total_reward * 1.0) / len(rewards)   
				#Save reward
				file = open("TTTReward.txt", "w")
				file.write(str(avg_reward))
				file.close()
				#Print messages
				print("Episode %d/%d\nAvg reward last 1000 episodes: %.3f\nCurrent Exp Memory Size: %d\nEpsilon: %.3f" % (i, num_episodes, avg_reward, len(experiences), epsilon))
				print("Wins: %d  Draws: %d  Loses: %d" % (wins, draws, loses))
				rewards.clear()
			#Train the model
			if len(experiences) != 0:
				train_model(model,gamma, 9, experiences)
				#Clear the experiences
				experiences.clear()
		#For every 10k episodes, save the model
		if i % 10000 == 0 and i != start_episode:
			model.save("TTTAgent.h5")
			file = open("TTTEpisodes.txt", "w")
			file.write(str(i))
			file.close()
			print("Model Saved!")
		#Reset game
		env.reset()
		state = env.getState()
		
		#Generate episode
		for t in itertools.count():
			state = np.asarray(state).reshape(1,len(state))
			#Pick an action according to epsilon greedy
			action = epsilon_greedy(model, 9 , epsilon, state)
			next_state, reward, done, illegal = env.step(action + 1)
			#Save experience in experience memory
			if not illegal:
				experiences.append([state, action, reward, done, next_state])
			if done:
				rewards.append(reward)
				break
			#Move to next state
			state = next_state


env = UltimateTicTacToe()
player = init_model()
episodes = 300000

DeepQLearning(env, episodes)

