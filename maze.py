from abc import ABC, abstractmethod
import networkx as nx
from enum import IntEnum
import svgwrite as draw
import random as rnd
import stack

class Maze(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def random_cell (self):
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




class Maze_Gen_Algorithm(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

class Recursive_Backtracker (Maze_Gen_Algorithm):

    def __init__(self):
        pass

    def __call__(self, maze):
        n_rows = len(maze.grid)
        n_cols = len(maze.grid[0])

        s = stack.Stack()
        e = maze.random_cell()
        #e = maze.grid[0][0]
        #print (e)
        s.push(e)
        while not s.is_empty():
            current = s.top()
            n = maze.neighbours(of_cell=current, only_unvisited=True)
            #print ('N', n)
            if len(n) == 0:
                s.pop()
            else:
                e = rnd.sample(n, 1)[0]
                #print ('e', e)
                current.connect(e)
                s.push(e)
                n.remove(e)


class Maze_Printer:

    def __init__(self, cell_size = 10, filename="maze.svg"):
        self.cell_size = cell_size
        self.filename = filename

    def print(self, maze):

        def add_to_paths(paths, s, e):
            #print (paths, s, e)
            for p in paths:
                if p[-1] == s:
                    if p[-2][0] == e[0] or p[-2][1] == e[1]:
                        p[-1] = e
                    else:
                        p.append(e)
                    #print("1:", paths)
                    return
                elif p[0] == e:
                    #print("2:", p, s, e)
                    if p[1][0] == s[0] or p[1][1] == s[1]:
                        p[0] = s
                    else:
                        p.insert(0, s)
                    return
                elif p[0] == s:
                    if p[0][0] == e[0] or p[0][1] == e[1]:
                        #print("3:", p, s, e)
                        p.insert(0, e)
                        #p[0] = e
                    else:
                        #print("4:", p, s, e)
                        p.insert(s, 0)
                    return

            paths.append([s, e])
            #print("2:", paths)

        def make_path_string (path):
            path_cmds = []

            cmd = "M {} {}".format(path[0][0], path[0][1])
            path_cmds.append(cmd)
            for p in path[1:]:
                cmd = "L {} {}".format(p[0], p[1])
                path_cmds.append(cmd)
            s = ''.join(path_cmds)
            return (s)

        rows = len(maze.grid)
        cols = len(maze.grid[0])
        paths = []
        for i, row in enumerate(maze.grid):
            for j, el in enumerate(row):
                if not el.neighbours[Neighbour.West]:
                    #print(el)
                    s = (j * self.cell_size, i * self.cell_size)
                    e = (j * self.cell_size, (i + 1) * self.cell_size)
                    #d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                    add_to_paths(paths, s, e)
                if not el.neighbours[Neighbour.North]:
                    s = (j * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, i * self.cell_size)
                    #d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                    add_to_paths(paths, s, e)
                    #print('North', paths, s, e)
                if j == cols - 1:
                    s = ((j + 1) * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    #d.add (draw.shapes.Line(s,e, style="stroke:#000000"))
                    add_to_paths(paths, s, e)
                if i == rows - 1:
                    s = (j * self.cell_size, (i + 1) * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    #d.add(draw.shapes.Line(s, e, style="stroke:#000000"))
                    add_to_paths(paths, s, e)

        d = draw.Drawing(self.filename)
        g = draw.container.Group()
        for p in paths:
            ps = make_path_string(p)
            svg_path = draw.path.Path (ps, style="stroke:#000000;fill:none")
            d.add(svg_path)

        #print (paths)
        d.add(g)
        d.save(pretty=True)


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
