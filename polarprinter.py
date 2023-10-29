import drawsvg as draw
import numpy as np
from polar_coordinates import Polar, PolarGridCell, Coordinate
from typing import TypeVar
from icecream import ic

PolarType = TypeVar("Polar")


def print_single_cell (cell: PolarGridCell, canvas: draw.Drawing) -> None:

    #d = draw.Drawing(200, 200, origin='center',transform='translate(-100,-100)')
    #d = draw.Drawing(400, 400)
    #d = draw.Drawing(200, 200, transform='translate(0,100)')

    ic(print(cell))
    c_ur = cell.ur.to_cartesian()
    c_lr = cell.lr.to_cartesian()
    c_ll = cell.ll.to_cartesian()
    c_ul = cell.ul.to_cartesian()

    #c_ur = Cartesian(60.0, 0.0)
    #c_lr = Cartesian(30.0, 0.0)
    #c_ll = Cartesian(0.0, 30.0)
    #c_ul = Cartesian(0.0, 60.0)

    #print(cell)
    #print(c_ur, c_lr, c_ul, c_ll)

    p = draw.Path(id="First", style="fill:none;stroke:#000000")
    p.M(c_lr.x, c_lr.y)
    p.A(cell.lr.rho, cell.lr.rho, rot=0, large_arc=0, sweep=0, ex=c_ll.x, ey=c_ll.y)

    #d.append(p)
    #p.L(c_ul.x, c_ul.y)

    #p = draw.Path(id="Second",style="fill:none;stroke:#FF0000")
    p.M(c_ur.x, c_ur.y)
    p.A(cell.ur.rho, cell.ur.rho, rot=0, large_arc=0, sweep=0, ex=c_ul.x, ey=c_ul.y)

    p.M(c_ur.x, c_ur.y)
    p.L(c_lr.x, c_lr.y)

    p.M(c_ul.x, c_ul.y)
    p.L(c_ll.x, c_ll.y)

    canvas.append(p)
    #d.save_svg('polar.svg')



if __name__ == '__main__':

    #d = draw.Drawing(200, 100, origin='center')
    #d.append(draw.Arc (60, 20, 20, 60, 270))
    #print(d.as_svg())

    ic.configureOutput(includeContext=True)
    mirror = np.matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    translation = np.matrix([[1, 0, 200], [0, 1, 200], [0, 0, 1]])
    Coordinate.add_transformation(translation*mirror)
    cell = PolarGridCell(lr=Polar(30, 0), height=30, arc=45)
    print("Cell", cell)
    #print("Cell", cell.to_cartesian())


    d = draw.Drawing(400, 400)
    #print(Coordinate.transformation)
    cell = PolarGridCell(lr=Polar(30, 0), height=30, arc=45)
    print_single_cell(cell, d)
    cell = PolarGridCell(lr=Polar(30, 45), height=30, arc=45)
    print_single_cell(cell, d)
    cell = PolarGridCell(lr=Polar(30, 90), height=30, arc=45)
    print_single_cell(cell, d)

    d.save_svg('polar.svg')
    #draw_line()