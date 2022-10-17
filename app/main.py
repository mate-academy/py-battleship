class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        ship_length = (end[0] - start[0], end[1] - start[1])
        if ship_length[1] > 0:
            for i in range(ship_length[1] + 1):
                self.decks.append(Deck(start[0], start[1] + i))
        elif ship_length[0] > 0:
            for i in range(ship_length[0] + 1):
                self.decks.append(Deck(start[0] + i, start[1]))
        else:
            self.decks.append(Deck(start[0], start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        all_destroyed = []
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
            all_destroyed.append(not deck.is_alive)

        if all(all_destroyed):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for coords in ships:
            ship = Ship(coords[0], coords[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if (location in self.field.keys()
                and not self.field[location].is_drowned):
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for coords, ship in self.field.items():
            if ship.is_drowned:
                field[coords[0]][coords[1]] = "x"
            else:
                for deck in ship.decks:
                    if ((deck.row, deck.column) == coords
                            and deck.is_alive):
                        field[coords[0]][coords[1]] = "□"
                    elif ((deck.row, deck.column) == coords
                          and not deck.is_alive):
                        field[coords[0]][coords[1]] = "*"
        for row in range(10):
            for column in range(10):
                print(field[row][column], end=" ")
            print()
