# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from maze import Rectangular_Maze
from maze_gen_algorithms import Recursive_Backtracker
from maze_printer import Rectangular_Maze_Printer

if __name__ == '__main__':

    mask = "D:\\Projects\\Flavio\\fla_quadrat.png"
    #m = Rectangular_Maze(300,300)
    m = Rectangular_Maze.masked(mask)
    #m = Rectangular_Maze(2,2)
    a = Recursive_Backtracker()
    a(m)

    p = Rectangular_Maze_Printer()
    p.print(m)
