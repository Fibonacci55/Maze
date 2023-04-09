

from abc import ABC, abstractmethod
import stack
import random as rnd



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
