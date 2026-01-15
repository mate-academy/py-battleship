from dataclasses import dataclass


class ValidateFieldError(Exception):
    pass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True
    status = u"\u25A1"


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks = []

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            deck.status = "*"
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True
                for deck in self.decks:
                    deck.status = "x"

    def create_new_deck(self) -> None:
        if self.start[0] == self.end[0]:
            decks_number = self.end[1] - self.start[1] + 1
            for ship_deck in range(decks_number):
                created_deck = Deck(self.start[0], self.start[1] + ship_deck)
                self.decks.append(created_deck)
        else:
            decks_number = self.end[0] - self.start[0] + 1
            for ship_deck in range(decks_number):
                created_deck = Deck(self.start[0] + ship_deck, self.start[1])
                self.decks.append(created_deck)

    def get_neighbors(self) -> list:
        neighbors = []
        for deck in self.decks:
            x, y = deck.row, deck.column
            for row in range(-1, 2):
                for column in range(-1, 2):
                    if row != 0 or column != 0:
                        neighbors_x, neighbors_y = x + row, y + column
                        if 0 <= neighbors_x < 10 and 0 <= neighbors_y < 10:
                            neighbors.append((neighbors_x, neighbors_y))
        return neighbors


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship in ships:
            created_ship = Ship(ship[0], ship[1])
            created_ship.create_new_deck()
            for deck in created_ship.decks:
                self.field[(deck.row, deck.column)] = created_ship
        if not self._validate_field():
            raise ValidateFieldError

    def fire(self, location: tuple) -> str:
        battleship = self.field.get(location)
        if battleship:
            battleship.fire(*location)
            if battleship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            output = ""
            for column in range(10):
                deck = self.field.get((row, column))
                if deck:
                    deck = deck.get_deck(row, column)
                    output += f"{deck.status}  "
                    continue
                output += "~  "
            print(output)

    def _validate_field(self) -> bool:
        verdict = True

        ships = list(set(self.field.values()))
        if len(ships) != 10:
            verdict = False

        number_of_decks = {}
        for ship in ships:
            if number_of_decks.get(len(ship.decks)):
                number_of_decks[len(ship.decks)] += 1
            else:
                number_of_decks[len(ship.decks)] = 1
        if not all(
                [
                    number_of_decks[1] == 4,
                    number_of_decks[2] == 3,
                    number_of_decks[3] == 2,
                    number_of_decks[4] == 1
                ]
        ):
            verdict = False

        for first_ship in ships:
            for second_ship in ships:
                if first_ship != second_ship:
                    occupied_coordinate = first_ship.get_neighbors()
                    for deck in second_ship.decks:
                        x, y = deck.row, deck.column
                        if (x, y) in occupied_coordinate:
                            verdict = False

        return verdict
