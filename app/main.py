from __future__ import annotations


class ShipTouchError(Exception):
    pass


class NotEqualToTenError(Exception):
    pass


class WrongAmountOfShipTypes(Exception):
    pass


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
        self.decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str | None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"
        return None

    @property
    def is_drowned(self) -> bool:
        return not any([deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(*ship)
        self.neighbours = []
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            result = ship.fire(*location)
            if result:
                return result
        return "Miss!"

    def print_field(self) -> None:
        screen = [["~" for _ in range(0, 10)] for __ in range(0, 10)]
        for ship in self.field.values():
            for deck in ship.decks:
                if deck.is_alive:
                    screen[deck.row][deck.column] = "□"
                else:
                    screen[deck.row][deck.column] = "x"
        for elem in self.neighbours:
            screen[elem[0]][elem[1]] = "O"
        for row in screen:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise NotEqualToTenError("There must be 10 ships on the field")
        check = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.field.values():
            check[len(ship.decks)] += 1
        if check[1] != 4 or check[2] != 3 or check[3] != 2 or check[4] != 1:
            raise WrongAmountOfShipTypes(
                "There must be 4 one deck ships, three 2 deck ships,"
                "two 3 deck ships and one 4 deck ship"
            )
        for ship in self.field.values():
            ship_neighbours = []
            for deck in ship.decks:
                raw_neighbours = [
                    (deck.row - 1, deck.column - 1),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column - 1),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column - 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column + 1),
                ]
                clean_neighbours = [
                    elem for elem in raw_neighbours if
                    0 <= elem[0] <= 9
                    and 0 <= elem[1] <= 9
                ]
                ship_neighbours.extend(clean_neighbours)
            ship_neighbours = set(ship_neighbours)
            for deck in ship.decks:
                if (deck.row, deck.column) in ship_neighbours:
                    ship_neighbours.remove((deck.row, deck.column))
            self.neighbours.extend(ship_neighbours)
        for ship in self.field.values():
            for deck in ship.decks:
                if (deck.row, deck.column) in self.neighbours:
                    raise ShipTouchError("Ships shouldn't touch each other")
