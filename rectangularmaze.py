from typing import TypeVar, Type
from maze import Maze
import wand.image as image
from wand import color
import random as rnd
import networkx as nx
import json
import pickle
from enum import IntEnum

T = TypeVar('T', bound='MazeElement')


class Neighbour(IntEnum):
    """

    """
    North = 0
    East = 1
    South = 2
    West = 3

class MazeElement:
    def __init__(self, row: int, col: int) -> None:
        self.neighbours = [False, False, False, False]
        self.row = row
        self.col = col
        self.pos = (row, col)
        self.visited = False
        self.active = True

    def __repr__(self):
        return '{} / {}'.format(self.row, self.col)

    def __lt__(self, other: Type[T]) -> bool:
        if self.row < other.row:
            return True
        if self.row == other.row:
            if self.col < other.col:
                return True
        return False

    def connect(self, o_cell: Type[T]) -> None:
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
        # return "{0}".format(self.pos)


class RectangularMaze(Maze):

    def __init__(self, width: int, height: int):
        self.grid = [[MazeElement(r, c) for c in range(0, width)] for r in range(0, height)]
        self.grid_graph = nx.DiGraph()
        self.width = width
        self.height = height

        #for row in self.grid:
        #    self.grid_graph.add_nodes_from (row)

    @classmethod
    def masked(cls, mask_file: str) -> Maze:

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


    def make_graph(self):

        for i in range(0, self.height):
            for j in range(0, self.width):
                if not self.grid[i][j].active:
                    continue
                if self.grid[i][j].neighbours[Neighbour.South] :
                   self.grid_graph.add_edge((i, j), (i+1, j))
                if self.grid[i][j].neighbours[Neighbour.East] :
                    self.grid_graph.add_edge((i, j), (i, j+1))

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as inf:
            return pickle.load (inf)

    def to_file(self, filenname):
        with open(filenname, 'wb') as outf:
            pickle.dump(self, outf)
