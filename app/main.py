from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True
    marker = "\u25A1"


@dataclass
class Ship:
    start: tuple[int, int]
    end: tuple[int, int]
    is_drowned: bool = False

    def __post_init__(self) -> None:
        self.decks = [
            Deck(row, col)
            for row in range(self.start[0], self.end[0] + 1)
            for col in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                deck.marker = "*"

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            for deck in self.decks:
                deck.marker = "x"
            return "Sunk!"
        return "Hit!"


@dataclass
class Battleship:
    ships: list[tuple | Ship]

    def __post_init__(self) -> None:
        self.ships = [Ship(start, end) for start, end in self.ships]
        self.field: dict[tuple, Ship] = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }
        self.battle_field = [["~" for _ in range(10)] for j in range(10)]
        self._validate_field()

    def _validate_field(self) -> None:
        assert len(self.ships) == 10, "Ships should be exactly 10"
        assert sum(1 for ship in self.ships if len(ship.decks) == 1) == 4, (
            "must be 4 ship with 1 deck"
        )
        assert sum(1 for ship in self.ships if len(ship.decks) == 2) == 3, (
            "must be 3 ship with 2 deck"
        )
        assert sum(1 for ship in self.ships if len(ship.decks) == 3) == 2, (
            "must be 2 ship with 3 deck"
        )
        assert sum(1 for ship in self.ships if len(ship.decks) == 4) == 1, (
            "must be 1 ship with 4 deck"
        )
        self._is_ship_near()

    def _is_ship_near(self) -> None:
        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)
            neighbors = [
                (deck.row - 1, deck.column),
                (deck.row + 1, deck.column),
                (deck.row, deck.column - 1),
                (deck.row, deck.column + 1),
                (deck.row - 1, deck.column - 1),
                (deck.row - 1, deck.column + 1),
                (deck.row + 1, deck.column - 1),
                (deck.row + 1, deck.column + 1),
            ]
            for neighbor in neighbors:
                if neighbor in self.field and self.field[neighbor] != ship:
                    raise ValueError("another ship too close")

    def update_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.battle_field[deck.row][deck.column] = deck.marker

    def fire(self, location: tuple) -> str | None:
        if location not in self.field:
            return "Miss!"

        for coords, ship in self.field.items():
            row, column = coords
            if location == coords:
                shot = ship.fire(row, column)
                self.update_field()
                return shot
