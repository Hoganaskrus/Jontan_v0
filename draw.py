import pygame
import math

from constants import HEX_ORIENTATION, HEX_COORD, TEXT_OFFSET, VERTICES, HARBOUR_VERTICES, HARBOUR_HEX_AND_DIRECTION
from testplot import Hex
from board import Board

# From https://www.redblobgames.com/grids/hexagons/

class GameWindow():
    def __init__(self, gameboard, size, center_point=[500,400], hex_size=[75,75]):
        self.gameboard = gameboard
        self.size = size
        self.center_point = center_point
        self.hex_size = hex_size
        
        self.screen = pygame.display.set_mode([size[0], size[1]])
        pygame.display.set_caption('Settlers of Catan')

        hex_list = []

        for coord in HEX_COORD:
            hex_list.append(HexTile(coord[0],coord[1],hex_size, center_point))

        self.hex_list = hex_list


    def displayInitialBoard(self):
        #Dictionary to store RGB Color values
        HEX_COLOR = {'Brick': pygame.Color(255, 127, 80), 'Lumber': pygame.Color(34, 139, 34), 'Wool': pygame.Color(152, 251, 152), 'Grain':  pygame.Color(255, 228, 181), 'Ore':  pygame.Color(119, 136, 153), 'Desert': pygame.Color(160, 82, 45)}
        pygame.draw.rect(self.screen, pygame.Color('royalblue2'), (0,0,1000, 800)) #blue background

        for i,hex in enumerate(self.hex_list):
            land = self.gameboard.lands[i]
            color = HEX_COLOR[land['resource'].name]
            number = land['number']
        
            pygame.draw.polygon(self.screen, color, hex.polygon_corners())
            pixelCenter = _hex_to_pixel(hex.q, hex.r, hex.size, hex.center_point)
            if(land['resource'].name != 'Desert'): #skip desert text/number
                resourceText = pygame.font.SysFont('arialblack', 15).render(str(land['resource'].name) + " (" +str(number) + ")", False, (0,0,0))
                self.screen.blit(resourceText, (pixelCenter[0] + TEXT_OFFSET[land['resource'].name][0], pixelCenter[1] + TEXT_OFFSET[land['resource'].name][1])) #add text to hex


        #Display the Ports - update images/formatting later
        for i,vertecies in enumerate(HARBOUR_HEX_AND_DIRECTION): 
            harb = self.gameboard.graph[HARBOUR_VERTICES[i][0]]['harbour']
            pixelCenter = _hex_to_node(vertecies[0],vertecies[1],vertecies[2],hex.size,hex.center_point)
            portText = pygame.font.SysFont('cambria', 12).render(harb.name[7:9], False, (0,0,0))
            self.screen.blit(portText, (pixelCenter[0] , pixelCenter[1]))
            pixelCenter = _hex_to_node(vertecies[0],vertecies[1],vertecies[3],hex.size,hex.center_point)
            self.screen.blit(portText, (pixelCenter[0] , pixelCenter[1]))
            
        for i in range(1,3,1):
            rectpoint = _hex_to_node(i,-1+i,1+i,self.hex_size,self.center_point)
            pygame.draw.rect(self.screen, pygame.Color('black'), (rectpoint[0]-8,rectpoint[1]-8,16, 16))

            rectpoint2 = _hex_to_node(i,-1+i,2+i,self.hex_size,self.center_point)
            pygame.draw.line(self.screen, pygame.Color('black'), rectpoint, rectpoint2, 5)

        pygame.display.update()

#Layout has the orientation, size and origin

class HexTile():
    """"
    Coordinates for a hex. 
    args: q = Column
        r = Rows
        s = Square
    """
    def __init__(self, q, r, hex_size, center_point):
        self.q = q
        self.r = r
        self.size = hex_size
        self.center_point = center_point


    def polygon_corners(self):
        corners = []
        center = _hex_to_pixel(self.q, self.r, self.size, self.center_point)
        for i in range(0, 6):
            offset = _hex_corner_offset(self.size, i)
            corners.append((round(center[0] + offset[0],2), round(center[1] + offset[1],2)))
        return corners

def _hex_to_pixel(q,r, hex_size, center_point):
    x = (HEX_ORIENTATION[0] * q + HEX_ORIENTATION[1] * r) * hex_size[0]
    y = (HEX_ORIENTATION[2] * q + HEX_ORIENTATION[3] * r) * hex_size[1]
    return x + center_point[0], y + center_point[1]


def _hex_corner_offset(hex_size, corner):
    angle = 2.0 * math.pi * (HEX_ORIENTATION[-1] - corner) / 6.0
    return hex_size[0] * math.cos(angle), hex_size[1] * math.sin(angle)

def _hex_to_node(q,r,direction, hex_size, center_point):
    x,y = _hex_to_pixel(q,r,hex_size,center_point)
    offset_x, offset_y = _hex_corner_offset(hex_size, direction)
    return x+offset_x, y + offset_y

# def node_to_hex(node):
#     row = [i for i,v in enumerate(VERTICES) if node in v]
#     col = [i for i,v in VERTICES[row] if node==v]



def test_layout(board):
    gw = GameWindow(board,[1000, 800])
    gw.displayInitialBoard()

    p = 2


if __name__ == '__main__':
    board = Board(1337)

    test_layout(board)