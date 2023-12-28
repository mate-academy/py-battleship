from typing import List, Tuple


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.is_alive = is_alive
        self.row = row
        self.column = column


class Ship:
    def __init__(
            self,
            start: Tuple[int],
            end: Tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [Deck(row, column) for row in
                      range(self.start[0], self.end[0] + 1)
                      for column in range(self.start[1], self.end[1] + 1)]

    def generate_decks(self) -> list:
        start = self.start
        end = self.end
        ship = []
        if start[0] == end[0]:
            for hor_coord in range(start[1], end[1] + 1):
                ship.append(Deck(start, hor_coord))
        elif start[1] == end[1]:
            for vert_coord in range(start[0], end[0] + 1):
                ship.append(Deck(vert_coord, end))
        else:
            raise ValueError("Invalid ship coordinates")
        return ship

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = []
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        print(len(self.ships))
        if len(self.ships) != 10:
            raise ValueError("less ships on the field")

        counter = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            for deck in ship.decks:
                if deck.row == ship.decks[0] and \
                        deck.column == ship.decks[0].column:
                    raise ValueError("This position is wrong to create a ship")

            if len(ship.decks) == 4:
                counter[4] += 1
            elif len(ship.decks) == 3:
                counter[3] += 1
            elif len(ship.decks) == 2:
                counter[2] += 1
            else:
                counter[1] += 1
        print(f"we have {counter[4]} four-decks ships")
        print(f"we have {counter[3]} three-decks ships")
        print(f"we have {counter[2]} two-decks ships")
        print(f"we have {counter[1]} one-decks ships")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def __str__(self) -> str:
        field_representation = ""
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    for deck in ship.decks:
                        if not deck.is_alive and ship.is_drowned:
                            field_representation += "X"
                        elif not deck.is_alive and not ship.is_drowned:
                            field_representation += "*"
                        else:
                            field_representation += u"\u25A1"
                    else:
                        field_representation += "~"

                field_representation += "\n"

        return field_representation
