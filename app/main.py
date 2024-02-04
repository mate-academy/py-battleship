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
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = self._create_ship_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def _create_ship_decks(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[Deck]:
        return [
            Deck(row=row, column=column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.printed_field = [["~" for _ in range(10)] for _ in range(10)]
        self.field = self._create_field(ships)

    def _create_field(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> dict[tuple[tuple[int, int]], Ship]:
        return {
            self._get_ship_coordinates(ship): Ship(start=ship[0], end=ship[1])
            for ship in ships
        }

    def _get_ship_coordinates(self, ship: tuple) -> tuple[tuple[int, int]]:
        start = ship[0]
        end = ship[1]

        return tuple(
            self._get_deck_coordinates_after_initial_marking(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        )

    def fire(self, location: tuple) -> str:
        for coordinates, ship in self.field.items():
            if location in coordinates:
                ship.fire(row=location[0], column=location[1])
                self._mark_actual_deck_status_onto_field(
                    ship=ship, row=location[0], column=location[1]
                )
                return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in self.printed_field:
            print(" ".join(row))

    def _get_deck_coordinates_after_initial_marking(
            self,
            row: int,
            column: int
    ) -> tuple[int, int]:
        self.printed_field[row][column] = u"\u25A1"
        return row, column

    def _mark_actual_deck_status_onto_field(
            self,
            ship: Ship,
            row: int,
            column: int
    ) -> None:
        if ship.is_drowned:
            for deck in ship.decks:
                self.printed_field[deck.row][deck.column] = "x"
        else:
            self.printed_field[row][column] = "*"
