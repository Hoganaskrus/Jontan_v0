from utils import Graph, dot, norm, squared_dist, sub, dist
from board import Board
from draw import GameWindow
from constants import DEBUG
from collections import namedtuple
import pygame
from draw import _pixel_to_hex, _hex_to_node
from game import Game
from person import Player

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
    player_list = [Player(True, 'test1', (0, 0, 0)), Player(True, 'test2', (255, 255, 255))]
    catan = Game(board,player_list)

    catan.apply(0,['road', 0, 3])

    gw = GameWindow(board,[1000, 800])

    gw.displayInitialBoard()
    mouse_pos = pygame.mouse.get_pos()
    fps = 30
    expected_frame_time_ms = int((1.0/fps) * 1000)


    last_tick = pygame.time.get_ticks()
    while True:
        ev = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        gw.displayInitialBoard()

        try:
            q,r = _pixel_to_hex(*mouse_pos)
            land = board.lands[(q,r)]
            tile = land['hextile']

            corners_with_dist = []
            for c in tile.corners:
                d = dist(mouse_pos, c)
                corners_with_dist.append((d, c))
            
            corners_with_dist = sorted(corners_with_dist, key=lambda tup: tup[0])
            curr_closest = corners_with_dist[0]
            last_curr_closest = corners_with_dist[1]

            if curr_closest[0] < 20:
                pygame.draw.rect(gw.screen, pygame.Color('green'), (curr_closest[1][0]-8,curr_closest[1][1]-8,16, 16))
            else:
                pygame.draw.line(gw.screen, pygame.Color('green'), curr_closest[1], last_curr_closest[1], 3)

            if DEBUG:
                pygame.draw.line(gw.screen, pygame.Color('green'), mouse_pos, last_curr_closest[1], 1)
                pygame.draw.line(gw.screen, pygame.Color('green'), curr_closest[1], mouse_pos, 1)
                pygame.draw.line(gw.screen, pygame.Color('red'), mouse_pos, tile.center, 1)
        except Exception:
            pass


        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                test = _pixel_to_hex(mouse_pos[0], mouse_pos[1])
                pixelCenter = _hex_to_node(test.q, test.r, 1, test.size, test.center_point)
                # pixelCenter = _hex_to_pixel(test.q, test.r, test.size, test.center_point)
                print(pixelCenter)
                pygame.draw.rect(gw.screen, pygame.Color('green'), (pixelCenter[0]-8,pixelCenter[1]-8,16, 16))

        pygame.display.update()
        new_tick = pygame.time.get_ticks()
        frame_time = new_tick - last_tick
        pygame.time.delay(max(0, expected_frame_time_ms - frame_time))
        last_tick = pygame.time.get_ticks()
    p = 2


    sdasd.displayInitialBoard()

    print(_vertices)