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
            is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.creating_deck_list()

    def creating_deck_list(self) -> list:
        deck_list = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                deck_list.append(Deck(self.start[0], column))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                deck_list.append(Deck(row, self.start[1]))
        return deck_list

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        for coords, ship in self.field.items():
            if coords == location:
                ship.fire(location[0], location[1])
                if not ship.is_drowned:
                    return "Hit!"
                return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if not ship.is_drowned:
                        if deck.is_alive:
                            print(u"\u25A1", end=" ")
                        else:
                            print("*", end=" ")
                    else:
                        print("x", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError
        count_ships = {}
        for ship in self.ships:
            decks = len(ship.decks)
            count_ships[decks] = count_ships.get(decks, 0) + 1
        if count_ships[1] != 4:
            raise ValueError
        if count_ships[2] != 3:
            raise ValueError
        if count_ships[3] != 2:
            raise ValueError
        if count_ships[4] != 1:
            raise ValueError
        for ship in self.ships:
            for deck in ship.decks:
                for row in range(deck.row - 1, deck.row + 2):
                    for column in range(deck.column - 1, deck.column + 2):
                        if (row, column) in self.field:
                            if self.field[(row, column)] != ship:
                                raise ValueError
