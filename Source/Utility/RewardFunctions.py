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
    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_4(obs, latest_obs):  # reward from Change in num Living Players and Distance to Border + Speed between 1 and 3
    reward = (-obs[3] + latest_obs[3] + ((min(obs[-4:-1]) - 17) / 17))
    if 1 <= obs[4] <= 3:
        reward = reward + 2
    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_simple(obs, latest_obs):  # reward is one as long as player is alive + Speed 1 - 3
    reward = 1
    return reward


def reward_5(obs, latest_obs): # difference in avg distance to players,  difference in num of living players, difference in border distances
    reward = 0
    if obs[0] > latest_obs[0]:
        reward = reward + 1
    if obs[3] < latest_obs[3]:
        reward = reward + 1
    if min(obs[-4:-1]) > min(latest_obs[-4:-1]):
        reward = reward + 1

    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_6(obs, latest_obs): # difference in avg distance to players,  difference in num of living players, difference in border distances and directions free
    reward = 0
    if obs[0] > latest_obs[0]:
        reward = reward + 1
    if obs[3] < latest_obs[3]:
        reward = reward + 1
    if min(obs[-4:-1]) > min(latest_obs[-4:-1]):
        reward = reward + 1
    if obs[5] == True:
        reward = reward + 1
    if obs[6] == True:
        reward = reward + 1
    if obs[7] == True:
        reward = reward + 1
    if obs[8] == True:
        reward = reward + 1

    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_7(obs, latest_obs): # difference in free spaces, avg dist, num of living players, border distance and free directions
    reward = 0
    if obs[0] > latest_obs[0]:
        reward = reward + 1
    if obs[1] > latest_obs[1]:
        reward = reward + 1
    if obs[3] < latest_obs[3]:
        reward = reward + 1
    if min(obs[-4:-1]) > min(latest_obs[-4:-1]):
        reward = reward + 1
    if obs[5] == True:
        reward = reward + 1
    if obs[6] == True:
        reward = reward + 1
    if obs[7] == True:
        reward = reward + 1
    if obs[8] == True:
        reward = reward + 1

    return 0.5 * (1 + np.tanh(reward / 2.0))


def reward_8(obs, latest_obs): # free spaces, number of living players, distances to borders, directions free
    reward = 0
    if obs[1] > latest_obs[1]:
        reward = reward + 1
    if obs[3] < latest_obs[3]:
        reward = reward + 1
    if min(obs[-4:-1]) > min(latest_obs[-4:-1]):
        reward = reward + 3
    if obs[5] == True:
        reward = reward + 5
    if obs[6] == True:
        reward = reward + 5
    if obs[7] == True:
        reward = reward + 5
    if obs[8] == True:
        reward = reward + 5


    return 0.5 * (1 + np.tanh(reward / 2.0))