from abc import ABC, abstractmethod
import networkx as nx
from enum import IntEnum
import random as rnd

class Maze(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def random_cell(self):
        pass

    @abstractmethod
    def connect(self, o_cell):
        pass

    @abstractmethod
    def neighbours(self, of_cell, only_unvisited=True):
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
            self.visited = False

        def connect(self, o_cell):
            self.visited = True
            o_cell.visited = True

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
                self.neighbours[Neighbour.North] = True
                o_cell.neighbours[Neighbour.South] = True

        def __str__(self):
            return "{0} {1}".format(self.pos, self.neighbours)
            #return "{0}".format(self.pos)

    def __init__(self, width, height):
        self.grid = [[self.Maze_Element(r, c) for c in range(0, width)] for r in range(0, height)]
        self.grid_graph = nx.Graph()
        self.width = width
        self.height = height

        for row in self.grid:
            self.grid_graph.add_nodes_from (row)

    def random_cell(self):
        i = rnd.randint(0, self.height-1)
        j = rnd.randint(0, self.width-1)

        return self.grid[i][j]

    def neighbours(self, of_cell, only_unvisited=True):
        neighbour_list = []
        i = of_cell.row
        j = of_cell.col

        #print ('i {}, i+1 {}, j {}, j+1 {}'.format(i, i+1, j, j+1))
        if i > 0:
            neighbour_list.append(self.grid[i-1][j])
        if i + 1 < self.height:
            neighbour_list.append(self.grid[i+1][j])
        if j > 0:
            neighbour_list.append(self.grid[i][j-1])
        if j + 1 < self.width:
            neighbour_list.append(self.grid[i][j+1])

        if only_unvisited:
            neighbour_list = [e for e in neighbour_list if e.visited == False]

        #print ("Neighbours of ", of_cell)
        for e in neighbour_list:
            pass
            #print (e)

        return neighbour_list

    def add_passage(self, cell, length, dir):
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








if __name__ == '__main__':

    m = Rectangular_Maze(300,300)
    #m = Rectangular_Maze(2,2)
    a = Recursive_Backtracker()
    a(m)

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
