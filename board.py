from graph import Colony, Graph, Harbour, Road
from constants import VERTICES, START_VERTICE_ROW, END_VERTICE_ROW, PIVOT_ROW, NEIGHBOURS, COLONY, ROADS, HARBOUR_VERTICES, HARBOUR, HEX_COORD, Resource, DEBUG
import numpy as np

class Board():
    def __init__(self, seed):
        self._random = np.random.RandomState(seed)
        self.graph = Graph().graph
        self.lands = Graph().lands

        self.player_boards = {}
        self.player_info = {}

        self.suffle_board(self._random)
    
    def suffle_board(self, random):
        land_numbers = [2, 12] + [i for i in range(3, 12) if i != 7] * 2
        land_resources = [Resource.Lumber, Resource.Wool, Resource.Grain
                          ] * 4 + [Resource.Brick, Resource.Ore] * 3
        random.shuffle(land_numbers)
        random.shuffle(land_resources)
        
        number_to_land = {}
        for i in range(18):
            number = land_numbers[i]
            if number not in number_to_land:
                number_to_land[number] = [i]
            else:
                number_to_land[number].append(i)
        self.number_to_land = number_to_land


        desert_idx = random.randint(0,19)
        self.desert_id = desert_idx
        land_numbers = land_numbers[:desert_idx] + [-1] + land_numbers[desert_idx:]
        land_resources = land_resources[:desert_idx] + [Resource.Desert] + land_resources[desert_idx:]

        for i in range(19):
            self.lands[i].update({'number' : land_numbers[i], 'resource' : land_resources[i]})
            if land_resources[i] == Resource.Desert:
                self.lands[i]['robber'] = True

        harbours = [Harbour.HarbourBrick, Harbour.HarbourLumber, Harbour.HarbourWool, Harbour.HarbourGrain, Harbour.HarbourOre] + 4 * [Harbour.HarbourGeneric]
        random.shuffle(harbours)

        for i, pair_of_vertices in enumerate(HARBOUR_VERTICES):
            for harbours_vertex in pair_of_vertices:
                self.graph[harbours_vertex][HARBOUR] = harbours[i]


    def reset_board(self, seed=None):
        for node in self.graph:
            self.graph[node][COLONY] = Colony.Uncolonised
            for roads in self.graph[node][ROADS]:
                self.graph[node][ROADS][roads] = Road.Unpaved
        for land in self.lands:
            self.lands[land]['robber'] = False 
        
        self.lands[self.desert_id]['robber'] = True 