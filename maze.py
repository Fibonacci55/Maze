from abc import ABC, abstractmethod

from maze_gen_algorithms import Recursive_Backtracker
#from maze_printer import MazePrinter


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




if __name__ == '__main__':


    #m = RectangularMaze(300,300)
    #m = RectangularMaze(2,2)
    a = Recursive_Backtracker()
    a(m)


    #print (m.grid)
    #nx.write_adjlist(m.grid_graph, "adj_list.txt")
    #print (nx.is_tree(m.grid_graph))
    #t = nx.minimum_spanning_tree(m.grid_graph)
    #print(nx.is_tree(t))
