class Deck:
    def __init__(self, row: int, column: int, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
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

    def fire(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = self.creating_ship_dict()

    def creating_ship_dict(self) -> dict:
        ship_dict = {}
        ships_list = [Ship(ship_t[0], ship_t[1]) for ship_t in self.ships]
        for ship in ships_list:
            for cell in ship.decks:
                ship_dict[(cell.row, cell.column)] = ship
        return ship_dict

    def fire(self, location: tuple) -> None:
        for coords, ship in self.field.items():
            if coords == location:
                ship.fire(location[0], location[1])
                if not ship.is_drowned:
                    print("Hit!")
                    return
                print("Sunk!")
                return
        print("Miss!")