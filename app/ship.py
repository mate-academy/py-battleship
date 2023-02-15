from __future__ import annotations


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end

        if self.start[0] == self.end[0]:
            if start[1] < end[1]:
                self.decks_cord = tuple(
                    (self.start[0], i)
                    for i in range(self.start[1], self.end[1] + 1)
                )

            else:
                self.decks_cord = tuple(
                    (self.start[0], i)
                    for i in range(self.end[1], self.start[1] + 1)
                )

        if self.start[1] == self.end[1]:
            if start[0] < end[0]:
                self.decks_cord = tuple(
                    (i, self.start[1])
                    for i in range(self.start[0], self.end[0] + 1)
                )

            else:
                self.decks_cord = tuple(
                    (i, self.start[1])
                    for i in range(self.end[0], self.start[0] + 1)
                )
        self.kicks = set()
