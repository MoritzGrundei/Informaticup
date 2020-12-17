from Source.Utility.GameMetricsNew import GameMetrics
import numpy as np


class GameObservations:

    def __init__(self):
        self.game_metrics = GameMetrics()

    # Obervations: Avg Dist, Avg Free Spaces, Avg Speed, Own Speed, Num Living Players, Directions for Speed free, Player Distances, Border Distances
    def get_obs_1(self, game_state):
        self.game_metrics.set_game_state(game_state)
        own_player = game_state["players"][str(game_state["you"])]
        player_distances = self.game_metrics.get_distance_to_players()
        distances = self.game_metrics.get_distances_to_borders(game_state["you"])
        obs = np.array([self.game_metrics.get_average_distance(self.game_metrics.get_distance_to_players()),
                        self.game_metrics.get_free_spaces((own_player["x"], own_player["y"])),
                        self.game_metrics.get_avg_speed(),
                        self.game_metrics.get_num_living_players(),
                        self.game_metrics.get_own_speed(),
                        self.game_metrics.get_down_free(), self.game_metrics.get_down_free(), self.game_metrics.get_down_free(), self.game_metrics.get_down_free(),
                        player_distances[0], player_distances[1], player_distances[2], player_distances[3],
                        player_distances[4], player_distances[5],
                        distances[0], distances[1], distances[2], distances[3]])
        return obs
