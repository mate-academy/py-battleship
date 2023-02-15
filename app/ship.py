from __future__ import annotations


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.decks_cord = self.ship_building()
        self.kicks = set()

    def ship_building(self) -> tuple:
        if self.start[0] == self.end[0]:
            if self.start[1] < self.end[1]:
                return tuple(
                    (self.start[0], i)
                    for i in range(self.start[1], self.end[1] + 1)
                )
            return tuple(
                (self.start[0], i)
                for i in range(self.end[1], self.start[1] + 1)
            )
        if self.start[1] == self.end[1]:
            if self.start[0] < self.end[0]:
                return tuple(
                    (i, self.start[1])
                    for i in range(self.start[0], self.end[0] + 1)
                )
            return tuple(
                (i, self.start[1])
                for i in range(self.end[0], self.start[0] + 1)
            )
