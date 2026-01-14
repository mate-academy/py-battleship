from app.ship import Ship


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = self.create_ships(ships)
        self.field = self.create_field()
        self._validate_field()

    @staticmethod
    def create_ships(ships: list[tuple]) -> list[Ship]:
        class_ships = []
        for start, end in ships:
            class_ships.append(Ship(start, end))
        return class_ships

    def create_field(self) -> dict:
        field = {}
        for ship in self.ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            is_drowned = ship.fire(location[0], location[1])
            if is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    # creating a game field
    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if not deck.is_alive and ship.is_drowned:
                        print("x   ", end=" ")
                    elif not deck.is_alive:
                        print("*   ", end=" ")
                    else:
                        print(u"\u25A1   ", end=" ")

    # partly-validation
    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Must be 10 whips on a field")

        ship_lengths = [len(ship.decks) for ship in self.ships]

        if ship_lengths.count(1) != 4:
            raise ValueError("Must be 4 single-deck ships")
        if ship_lengths.count(2) != 3:
            raise ValueError("Must be 3 double-deck ships")
        if ship_lengths.count(3) != 2:
            raise ValueError("Must be 2 triple-deck ships")
        if ship_lengths.count(4) != 1:
            raise ValueError("Must be 1 fourth-deck ship")
