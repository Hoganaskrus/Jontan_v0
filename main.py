from utils import Graph
from board import Board
from draw import GameWindow
import pygame
from draw import _pixel_to_hex, _hex_to_node


if __name__ == '__main__':
    _vertices_rows = [
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
    _vertices = [v for vertices_row in _vertices_rows for v in vertices_row]

    # board = Graph()
    board = Board(1337)

    gw = GameWindow(board,[1000, 800])
    gw.displayInitialBoard()

    while True:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                test = _pixel_to_hex(pos[0], pos[1], [75,75], [500,400])
                pixelCenter = _hex_to_node(test.q, test.r, 1, test.size, test.center_point)
                # pixelCenter = _hex_to_pixel(test.q, test.r, test.size, test.center_point)
                print(pixelCenter)
                pygame.draw.rect(gw.screen, pygame.Color('green'), (pixelCenter[0]-8,pixelCenter[1]-8,16, 16))

                pygame.display.update()
    p = 2


    sdasd.displayInitialBoard()

    print(_vertices)