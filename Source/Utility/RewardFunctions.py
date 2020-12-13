import numpy as np

def reward_1(obs, latest_obs):
       reward = ((obs[0] - latest_obs[0]) + (obs[1] - latest_obs[1]) + (obs[2] - latest_obs[2]) + (-obs[3] + latest_obs[3]) + ((min(obs[-4:-1]) - 17)/17))
       return (0.5 * (1 + np.tanh(reward/2.0)))
