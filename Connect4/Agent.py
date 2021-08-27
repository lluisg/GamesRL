import gym

class CustomEnv(gym.Env):
    def __init__(self,env_config={}):
        self.observation_space = <gym.space>
        self.action_space = <gym.space>

    def reset(self):
        # reset the environment to initial state
        return observation

    def step(self, action):
        # perform one step in the game logic
        return observation, reward, done, info
