from __future__ import annotations

from typing import Dict, Tuple

# Directions: (dx, dy)
DIRS: Dict[str, Tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

OPPOSITE: Dict[str, str] = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


class Cell:
    """Represents a cell in the maze."""

    DIRS: Dict[str, Tuple[int, int]] = DIRS
    OPPOSITE: Dict[str, str] = OPPOSITE

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.walls: Dict[str, bool] = {d: False for d in DIRS}

    def connect(self, other: Cell) -> None:
        """Connect this cell to another cell by removing the wall between them."""
        # Determine direction from self to other
        dx: int = other.x - self.x
        dy: int = other.y - self.y

        for direction, (ddx, ddy) in DIRS.items():
            if ddx == dx and ddy == dy:
                self.walls[direction] = True
                other.walls[OPPOSITE[direction]] = True
                break

    def is_connected_to(self, other: Cell) -> bool:
        """Check if this cell is connected to another cell."""
        dx: int = other.x - self.x
        dy: int = other.y - self.y

        for direction, (ddx, ddy) in DIRS.items():
            if ddx == dx and ddy == dy:
                return self.walls[direction]
        return False

    def get_wall(self, direction: str) -> bool:
        """Get the wall status in the given direction."""
        return self.walls.get(direction, False)

    def set_wall(self, direction: str, open: bool = True) -> None:
        """Set the wall status in the given direction."""
        if direction in self.walls:
            self.walls[direction] = open

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False
