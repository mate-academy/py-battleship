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
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        current_deck = self.get_deck(row, column)
        current_deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def _validate_field(self) -> bool:
        number_of_ships = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in set(self.field.values()):
            number_of_ships[len(ship.decks)] += 1
        return (sum(number_of_ships.values()) == 10
                and number_of_ships[1] == 4
                and number_of_ships[2] == 3
                and number_of_ships[3] == 2
                and number_of_ships[4] == 1)

    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        if not self._validate_field():
            raise ValueError("Invalid fleet configuration.")

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for column in range(0, 10):
                location = (row, column)
                if location not in self.field:
                    print("~", end=" ")
                else:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)
                    if not deck.is_alive and not ship.is_drowned:
                        print("*", end=" ")
                    elif deck.is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("x", end=" ")
            print()
