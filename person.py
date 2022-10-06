
from constants import Resource


class Player():

    def __init__(self, is_player, name, color):
        self.is_player = is_player
        self.name = name
        self.color = color
        self.n_dev_cards = 0
        self.resources = {r.name : 5 for r in Resource}


    def get_num_cards(self):
        n_cards = 0
        for r in self.resources:
            n_cards += r