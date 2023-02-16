from __future__ import annotations


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        self.start = start
        self.end = end
        self.decks_cord = self.ship_building()
        self.kicks = set()

    def ship_building(self) -> tuple:
        if self.start[0] > self.end[0] or self.start[1] > self.end[1]:
            self.start, self.end = self.end, self.start
        cords = []
        for cord_1 in range(self.start[0], self.end[0] + 1):
            for cord_2 in range(self.start[1], self.end[1] + 1):
                cords.append((cord_1, cord_2))
        return tuple(cords)
