from __future__ import annotations

from typing import List, Optional, Set


class Polar_Cell:
    """A maze cell positioned on a polar grid."""

    def __init__(self, ring: int, index: int) -> None:
        self.ring: int = ring
        self.index: int = index
        self.visited: bool = False

        self.clockwise: Optional[Polar_Cell] = None
        self.counter_clockwise: Optional[Polar_Cell] = None
        self.inward: Optional[Polar_Cell] = None
        self.outward: List[Polar_Cell] = []

        self.links: Set[Polar_Cell] = set()

    def connect(self, other: object) -> None:
        """Connect this cell to another polar cell."""
        if not isinstance(other, Polar_Cell):
            raise TypeError("Polar_Cell.connect expects a Polar_Cell instance")

        self.links.add(other)
        other.links.add(self)

    def is_connected_to(self, other: object) -> bool:
        """Return True when this cell is linked to the other cell."""
        return isinstance(other, Polar_Cell) and other in self.links

    def adjacent(self) -> List[Polar_Cell]:
        """Return all geometrically adjacent cells."""
        neighbours: List[Polar_Cell] = []
        for candidate in [
            self.clockwise,
            self.counter_clockwise,
            self.inward,
            *self.outward,
        ]:
            if candidate is not None and candidate not in neighbours:
                neighbours.append(candidate)
        return neighbours

    def __repr__(self) -> str:
        return f"Polar_Cell(ring={self.ring}, index={self.index})"

    def __hash__(self) -> int:
        return hash((self.ring, self.index))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Polar_Cell)
            and self.ring == other.ring
            and self.index == other.index
        )
