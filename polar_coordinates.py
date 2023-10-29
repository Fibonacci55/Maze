import drawsvg as draw
import numpy as np
import mpmath as mp
from typing import TypeVar
from math import radians, degrees
import math
from icecream import ic

PolarType = TypeVar("Polar")


class Coordinate:

    transformation = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def add_transformation(trans_matrix: np.matrix) -> None:
        Coordinate.transformation *= trans_matrix

class Cartesian:

    def __init__(self, x: float, y: float) -> None:
        setattr(self, '_x', x)
        setattr(self, '_y', y)
        ic(self._x, self._y)

    def to_polar(self) -> PolarType:
        rho = np.sqrt(self.x ** 2 + self.y ** 2)
        phi = np.arctan2(self.y, self.x)
        return Polar(rho, phi)

    @property
    def rho(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def phi(self):
        return np.arctan2(self.y, self.x)

    @property
    def x(self):
        v = np.array([[self._x],[self._y], [1]])
        m = Coordinate.transformation * v
        return (m[0,0])

    @property
    def y(self):
        v = np.array([[self._x],[self._y], [1]])
        m = Coordinate.transformation * v
        return (m[1, 0])

    @x.setter
    def x(self, value):
        setattr(self, '_x', value)

    @y.setter
    def y(self, value):
        setattr(self, '_y', value)

    def __str__(self):
        lx = self.x
        ly = self.y
        return "C({x:.2f} / {y:.2f})".format(x=lx, y=ly)

class Polar:
    def __init__(self, rho: float, phi: float) -> None:
        self.rho = rho
        self.phi = phi

    def to_cartesian(self) -> Cartesian:
        x = self.rho * math.cos(radians(self.phi))
        y = self.rho * math.sin(radians(self.phi))

        return Cartesian(x, y)

    @property
    def x(self):
        return self.rho * np.cos(radians(self.phi))

    @property
    def y(self):
        return self.rho * np.sin(radians(self.phi))

    def __str__(self):
        return "R({rho:.2f} / {phi:.2f})".format(rho=self.rho, phi=self.phi)


def create_polar_grid (start: float, steps: int, sectors: int) -> None:

    for s in range(0, steps):
        for angle in range(0, 360 // sectors):
            pass

#def create_polar_cell(lr: Polar, arc: float, height: float) -> list[Polar]:

class PolarGridCell:

    def __init__(self, lr: Polar, height:float, arc:float) -> None:
        #self.arc = arc
        self.lr = lr
        self.ur = Polar(rho=self.lr.rho + height, phi=self.lr.phi)
        self.ll = Polar(rho=self.lr.rho, phi=self.lr.phi + arc)
        self.ul = Polar(rho=self.lr.rho + height, phi=self.lr.phi + arc)

    def __str__(self):
        return "Polar lr:{lr}/ur:{ur}/ll:{ll}/ul:{ul}".format(lr=self.lr, ur=self.ur, ll=self.ll, ul=self.ul)

    def to_cartesian(self):
       c = CartesianGridCell(
           lr=self.lr.to_cartesian(),
           ur = self.ur.to_cartesian(),
           ll = self.ll.to_cartesian(),
           ul = self.ul.to_cartesian()
       )
       return c

class CartesianGridCell:

    def __init__(self, lr: Cartesian, ur: Cartesian, ll: Cartesian, ul: Cartesian):
        self.lr = lr
        self.ur = ur
        self.ll = ll
        self.ul = ul

    def __str__(self):
        return "Cartesian lr:{lr}/ur:{ur}/ll:{ll}/ul:{ul}".format(lr=self.lr, ur=self.ur, ll=self.ll, ul=self.ul)
