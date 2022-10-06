
from constants import PRICES
from utils import Road



class Game():

    def __init__(self, gameboard, player_list):
        self.gameboard = gameboard
        self.player_list = player_list

        self.gamestate = []

    def apply(self, player, action):
        if self.is_allowed(player, action):
            pass




    def is_allowed(self, player, action):
        if _enough_resources(self.player_list[player].resources, action[0]):
            return False

        if action[0] == 'road':
            road_idx = str(action[1])+str(action[2])
            for _, nodes in self.gameboard.graph.items():
                if road_idx in nodes['roads']:
                    if nodes['roads'] == Road.Unpaved:
                        nodes['roads'] = [player, Road.Paved]
                        self.remove_resources(player, PRICES[action[0]])
                        return True

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




