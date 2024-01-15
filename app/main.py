from typing import List


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.ship = []
        self.is_drowned = is_drowned
        self.deck()

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.ship:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        current_deck = self.get_deck(row, column)
        current_deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.ship)

    def deck(self) -> None:
        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                deck = Deck(row, column)
                self.ship.append(deck)


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.ship:
                self.field[(deck.row, deck.column)] = new_ship
        self.field_ship = {num: ["~"] * 10 for num in range(10)}
        self.location_ship = []
        self._ships_place()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            for deck in ship.ship:
                self.field_ship[deck.row][deck.column] = "X"
            return "Sunk!"
        self.field_ship[location[0]][location[1]] = "*"
        return "Hit!"

    def _ships_place(self) -> None:
        print(self.field)
        for start, end in self.ships:
            ship_pos = Ship(start, end)
            for ship in ship_pos.ship:
                self.location_ship.append(ship)
                self.field_ship[ship.row][ship.column] = "□"

    def print_field(self) -> None:
        for row in self.field_ship:
            print("    ".join(self.field_ship[row]))
