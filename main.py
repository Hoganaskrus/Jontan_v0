from utils import Graph
from board import Board
from draw import GameWindow


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
    board = Board(0)

    sdasd = GameWindow(gameboard=board)

    sdasd.displayInitialBoard()

    print(_vertices)