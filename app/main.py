class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.colum = column
        self.is_alive = is_alive
        self.coordinates = (self.row, self.colum)

    def __repr__(self) -> str:
        return f"{self.coordinates}"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = Deck(start[0], start[1])
        self.end = Deck(end[0], end[1])
        self.is_drowned = is_drowned
        self.decks = [self.start]
        if self.start.coordinates != self.end.coordinates:
            self.create_list_of_decks()

    def __repr__(self) -> str:
        return f"{self.decks}"

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.colum == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
        if not any([elem.is_alive for elem in self.decks]):
            self.is_drowned = True

    def create_list_of_decks(self) -> None:
        if self.start.row == self.end.row:
            for i in range(self.start.colum + 1, self.end.colum):
                self.decks.append(Deck(self.start.row, i))
        if self.start.colum == self.end.colum:
            for i in range(self.start.row + 1, self.end.row):
                self.decks.append(Deck(i, self.start.colum))
        self.decks.append(self.end)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.create_field()

    def fire(self, location: tuple) -> str:
        if self.field[location] == "□":
            self.field[location] = "x"
            for ship in self.ships:
                if ship.get_deck(location[0], location[1]):
                    ship.fire(location[0], location[1])
                    if ship.is_drowned:
                        return "Sunk!"
                    if not ship.is_drowned and not ship.get_deck(
                            location[0], location[1]
                    ).is_alive:
                        return "Hit!"
        return "Miss!"

    def create_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.coordinates] = "□"
        for i in range(0, 10):
            for el_2 in range(0, 10):
                if (i, el_2) not in self.field:
                    self.field[(i, el_2)] = "~"

    def print_field(self) -> None:
        for i in range(0, 10):
            new_dict = {}
            for el_2 in range(0, 10):
                new_dict[i, el_2] = self.field[i, el_2]
            print("     ".join(list(new_dict.values())))
            del new_dict
