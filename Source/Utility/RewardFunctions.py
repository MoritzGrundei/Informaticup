import numpy as np


def reward_1(obs, latest_obs):  # reward from Avg Distance, Avg Speed, change Num Living Players, Border Distances
    reward = ((obs[0] - latest_obs[0])  # average distance
              + (obs[2]) / 10  # avg Speed normalized
              + (-obs[3] + latest_obs[3])
              + ((min(obs[-4:-1]) - 17) / 17))
    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_2(obs, latest_obs):  # reward from change in num living players
    reward = (-obs[3] + latest_obs[3]) + 1
    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_3(obs, latest_obs):  # reward from Change in num Living Players and Distance to Border
    reward = (-obs[3] + latest_obs[3] + ((min(obs[-4:-1]) - 17) / 17))
    return reward


def reward_simple():  # reward is one as long as player is alive
    reward = 1
    return reward
