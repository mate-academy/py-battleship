class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.cell = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = [
            Deck(j, i)
            for j in range(start[0], end[0] + 1)
            for i in range(start[1], end[1] + 1)
        ]

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.cell == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if any(deck.is_alive for deck in self.decks):
            return "Hit!"

        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {
            ship: Ship(*ship) for ship in ships
        }

        self.field_matrix = [["~" for _ in range(10)] for _ in range(10)]

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            for deck in ship.decks:
                if location == deck.cell:
                    return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    self.field_matrix[deck.cell[0]][deck.cell[1]] = "X"
                elif deck.is_alive:
                    self.field_matrix[deck.cell[0]][deck.cell[1]] = u"\u25A1"
                else:
                    self.field_matrix[deck.cell[0]][deck.cell[1]] = "*"

        for row in self.field_matrix:
            for cell in row:
                print(cell, end="    ")
            print()
