from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"deck({self.row}, {self.column})"

    def __repr__(self) -> str:
        return f"deck({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self._add_to_decks()
        self.live_decks = len(self.decks)

    def __str__(self) -> str:
        return f"ship({self.start}, {self.end})"

    def __repr__(self) -> str:
        return f"ship(start: {self.start}, finish: {self.end})"

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return True
        return False

    def get_status(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column and deck.is_alive:
                return True
        return False

    def _add_to_decks(self) -> None:
        start_x, start_y = self.start[0], self.start[1]
        end_x, end_y = self.end[0], self.end[1]

        if start_x != end_x:
            for i in range(start_x, end_x + 1):
                start_x = i
                self.decks.append(Deck(start_x, start_y))

        elif start_y != end_y:
            for i in range(start_y, end_y + 1):
                start_y = i
                self.decks.append(Deck(start_x, start_y))

        else:
            self.decks.append(Deck(start_x, start_y))


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = {}
        self._add_ships_to_dict(ships)

    def fire(self, location: tuple) -> str:
        x, y = location[0], location[1]
        for ship in self.ships.values():
            for deck in ship.decks:
                if deck.row == x and deck.column == y:
                    deck.is_alive = False
                    ship.live_decks -= 1
                    if ship.live_decks == 0:
                        ship.is_drowned = True
                        return "Sunk!"
                    return "Hit!"
        else:
            return "Miss!"

    def _add_ships_to_dict(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for ship in ships:
            self.ships[ship] = Ship(ship[0], ship[1])

    def draw_matrix(self, rows: int, columns: int) -> str:
        result = ""

        for column in range(columns):
            for row in range(rows):
                if self.check_deck_status(row, column) == "ship_sunk":
                    result += "x\t"
                elif self.check_deck_status(row, column) == "is_alive":
                    result += u"\u25A1\t"
                elif self.check_deck_status(row, column) == "dead_deck":
                    result += "*\t"
                else:
                    result += "~\t"
            result += "\n"
        return result

    def check_deck_status(self, row: int, column: int) -> bool | str:
        for ship in self.ships.values():
            if ship.get_deck(row, column):
                if ship.live_decks == 0:
                    return "ship_sunk"
                if ship.get_status(row, column):
                    return "is_alive"
                return "dead_deck"
        return False
