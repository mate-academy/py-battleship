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
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))
        else:
            raise ValueError("Ships must be either horizontal or vertical")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            return True
        return False

    def is_sunk(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            if ship.fire(location[0], location[1]):
                if not ship.is_sunk():
                    return "Hit!"
                ship.is_drowned = True
                return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        field_size = 10
        field = [["~" for _ in range(field_size)] for _ in range(field_size)]

        for (row, column), ship in self.field.items():
            if ship.get_deck(row, column).is_alive:
                field[row][column] = "□"
            else:
                field[row][column] = "x"

        for row in field:
            print("\t".join(row))
