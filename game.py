
from tkinter import W
from constants import PRICES, Actions
from graph import Road



class Game():

    def __init__(self, gameboard, player_list):
        self.gameboard = gameboard
        self.player_list = player_list

        self.gamestate = []

    def apply(self, player, action, *args):
        if self.is_allowed(player, action, *args):
            pass




    def is_allowed(self, player, action, *args):
        if _enough_resources(self.player_list[player].resources, action):
            return False

        if action == Actions.BuildRoad:
            node1, node2 = args
            road_idx = str(node1).zfill(2)+str(node2).zfill(2)
            node = self.gameboard.graph[node1]
            if road_idx in node['roads']:
                if not node['roads'][road_idx]['owner']:
                    node['roads'][road_idx]['owner'] = player
                    self.remove_resources(player, PRICES[action])
                    return True
            return False
            pass

    
    def remove_resources(self, player, resources):
        for r in resources:
            self.player_list[player].resources[r.name] -= r.value


def _enough_resources(resources, action):
    if action not in PRICES:
        return True
    else:
        for cost_per_resourcs in PRICES[action]:
            if cost_per_resourcs.value > resources[cost_per_resourcs.name]:
                return False




