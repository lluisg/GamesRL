from CustomEnv import Game2048Env

import numpy as np
import matplotlib.pyplot as plt
import cv2

scores = []
better_result = {
	'score' : 0,
	'value' : 0,
	'list_moves' : [],
	'list_states' : [],
	'finished' : False,
	'episode': -1
}

env = Game2048Env(4, 4, 6, True)

episodes = 1
for i_episode in range(episodes):
	observation = env.reset()
	for t in range(1001):
		env.render('terminal')
		action = env.action_space.sample()
		observation, reward, done, info = env.step(action)

		if done:
			print("Episode {} finished after {} movements with score = {} and maximum value = {}".format(i_episode, t+1, reward, info['max_v']))
			scores.append(reward)

			if reward > better_result['score']:

				if info['max_v'] == 2048:
					better_result['finished'] = True
				else:
					better_result['finished'] = False

				better_result['score'] = reward
				better_result['value'] = info['max_v']
				better_result['list_moves'] = info['list_moves']
				better_result['list_states'] = info['list_states']
				better_result['episode'] = i_episode

			break
env.close()
