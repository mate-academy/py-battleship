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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        is_rowed_ship = self.start[0] == self.end[0]

        if is_rowed_ship:
            column_coord = self.start[-1]

            while column_coord <= self.end[-1]:
                self.decks.append(
                    Deck(self.start[0], column_coord)
                )

                column_coord += 1
        else:
            row_coord = self.start[0]

            while row_coord <= self.end[0]:
                self.decks.append(
                    Deck(row_coord, self.start[-1])
                )

                row_coord += 1

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {
            ship: Ship(ship[0], ship[-1])
            for ship in ships
        }

    def fire(self, location: tuple) -> str:
        row, column = location

        for ship in self.field.values():
            fired_deck = ship.get_deck(row, column)

            if fired_deck:
                ship.fire(row, column)

                for deck in ship.decks:
                    if deck.is_alive:
                        return "Hit!"

                return "Sunk!"

        return "Miss!"
