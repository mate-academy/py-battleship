from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.colum = column
        self.is_alive = is_alive
        self.coordinates = (self.row, self.colum)

    def __repr__(self) -> str:
        return f"{self.coordinates}"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for colum in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, colum))

    def __repr__(self) -> str:
        return f"{self.decks}"

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.colum == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.create_field()

    def fire(self, location: tuple) -> str:
        if self.field[location] == "□":
            self.field[location] = "x"
            for ship in self.ships:
                if ship.get_deck(location[0], location[1]):
                    ship.fire(location[0], location[1])
                    if ship.is_drowned:
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"

    def create_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.coordinates] = "□"
        for x_coord in range(0, 10):
            for y_coord in range(0, 10):
                if (x_coord, y_coord) not in self.field:
                    self.field[(x_coord, y_coord)] = "~"

    def print_field(self) -> None:
        for x_coord in range(0, 10):
            new_dict = {}
            for y_coord in range(0, 10):
                new_dict[x_coord, y_coord] = self.field[x_coord, y_coord]
            print("     ".join(list(new_dict.values())))
            del new_dict
