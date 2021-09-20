from GameController import GameController

game = GameController(4,4)
game.play()


ppo_model_loaded = load_model(save_dir_ppo, save_name_ppo, 'PPO2')

times = 5
for time in range(times):
	observation = env.reset()
	for t in range(1001):
		env.render()
		action, _states = model.predict(obs)
		# action = env.action_space.sample()
		observation, reward, done, info = env.step(action)
		if done:
			break
