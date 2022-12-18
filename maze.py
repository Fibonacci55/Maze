from abc import ABC, abstractmethod
import networkx as nx
from enum import IntEnum
import random as rnd
import wand.image as image
from wand import color

class Maze(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def random_cell(self):
        pass

    #@abstractmethod
    #def connect(self, o_cell):
    #    pass

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
            self.active = True



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

    @classmethod
    def masked(cls, mask_file):

        white = color.Color('#fff')
        whites = 0
        with image.Image(filename=mask_file) as img:
            m = cls(img.width, img.height)
            for i in range(0, img.height):
                for j in range(0, img.width):
                    if img[i][j] == white:
                        m.grid[i][j].active = False
                        whites += 1
            print ('Whites', whites)
            return m
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
            if self.grid[i-1][j].active:
                neighbour_list.append(self.grid[i-1][j])
        if i + 1 < self.height:
            if self.grid[i+1][j].active:
                neighbour_list.append(self.grid[i+1][j])
        if j > 0:
            if self.grid[i][j-1].active:
                neighbour_list.append(self.grid[i][j-1])
        if j + 1 < self.width:
            if self.grid[i][j+1].active:
                neighbour_list.append(self.grid[i][j+1])

        if only_unvisited:
            neighbour_list = [e for e in neighbour_list if e.visited == False]

        #print ("Neighbours of ", of_cell)
        for e in neighbour_list:
            pass
            #print (e)

        return neighbour_list



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
