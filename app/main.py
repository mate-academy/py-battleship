from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_ships()

    def create_ships(self) -> list[Deck]:
        decks = [
            Deck(row, column) for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.update_drowned_status()

    def update_drowned_status(self) -> None:
        alive_decks = [deck for deck in self.decks if deck.is_alive]
        if not alive_decks:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:

        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    if any(deck.is_alive for deck in ship.decks):
                        print(u"\u25A1", end="\t")
                    else:
                        print("x", end="\t")
                else:
                    print("~", end="\t")
            print()


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )

    printer = battle_ship

    printer.print_field()

    print(
        battle_ship.fire((0, 4)),  # Miss!
        battle_ship.fire((0, 3)),  # Hit!
        battle_ship.fire((0, 2)),  # Hit!
        battle_ship.fire((0, 1)),  # Hit!
        battle_ship.fire((0, 0)),  # Sunk!
    )
