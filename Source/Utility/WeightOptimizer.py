from Source.InformatiCupGame import GameWrapper
from Source.Main import HeuristicPlayer
from random import random
from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.PassivePlayer import PassivePlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
import json

import numpy as np

def funct(params):

    round_counter = 0
    game_count = 20

    for i in range(game_count):
        game_wrapper = GameWrapper(70, 70, [HeuristicPlayer(1, params), HeuristicPlayer(2, params), HeuristicPlayer(3, params), HeuristicPlayer(4, params), HeuristicPlayer(5, params), HeuristicPlayer(6, params)])
        round_counter += game_wrapper.get_round_counter()

    print('Average Game Length: ', str(round_counter / game_count))
    return round_counter / game_count

def approx_grad(params):
    h = 0.00000001
    gradient = [approx_derivative(params, h, 0), approx_derivative(params, h, 1), approx_derivative(params, h, 2)]
    norm = np.linalg.norm(gradient)
    return gradient/(norm * 100)

def approx_derivative(params, h, i):
    args1 = params[:]
    args2 = params[:]
    args3 = params[:]
    args4 = params[:]

    args1[i] = args1[i] + 2.0 * h
    args2[i] = args2[i] + h * 1.0
    args3[i] = args3[i] - h * 1.0
    args4[i] = args4[i] - 2.0 * h

    nominator = 0 - funct(args1) + 8 * funct(args2) - 8 * funct(args3) + funct(args4)
    demoniator = 12.0 * h

    return nominator / demoniator


candidates = dict()

for i in range(5):
    params = np.array([random() - 0.5 , random() - 0.5, random() - 0.5])
    prev_tries = [0,0,0]
    prev_params = [[], [], []]
    while(True):
        gradient = approx_grad(params)
        game_length = funct(params+gradient)
        print("gradient at: " + ' '.join(map(str, params +gradient)) + ": " + ' '.join(map(str, gradient)) + " game length: " + str(game_length))
        prev_tries.append(game_length)
        prev_params.append(params + gradient)
        if abs(3*game_length-prev_tries[0]-prev_tries[1]-prev_tries[2]) <= 50:
            best_approx = max(prev_tries)
            best_index = prev_tries.index(max(prev_tries))
            best_params = prev_params[best_index]
            candidates[best_approx] = best_params
            break
        else:
            prev_tries = prev_tries[1:]
            prev_params = prev_params[1:]
            params = params + gradient


print("candidates: " + json.dumps(candidates, indent=4))