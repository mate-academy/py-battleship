class Deck:

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.add_new_ship()

    def add_new_ship(self) -> None:
        if self.end[0] == self.start[0] and self.end[1] == self.start[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
        elif self.end[0] == self.start[0]:
            for cell in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], cell))
        elif self.end[1] == self.start[1]:
            for cell in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(cell, self.start[0]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if any([decks.is_alive for decks in self.decks]):
            pass
        else:
            self.is_drowned = True


class Battleship:

    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {
            ship: Ship(*ship)
            for ship in self.ships
        }
        self.battle_field = self.create_field()

    def fire(self, location: tuple) -> str:
        for coordinates, ship in self.field.items():
            if location[0] in range(
                coordinates[0][0], coordinates[1][0] + 1
            ) and location[1] in range(
                coordinates[0][1], coordinates[1][1] + 1
            ):
                ship.fire(*location)
                if ship.is_drowned:
                    for deck in ship.decks:
                        self.battle_field[deck.row][deck.column] = "x"
                    return "Sunk!"
                self.battle_field[location[0]][location[1]] = "*"
                return "Hit!"
        self.battle_field[location[0]][location[1]] = "o"
        return "Miss!"

    def create_field(self) -> list:
        battle_field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.field.values():
            for deck in ship.decks:
                battle_field[deck.row][deck.column] = u"\u25A1"
        return battle_field

    def print_field(self) -> None:
        for row in self.battle_field:
            for column in row:
                print(column.rjust(2), end=" ")
            print()
