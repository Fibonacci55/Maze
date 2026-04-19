from abc import ABC, abstractmethod

class Maze_Gen_Algorithm(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass
