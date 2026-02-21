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

        if start == end:
            self.decks.append(Deck(start[0], start[1]))

        elif start[1] == end[1]:
            for coord_row in range(start[0], end[0] + 1):
                self.decks.append(Deck(coord_row, start[1]))

        elif start[0] == end[0]:
            for coord_column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], coord_column))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> bool:
        deck = self.get_deck(row, column)
        if deck is None:
            raise Exception("Error while shooting at the ship!")
        deck.is_alive = False
        for decks in self.decks:
            if decks.is_alive:
                return False
        self.is_drowned = True
        return True


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field = {}
        for item_ship in ships:
            if ((item_ship[0][0] not in range(0, 10)
                or item_ship[0][1] not in range(0, 10))
                    or item_ship[1][0] not in range(0, 10)
                    or item_ship[1][1] not in range(0, 10)):
                raise ValueError("Location of ship is incorrect!")
            ship = Ship(item_ship[0], item_ship[1])
            for cell in ship.decks:
                if self.field.get((cell.row, cell.column)):
                    raise ValueError(
                        f"Cell {(cell.row, cell.column)} is already used!"
                    )
                self.field[(cell.row, cell.column)] = ship

    def fire(
            self,
            location: tuple
    ) -> str:
        if location[0] not in range(0, 10) or location[1] not in range(0, 10):
            raise ValueError("Location is incorrect!")

        if self.field.get(location):
            ship_status = self.field[location].fire(location[0], location[1])
        else:
            return "Miss!"

        if ship_status:
            return "Sunk!"
        else:
            return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if self.field.get((row, column)):
                    if self.field.get((row, column)).is_drowned:
                        print("x", end=" ")
                    else:
                        if self.field.get(
                                (row, column)
                        ).get_deck(row, column).is_alive:
                            print(u"\u25A1", end=" ")
                        else:
                            print("*", end=" ")
                else:
                    print("~", end=" ")
            print("")
