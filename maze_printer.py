
from abc import ABC, abstractmethod
import svgwrite as draw
from maze import Neighbour

class Maze_Printer(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def print(self, maze):
        pass


class Rectangular_Maze_Printer:

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
                if not el.active:
                    el.neighbours = [True, True, True, True]
                #    pass
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
            g.add(svg_path)

        #print (paths)
        d.add(g)
        d.save(pretty=True)
