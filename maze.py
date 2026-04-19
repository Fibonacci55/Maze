from abc import ABC, abstractmethod

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from typing import Generic, Iterator, List, Optional, Protocol, TypeVar

from cell import Cell
from polar_cell import Polar_Cell


class MazeCell(Protocol):
    visited: bool


TCell = TypeVar("TCell", bound=MazeCell)


class Maze(ABC, Generic[TCell]):
    """Abstract base class for maze implementations."""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def random_cell(self) -> TCell:
        pass

    @abstractmethod
    def neighbours(self, of_cell: TCell, only_unvisited: bool = True) -> List[TCell]:
        pass

    @abstractmethod
    def all_cells(self) -> List[TCell]:
        pass


class Maze_Grid(Maze[Cell]):
    """Maze implementation using a 2D rectangular grid of cells."""

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must both be positive")

        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def random_cell(self) -> Cell:
        x: int = random.randint(0, self.width - 1)
        y: int = random.randint(0, self.height - 1)
        return self.grid[y][x]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def neighbours(self, of_cell: Cell, only_unvisited: bool = True) -> List[Cell]:
        neighbours: List[Cell] = []
        for dx, dy in Cell.DIRS.values():
            neighbour: Optional[Cell] = self.get_cell(of_cell.x + dx, of_cell.y + dy)
            if neighbour is None:
                continue
            if only_unvisited and neighbour.visited:
                continue
            neighbours.append(neighbour)
        return neighbours

    def all_cells(self) -> List[Cell]:
        return [cell for row in self.grid for cell in row]

    def __iter__(self) -> Iterator[List[Cell]]:
        return iter(self.grid)

    def __len__(self) -> int:
        return self.width * self.height


class Polar_Grid(Maze[Polar_Cell]):
    """Maze implementation using concentric circular rows of cells.

    Parameters
    ----------
    circle_count:
        Number of concentric circles (rings) in the maze.
    inner_circle_cells:
        Number of cells placed in the innermost ring.

    The number of cells per ring is adapted automatically so that cell sizes stay
    roughly consistent as the circumference grows.
    """

    def __init__(self, circle_count: int, inner_circle_cells: int) -> None:
        if circle_count <= 0:
            raise ValueError("circle_count must be positive")
        if inner_circle_cells <= 0:
            raise ValueError("inner_circle_cells must be positive")

        self.circle_count: int = circle_count
        self.inner_circle_cells: int = inner_circle_cells
        self.grid: List[List[Polar_Cell]] = []

        self._prepare_grid()
        self._configure_cells()

    def _prepare_grid(self) -> None:
        base_radius: float = 0.5
        base_circumference: float = 2.0 * math.pi * base_radius
        target_arc_length: float = base_circumference / self.inner_circle_cells

        first_row: List[Polar_Cell] = [
            Polar_Cell(0, index)
            for index in range(self.inner_circle_cells)
        ]
        self.grid.append(first_row)

        for ring in range(1, self.circle_count):
            previous_count: int = len(self.grid[ring - 1])
            current_radius: float = ring + 0.5
            current_circumference: float = 2.0 * math.pi * current_radius

            width_if_unchanged: float = current_circumference / previous_count
            ratio: int = max(1, round(width_if_unchanged / target_arc_length))
            cell_count: int = previous_count * ratio

            row: List[Polar_Cell] = [
                Polar_Cell(ring, index)
                for index in range(cell_count)
            ]
            self.grid.append(row)

    def _configure_cells(self) -> None:
        for ring, row in enumerate(self.grid):
            row_count: int = len(row)
            for index, cell in enumerate(row):
                if row_count > 1:
                    cell.clockwise = row[(index + 1) % row_count]
                    cell.counter_clockwise = row[(index - 1) % row_count]
                elif row_count == 1:
                    cell.clockwise = row[0]
                    cell.counter_clockwise = row[0]

                if ring == 0:
                    continue

                previous_row: List[Polar_Cell] = self.grid[ring - 1]
                ratio: int = len(row) // len(previous_row)
                parent: Polar_Cell = previous_row[index // ratio]
                cell.inward = parent
                parent.outward.append(cell)

    def random_cell(self) -> Polar_Cell:
        row: List[Polar_Cell] = random.choice(self.grid)
        return random.choice(row)

    def get_cell(self, ring: int, index: int) -> Optional[Polar_Cell]:
        if not 0 <= ring < self.circle_count:
            return None
        row: List[Polar_Cell] = self.grid[ring]
        if not row:
            return None
        return row[index % len(row)]

    def neighbours(self, of_cell: Polar_Cell, only_unvisited: bool = True) -> List[Polar_Cell]:
        neighbours: List[Polar_Cell] = []
        for candidate in of_cell.adjacent():
            if only_unvisited and candidate.visited:
                continue
            neighbours.append(candidate)
        return neighbours

    def all_cells(self) -> List[Polar_Cell]:
        return [cell for row in self.grid for cell in row]

    def ring_sizes(self) -> List[int]:
        return [len(row) for row in self.grid]

    def __iter__(self) -> Iterator[List[Polar_Cell]]:
        return iter(self.grid)

    def __len__(self) -> int:
        return sum(len(row) for row in self.grid)


