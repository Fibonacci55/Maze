
from abc import ABC, abstractmethod
import svgwrite as draw
from rectangularmaze import Neighbour, Maze
import networkx as nx


class MazePrinter(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def print(self, maze: Maze):
        pass


class RectangularMazePrinter:

    def __init__(self, cell_size = 10, filename="maze.svg"):
        self.cell_size = cell_size
        self.filename = filename
        self.d = draw.Drawing(self.filename)
        self.g = draw.container.Group()
    def make_path_string (self, path):
        path_cmds = []

        cmd = "M {} {}".format(path[0][0], path[0][1])
        path_cmds.append(cmd)
        for p in path[1:]:
            cmd = "L {} {}".format(p[0], p[1])
            path_cmds.append(cmd)
        s = ''.join(path_cmds)
        return (s)

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


        rows = len(maze.grid)
        cols = len(maze.grid[0])
        paths = []
        texts = []
        for i, row in enumerate(maze.grid):
            for j, el in enumerate(row):
                if el.active and j % 2 == 0 and i % 2 == 0:
                    #t = draw.text.Text(text='({0} {1})'.format(i,j),
                    #                   insert=(j*self.cell_size, i*self.cell_size),
                    #                   font_size='6px')
                    #self.g.add(t)
                    pass

                if not el.active:
                    el.neighbours = [True, True, True, True]
                    pass
                if not el.neighbours[Neighbour.West]:
                    #print(el)
                    s = (j * self.cell_size, i * self.cell_size)
                    e = (j * self.cell_size, (i + 1) * self.cell_size)
                    add_to_paths(paths, s, e)
                    #if i % 2 == 0 and j % 2 == 0:
                    #    texts.append("{}/{}".format(i, j))
                if not el.neighbours[Neighbour.North]:
                    s = (j * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, i * self.cell_size)
                    add_to_paths(paths, s, e)
                    #if i % 2 == 0 and j % 2 == 0:
                    #    texts.append("{}/{}".format(i, j))
                if not el.neighbours[Neighbour.East]: #j == cols - 1:
                    s = ((j + 1) * self.cell_size, i * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    add_to_paths(paths, s, e)
                    #if i % 2 == 0 and j % 2 == 0:
                    #    texts.append("{}/{}".format(i, j))
                if not el.neighbours[Neighbour.South]: #i == rows - 1:
                    s = (j * self.cell_size, (i + 1) * self.cell_size)
                    e = ((j + 1) * self.cell_size, (i + 1) * self.cell_size)
                    add_to_paths(paths, s, e)
                    #if i % 2 == 0 and j % 2 == 0:
                    #    texts.append("{}/{}".format(i, j))


        for p in paths:
            ps = self.make_path_string(p)
            svg_path = draw.path.Path (ps, style="stroke:#000000;fill:none")
            self.g.add(svg_path)

        self.d.add(self.g)
    def add_path (self, path_way):

        def calc_pos (of_point):
            p = (of_point[1] * self.cell_size + self.cell_size // 2, of_point[0] * self.cell_size + self.cell_size // 2)
            return p

        pg = draw.container.Group()
        print (len(path_way))
        real_path = []
        s = calc_pos (path_way[0])
        #for i in range(0, len(path_way)-1):
        real_path.append(s)
        for p in path_way[1:]:
            e = calc_pos(p)
            #s = (path_way[i][0] * self.cell_size, path_way[i][0] * self.cell_size + self.cell_size // 2)
            #e = (path_way[i+1][0] * self.cell_size, path_way[i][0] * self.cell_size + self.cell_size // 2)
            real_path.append(e)
            s = e
            #real_path.append(s)
            #print (s, e)

        ps = self.make_path_string(real_path)
        svg_path = draw.path.Path(ps, style="stroke:#FF0000;fill:none")
        pg.add(svg_path)
        self.d.add(pg)

    def save(self):
        self.d.save(pretty=True)
