from abc import ABC, abstractmethod
import networkx as nx
from enum import IntEnum
import svgwrite as draw

class Maze(ABC):

    @abstractmethod
    def __init__(self):
        pass

class Neighbour(IntEnum):
    """

    """
    North = 0
    East = 1
    South = 2
    West = 3

class Rectangular_Maze(Maze):

    class Maze_Element:
        def __init__(self, row, col):
            self.neighbours = [False, False, False, False]
            self.row = row
            self.col = col
            self.pos = (row, col)

        def connect(self, o_cell):
            if self.row == o_cell.row and self.col + 1 == o_cell.col:
                self.neighbours[Neighbour.East] = True
                o_cell.neighbours[Neighbour.West] = True

            if self.row == o_cell.row and self.col - 1 == o_cell.col:
                self.neighbours[Neighbour.West] = True
                o_cell.neighbours[Neighbour.East] = True

            if self.row + 1 == o_cell.row and self.col == o_cell.col:
                self.neighbours[Neighbour.South] = True
                o_cell.neighbours[Neighbour.North] = True

            if self.row - 1 == o_cell.row and self.col == o_cell.col:
                self.neighbours[Neighbour.South] = True
                o_cell.neighbours[Neighbour.North] = True

        def __str__(self):
            return "{0} {1}".format(self.pos, self.neighbours)
            #return "{0}".format(self.pos)

    def __init__(self, width, height):
        self.grid = [[self.Maze_Element(r, c) for c in range(0, width)] for r in range(0, height)]
        self.grid_graph = nx.Graph()
        for row in self.grid:
            self.grid_graph.add_nodes_from (row)

    #def add_passage (self, cell1, cell2):
    #    self.grid_graph.add_edge(cell1, cell2)

    def add_passage (self, cell, length, dir):
        """

        :param cell:
        :param length:
        :param dir:
        :return:
        """
        s = cell
        for i in range(1, length):
            if dir == 'H':
                n = (s[0], s[1] + 1)
            elif dir == 'V':
                n = (s[0] + 1, s[1])
            #print (s, n)
            grid_cell1 = self.grid[s[0]][s[1]]
            grid_cell2 = self.grid[n[0]][n[1]]
            self.grid_graph.add_edge(grid_cell1,grid_cell2)
            grid_cell1.connect(grid_cell2)
            s = n




class Maze_Gen_Algorithm(ABC):

    @abstractmethod
    def __init__(self):
        pass

class Maze_Printer:

    def __init__(self, cell_size = 10, filename="maze.svg"):
        self.cell_size = cell_size
        self.filename = filename

    def print(self, maze):

        rows = len(maze.grid)
        cols = len(maze.grid[0])
        d = draw.Drawing(self.filename)
        for i, row in enumerate(maze.grid):
            for j, el in enumerate(row):
                if not el.neighbours[Neighbour.West]:
                    #print(el)
                    s = (j * self.cell_size, i * self.cell_size)
                    e = (j * self.cell_size, (i + 1) * self.cell_size)
                    d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                if not el.neighbours[Neighbour.North]:
                    s = (j * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, i * self.cell_size)
                    d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                if j == cols - 1:
                    s = ((j + 1) * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                if i == rows - 1:
                    s = (j * self.cell_size, (i + 1) * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    d.add(draw.shapes.Line(s, e, style="stroke:#000000"))

        d.save(pretty=True)


if __name__ == '__main__':
    m = Rectangular_Maze(5,5)
    #print (r.grid)
    import sys

    m.add_passage((0,0), 5, 'H')
    #for j, el in enumerate(m.grid[0]):
    #    print(el)

    m.add_passage((1,0), 3, 'H')
    m.add_passage((2,3), 2, 'H')
    m.add_passage((3,0), 5, 'H')
    m.add_passage((4,0), 2, 'H')
    m.add_passage((4,2), 2, 'H')
    #
    m.add_passage((1,0), 2, 'V')
    m.add_passage((0,1), 4, 'V')
    #for j, el in enumerate(m.grid[0]):
    #    print(el)
    m.add_passage((1,3), 2, 'V')
    m.add_passage((0,4), 3, 'V')
    m.add_passage((2,2), 2, 'V')
    m.add_passage((3,0), 2, 'V')
    m.add_passage((3,3), 2, 'V')
    m.add_passage((3,4), 2, 'V')

    p = Maze_Printer()
    p.print(m)

    for i, row in enumerate(m.grid):
        for j, el in enumerate(row):
            #print (el)
            pass

    #print (m.grid)
    #nx.write_adjlist(m.grid_graph, "adj_list.txt")
    #print (nx.is_tree(m.grid_graph))
    #t = nx.minimum_spanning_tree(m.grid_graph)
    #print(nx.is_tree(t))
