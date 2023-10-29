from maze import Maze
from math import pi
from icecream import ic
from polar_coordinates import Polar, PolarGridCell, Coordinate

def arc_length(radius: float, arc: float) -> float:

    l = 2*pi * radius * (arc / 360)
    return l

class PolarMaze(Maze):

    def __init__(self, no_rows: int, inner_cell_count: int, height: int, start: int=0) -> None:
        pass

        self.rows = []
        initial_arc = 360.0/inner_cell_count
        ic(initial_arc)
        initial_arc_length = arc_length(1.0, initial_arc)
        current_cell_count = inner_cell_count
        current_arc = initial_arc
        current_arc_length = initial_arc_length
        for row_num in range(1, no_rows+1):
            row = [PolarGridCell(lr=Polar(rho=start+row_num*height,phi=i*current_arc),height=height, arc=current_arc) for i in range(0, current_cell_count)]
            ic(row_num)
            self.rows.append(row)
            next_arc_length =arc_length(row_num + 1, current_arc)
            if next_arc_length >= 10.2 * current_arc_length:
                current_cell_count *= 2
                current_arc /= 2
                current_arc_length = next_arc_length
                ic(current_cell_count, current_arc, current_arc_length)


    def random_cell(self):
        pass

    def neighbours(self, of_cell, only_unvisited=True):
        pass


if __name__ == '__main__':

    import drawsvg as draw
    from polarprinter import print_single_cell
    import numpy as np

    mirror = np.matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    translation = np.matrix([[1, 0, 2000], [0, 1, 2000], [0, 0, 1]])
    Coordinate.add_transformation(translation*mirror)

    pm = PolarMaze(no_rows=15, inner_cell_count=12, height=60, start=1000)
    d = draw.Drawing(4000, 4000)
    # print(Coordinate.transformation)
    for row in pm.rows:
        for cell in row:
            print_single_cell(cell, d)

    d.save_svg('polar_full.svg')

