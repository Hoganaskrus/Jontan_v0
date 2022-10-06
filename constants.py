from distutils.debug import DEBUG
import enum
import math

DEBUG = True

HEX_SIZE = (75,75)
BOARD_CENTER_POINT = (500,400)

VERTICES = [
        [i for i in range(0, 3)],
        [i for i in range(3, 7)],
        [i for i in range(7, 11)],
        [i for i in range(11, 16)],
        [i for i in range(16, 21)],
        [i for i in range(21, 27)],
        [i for i in range(27, 33)],
        [i for i in range(33, 38)],
        [i for i in range(38, 43)],
        [i for i in range(43, 47)],
        [i for i in range(47, 51)],
        [i for i in range(51, 54)]
    ]

HARBOUR_VERTICES = [[0,3],[1,5],[11,16],[33,38],[47,51],[49,52],[42,46],[26,32],[10,15]]
HARBOUR_HEX_AND_DIRECTION = [[1,-2,1,2], [0,-2,2,3], [-1,-1,3,4], [-2,1,3,4], [-2,2,4,5], [-1,2,5,6], [1,1,5,6], [2,0,0,1], [2,-1,1,2]]
END_VERTICE_ROW = 11
START_VERTICE_ROW = 0
PIVOT_ROW = 6

NEIGHBOURS = 'neighbours'
COLONY = 'colony'
ROADS = 'roads'
HARBOUR = 'harbour'

HEX_ORIENTATION = [math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0,
                math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0,
                0.5]
HEX_COORD = [[0,-2],[1,-2],[2,-2],[-1,-1],[0,-1],[1,-1],[2,-1],[-2,0],[-1,0],[0,0],[1,0],[2,0],[-2,1],[-1,1],[0,1],[1,1],[-2,2],[-1,2],[0,2]]
TEXT_OFFSET = {'Brick': [-32,-5], 'Lumber': [-40,-5], 'Wool': [-25,-5], 'Grain': [-32,-5], 'Ore': [-22,-5]}

class Resource(enum.Enum):
    Brick = 0
    Lumber = 1
    Wool = 2
    Grain = 3
    Ore = 4
    Desert = 5

PRICES = {
    'road' : {
        Resource.Brick: 1,
        Resource.Lumber: 1,
        Resource.Wool: 0,
        Resource.Grain: 0,
        Resource.Ore: 0,
    },
    'settlement' : {
        Resource.Brick: 1,
        Resource.Lumber: 1,
        Resource.Wool: 1,
        Resource.Grain: 1,
        Resource.Ore: 0
    },
    'city' : {
        Resource.Brick: 0,
        Resource.Lumber: 0,
        Resource.Wool: 0,
        Resource.Grain: 2,
        Resource.Ore: 3
    },
    'development_card' : {
        Resource.Brick: 0,
        Resource.Lumber: 0,
        Resource.Wool: 1,
        Resource.Grain: 1,
        Resource.Ore: 1,
    },
}