from collections import OrderedDict
import pygame
import math

from constants import HEX_ORIENTATION, HEX_COORD, TEXT_OFFSET, VERTICES, HARBOUR_VERTICES, HARBOUR_HEX_AND_DIRECTION, HEX_SIZE, BOARD_CENTER_POINT
from testplot import Hex, polygon_corners
from board import Board

# From https://www.redblobgames.com/grids/hexagons/

class GameWindow():
    def __init__(self, gameboard, size):
        self.gameboard = gameboard
        self.size = size
        
        self.screen = pygame.display.set_mode([size[0], size[1]])
        pygame.display.set_caption('Settlers of Catan')

        hex_list = []

        for i, coord in enumerate(HEX_COORD):
            hex = HexTile(coord[0],coord[1], gameboard.lands[i])
            hex_list.append(hex)
            gameboard.lands[i]['hextile'] = hex
            gameboard.lands[tuple(coord)] = gameboard.lands[i]

        self.hex_list = hex_list


    def displayInitialBoard(self):
        #Dictionary to store RGB Color values
        HEX_COLOR = {'Brick': pygame.Color(255, 127, 80), 'Lumber': pygame.Color(34, 139, 34), 'Wool': pygame.Color(152, 251, 152), 'Grain':  pygame.Color(255, 228, 181), 'Ore':  pygame.Color(119, 136, 153), 'Desert': pygame.Color(160, 82, 45)}
        pygame.draw.rect(self.screen, pygame.Color('royalblue2'), (0,0,1000, 800)) #blue background

        for i,hex in enumerate(self.hex_list):
            land = self.gameboard.lands[i]
            color = HEX_COLOR[land['resource'].name]
            number = land['number']
        
            pygame.draw.polygon(self.screen, color, list(hex.corners.values()))
            pixelCenter = _hex_to_pixel(hex.q, hex.r)

            for i in range(6):
                rectpoint_0 = _hex_to_node(hex.q, hex.r,i,)
                rectpoint_1 = _hex_to_node(hex.q, hex.r,i+1)
                pygame.draw.line(self.screen, pygame.Color('black'), rectpoint_0, rectpoint_1, 3)

            if(land['resource'].name != 'Desert'): #skip desert text/number
                resourceText = pygame.font.SysFont('arialblack', 15).render(str(land['resource'].name) + " (" +str(number) + ")", False, (0,0,0))
                self.screen.blit(resourceText, (pixelCenter[0] + TEXT_OFFSET[land['resource'].name][0], pixelCenter[1] + TEXT_OFFSET[land['resource'].name][1])) #add text to hex


        #Display the Ports - update images/formatting later
        for i,vertecies in enumerate(HARBOUR_HEX_AND_DIRECTION): 
            harb = self.gameboard.graph[HARBOUR_VERTICES[i][0]]['harbour']
            pixelCenter = _hex_to_node(vertecies[0],vertecies[1],vertecies[2])
            portText = pygame.font.SysFont('cambria', 12).render(harb.name[7:9], False, (0,0,0))
            self.screen.blit(portText, (pixelCenter[0] , pixelCenter[1]))
            pixelCenter = _hex_to_node(vertecies[0],vertecies[1],vertecies[3])
            self.screen.blit(portText, (pixelCenter[0] , pixelCenter[1]))
            
        for i in range(1,3,1):
            rectpoint = _hex_to_node(i,-1+i,1+i)
            pygame.draw.rect(self.screen, pygame.Color('black'), (rectpoint[0]-8,rectpoint[1]-8,16, 16))

            rectpoint2 = _hex_to_node(i,-1+i,2+i)
            pygame.draw.line(self.screen, pygame.Color('black'), rectpoint, rectpoint2, 5)

    def draw_text(self, text, x, y):
        resourceText = pygame.font.SysFont('arialblack', 15).render(text, False, (0,0,0))
        self.screen.blit(resourceText, (x, y)) #add text to hex

#Layout has the orientation, size and origin

class HexTile():
    """"
    Coordinates for a hex. 
    args: q = Column
        r = Rows
        s = Square
    """
    def __init__(self, q, r, land):
        self.q = q
        self.r = r
        self.land = land
        self.center = _hex_to_pixel(q, r)
        self.corners = self._polygon_corners(land['nodes'])

    def _polygon_corners(self, nodes):
        corners = OrderedDict()
        graph_corner_map = [5,4,0,1,2,3]
        for i in range(0, 6):
            offset = _hex_corner_offset(i)
            corners[nodes[graph_corner_map[i]]] = (round(self.center[0] + offset[0],2), round(self.center[1] + offset[1],2))
        return corners

def _hex_to_pixel(q,r):
    x = (HEX_ORIENTATION[0] * q + HEX_ORIENTATION[1] * r) * HEX_SIZE[0]
    y = (HEX_ORIENTATION[2] * q + HEX_ORIENTATION[3] * r) * HEX_SIZE[1]
    return x + BOARD_CENTER_POINT[0], y + BOARD_CENTER_POINT[1]


def _hex_corner_offset(corner):
    angle = 2.0 * math.pi * (HEX_ORIENTATION[-1] - corner) / 6.0
    return HEX_SIZE[0] * math.cos(angle), HEX_SIZE[1] * math.sin(angle)

def _hex_to_node(q,r,direction):
    x,y = _hex_to_pixel(q,r)
    offset_x, offset_y = _hex_corner_offset(direction)
    return x+offset_x, y + offset_y

# def node_to_hex(node):
#     row = [i for i,v in enumerate(VERTICES) if node in v]
#     col = [i for i,v in VERTICES[row] if node==v]

def _pixel_to_hex(x,y):
    h_x = (x - BOARD_CENTER_POINT[0] ) / HEX_SIZE[0]
    h_y = (y - BOARD_CENTER_POINT[1] ) / HEX_SIZE[1]
    q = HEX_ORIENTATION[4] * h_x + HEX_ORIENTATION[5] * h_y
    r = HEX_ORIENTATION[6] * h_x  + HEX_ORIENTATION[7] * h_y

    return hex_round(q,r)


def hex_round(q,r):
    s = -q-r

    q_int = round(q)
    r_int = round(r)
    s_int = round(s)

    q_diff = abs(q_int - q)
    r_diff = abs(r_int - r)
    s_diff = abs(s_int - s)

    if q_diff > r_diff and q_diff > s_diff:
        q_int = -r_int-s_int
    elif r_diff > s_diff:
        r_int = -q_int-s_int

    return q_int,r_int



def test_layout(board):
    gw = GameWindow(board,[1000, 800])
    gw.displayInitialBoard()

    p = 2


if __name__ == '__main__':
    board = Board(1337)
    test_layout(board)
