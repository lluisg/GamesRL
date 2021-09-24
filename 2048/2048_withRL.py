from CustomEnv import Game2048Env

import numpy as np
import matplotlib.pyplot as plt

scores = []
better_result = {
	'score' : 0,
	'value' : 0,
	'list_moves' : [],
	'list_states' : [],
	'finished' : False,
	'episode': -1
}

print(2)
env = Game2048Env(4, 4. 3)
env = make_vec_env(lambda: env, n_envs=1)

model = DQN('MlpPolicy', env, learning_rate=1e-3, prioritized_replay=True, verbose=1)
model = model.learn(100)

episodes = 5
for i_episode in range(episodes):
	observation = env.reset()
	for t in range(1000):
		env.render()
		action, _ = model.predict(observation, deterministic=True)
		# action = env.action_space.sample()
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

print()
if better_result['finished'] == True:
	print("Episode {} finished the game!!".format(better_result['episode']))
else:
	print("No episode finished the game...")
	print("Max score = {} and Max value = {} on Episode {}".format(better_result['score'], better_result['value'], better_result['episode']))

episodes_ind = [x for x in range(episodes)]

plt.axis((0, episodes, 0, better_result['score']))
plt.plot(episodes_ind, scores, 'k', label='scores')
plt.legend(loc="upper right")
plt.show()
