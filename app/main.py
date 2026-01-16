from typing import List, Tuple


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]])\
            -> None:
        self.ship_fields = {}
        self.field = {}
        self.next_id = 0

        for start, end in ships:
            coordinates = []

            if start[0] == end[0]:
                for column in range(min(start[1], end[1]),
                                    max(start[1], end[1]) + 1):
                    coordinates.append((start[0], column))
            elif start[1] == end[1]:
                for row in range(min(start[0], end[0]),
                                 max(start[0], end[0]) + 1):
                    coordinates.append((row, start[1]))

            ship_id = self.next_id
            self.next_id += 1

            self.ship_fields[ship_id] = coordinates.copy()
            for coordinate in coordinates:
                self.field[coordinate] = ship_id

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship_id = self.field[location]

        if location in self.ship_fields[ship_id]:
            self.ship_fields[ship_id].remove(location)

        if not self.ship_fields[ship_id]:
            return "Sunk!"
        else:
            return "Hit!"
