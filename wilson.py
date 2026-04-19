from __future__ import annotations

import random
from typing import Dict, List, Protocol, Set, TypeVar

from cell import Cell
from maze import Maze, Maze_Grid, Polar_Grid
from maze_gen_algorithms import Maze_Gen_Algorithm
from polar_cell import Polar_Cell


class LinkableCell(Protocol):
    visited: bool

    def connect(self, other: object) -> None:
        ...

    def __hash__(self) -> int:
        ...


TCell = TypeVar("TCell", bound=LinkableCell)


class Wilson(Maze_Gen_Algorithm):
    """Wilson maze generation algorithm that works for any Maze implementation."""

    def __init__(self) -> None:
        pass

    def __call__(self, maze: Maze[TCell]) -> Maze[TCell]:
        all_cells: List[TCell] = maze.all_cells()
        for cell in all_cells:
            cell.visited = False

        unvisited: Set[TCell] = set(all_cells)

        first: TCell = maze.random_cell()
        first.visited = True
        unvisited.remove(first)

        while unvisited:
            cell: TCell = random.choice(list(unvisited))
            path: List[TCell] = [cell]
            visited_in_walk: Dict[TCell, int] = {cell: 0}

            while cell in unvisited:
                neighbours: List[TCell] = maze.neighbours(cell, only_unvisited=False)
                next_cell: TCell = random.choice(neighbours)

                if next_cell in visited_in_walk:
                    loop_start: int = visited_in_walk[next_cell]
                    path = path[: loop_start + 1]
                    visited_in_walk = {
                        walk_cell: index for index, walk_cell in enumerate(path)
                    }
                else:
                    path.append(next_cell)
                    visited_in_walk[next_cell] = len(path) - 1

                cell = next_cell

            for index in range(len(path) - 1):
                current: TCell = path[index]
                next_cell = path[index + 1]
                current.connect(next_cell)

                if current in unvisited:
                    current.visited = True
                    unvisited.remove(current)

            if path[-1] in unvisited:
                path[-1].visited = True
                unvisited.remove(path[-1])

        return maze


def print_maze(maze: Maze_Grid) -> None:
    width: int = maze.width
    height: int = maze.height

    print("+" + "---+" * width)
    for y in range(height):
        line1: str = "|"
        line2: str = "+"

        for x in range(width):
            cell: Cell = maze.grid[y][x]
            line1 += "   " if cell.walls["E"] else "   |"
            line2 += "   +" if cell.walls["S"] else "---+"

        print(line1)
        print(line2)


def print_polar_summary(maze: Polar_Grid) -> None:
    print("Polar grid ring sizes:", maze.ring_sizes())
    print("Total cells:", len(maze))

    for ring_index, row in enumerate(maze):
        linked_edges: int = sum(len(cell.links) for cell in row)
        print(
            f"ring {ring_index}: cells={len(row)}, linked_edges={linked_edges // 2}"
        )


if __name__ == "__main__":
    rectangular: Maze_Grid = Maze_Grid(10, 10)
    Wilson()(rectangular)
    print_maze(rectangular)

    print()

    polar: Polar_Grid = Polar_Grid(circle_count=6, inner_circle_cells=6)
    Wilson()(polar)
    print_polar_summary(polar)
