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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(row, col)
            for col in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        if deck := self.get_deck(row, column):
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {
            ship: Ship(*ship) for ship in ships
        }

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                cell_occupied = False
                for ship in self.field.values():
                    if deck := ship.get_deck(row, col):
                        cell_occupied = True
                        if ship.is_drowned:
                            print("X", end=" ")
                            break
                        if deck.is_alive:
                            print(u"\u25A1", end=" ")
                        else:
                            print("*", end=" ")
                if not cell_occupied:
                    print("~", end=" ")
            print()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"

        return "Miss!"
