import enum
from constants import VERTICES, HEX_COORD, START_VERTICE_ROW, END_VERTICE_ROW, PIVOT_ROW, NEIGHBOURS, COLONY, ROADS, HARBOUR, Resource

class Colony(enum.Enum):
    Uncolonised = 0
    Settlement = 1
    City = 2

class Harbour(enum.Enum):
    HarbourBrick = Resource.Brick.value
    HarbourLumber = Resource.Lumber.value
    HarbourWool = Resource.Wool.value
    HarbourGrain = Resource.Grain.value
    HarbourOre = Resource.Ore.value
    HarbourGeneric = 5
    NoHarbour = 6

class Road(enum.Enum):
    Paved = 1
    Unpaved = 2

class Graph():
    def __init__(self):
        self.roads = {}
        self.graph = self._build_graph()
        self.lands = self._build_lands()

    def _build_graph(self):
        graph = {}
        for i, row in enumerate(VERTICES):
            if i % 2: #When connection above is a split
                for j,node in enumerate(row):
                    if i < END_VERTICE_ROW:
                        neighbours = [VERTICES[i+1][j]]  #Connect downwards a line
                    else:
                        neighbours = [VERTICES[i-1][j], VERTICES[i-1][j+1]] #Only when last row, connect upwards
                    if i not in [START_VERTICE_ROW, END_VERTICE_ROW]:
                        if i < PIVOT_ROW: #If aggregation is top/bottom of graph
                            if node == row[0]:
                                neighbours.extend([VERTICES[i-1][j]]) #Connect only upwards to the right
                            elif node == row[-1]:
                                neighbours.extend([VERTICES[i-1][j-1]]) #Connect only upwards to the left
                            else:
                                neighbours.extend([VERTICES[i-1][j-1], VERTICES[i-1][j]]) #Connect upwards
                        else:
                            neighbours.extend([VERTICES[i-1][j], VERTICES[i-1][j+1]])#Connect upwards, since bottom rows

                    neighbours.sort()
                    graph[node] = {NEIGHBOURS : neighbours, COLONY: Colony.Uncolonised, HARBOUR: Harbour.NoHarbour, 'owner': None}

            else: #When connection above is a line
                for j,node in enumerate(row):
                    if i < PIVOT_ROW: #If aggregation is top/bottom of graph
                        if i > START_VERTICE_ROW:
                            neighbours = [VERTICES[i-1][j], VERTICES[i+1][j], VERTICES[i+1][j+1]] #Connect downwards and upwards, since top rows
                        else:
                            neighbours = [VERTICES[i+1][j], VERTICES[i+1][j+1]] #Only when first row, don't connect upwards
                    else:
                        if node == row[0]: #Connect only downwards to the right
                            neighbours = [VERTICES[i+1][j]]
                        elif node == row[-1]: #Connect only downwards to the left
                            neighbours = [VERTICES[i+1][j-1]]
                        else:
                            neighbours = [VERTICES[i+1][j-1], VERTICES[i+1][j]] #Connect downwards
                        neighbours.append(VERTICES[i-1][j])
                    neighbours.sort()
                    graph[node] = {NEIGHBOURS : neighbours, COLONY: Colony.Uncolonised, HARBOUR: Harbour.NoHarbour, 'owner': None}

            for node in row:
                node_roads = {}
                for connection in graph[node][NEIGHBOURS]:
                    key = str(node).zfill(2) + str(connection).zfill(2)
                    rew_key = str(connection).zfill(2) + str(node).zfill(2)
                    new_road = self.roads.get(rew_key, {'type': Road.Unpaved, 'node': node, 'connection': connection, 'owner': None})

                    node_roads[key] = new_road
                    self.roads[key] = new_road

                graph[node][ROADS] = node_roads

        return graph

    def _build_lands(self):
        lands = {}
        new_lands_counter = 0
        for i, row in enumerate(VERTICES):
            if i == END_VERTICE_ROW - 1:
                del lands[19]
                return lands
            neighbours = []
            if i % 2 == 0:
                for new_land_idx,node in enumerate(row):
                    is_a_new_land = True
                    lands[new_land_idx+new_lands_counter] = {}
                    neighbours = [node]
                    for j, p in enumerate(self.graph[node][NEIGHBOURS]):
                        if i >= PIVOT_ROW:
                            if node == row[0] or node == row[-1]:
                                is_a_new_land = False
                                new_lands_counter -= 1
                                break
                        if node < 3:
                            j += 1
                        if p > node:
                            neighbours.append(p)
                            q = self.graph[p][NEIGHBOURS][-1]
                            neighbours.append(q)
                            if j % 3 == 1:
                                neighbours.append(self.graph[q][NEIGHBOURS][-1])
                    if is_a_new_land:
                        lands[new_land_idx + new_lands_counter]['nodes'] = neighbours
                        lands[new_land_idx + new_lands_counter]['robber'] = False
                        for node in neighbours:
                            if new_land_idx + new_lands_counter not in node['lands']:
                                node['lands'] = {}
                            node['lands'][new_land_idx + new_lands_counter] = lands[new_land_idx + new_lands_counter]
                new_lands_counter += len(row)
