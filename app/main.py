class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (f"Deck ({self.row}, {self.column}) {self.is_alive}")

    def __eq__(self, coordinates: (int, int)) -> bool:
        return (
            coordinates[0] == self.row and coordinates[1] == self.column
        )


class Ship:
    def __init__(
        self,
        start: (int, int),
        end: (int, int),
        is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return None
        if deck.is_alive:
            deck.is_alive = False
            if any(deck.is_alive for deck in self.decks):
                return "Hit!"
            else:
                self.is_drowned = True
                return "Sunk!"
        return "Miss!"


class Battleship:
    def __init__(
        self,
        ships: ((int, int), (int, int))
    ) -> None:
        self.field = {}
        self.ships = [Ship(*ship) for ship in ships]
        for row in range(10):
            for column in range(10):
                self.field[(row, column)] = "~"

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = "□"

    def _validate_field(self) -> bool:
        is_valid = []
        is_valid.append(len(self.ships) == 10)
        is_valid.append(has_x_ships_with_y_decks(4, 1))
        is_valid.append(has_x_ships_with_y_decks(3, 2))
        is_valid.append(has_x_ships_with_y_decks(2, 3))
        is_valid.append(has_x_ships_with_y_decks(1, 4))

    def has_x_ships_with_y_decks(ships_quantity: int, decks_quantity: int) -> bool:
        return sum(
            len(ship.decks) == decks_quantity for ship in self.ships
        ) == ships_quantity
        
    def has_neighboor() -> bool:
        for ship in self.ships:
            around = (-1, 0, 1)
            if ship.start[0] == 0:
                around = (0, 1)
                
            

    def fire(self, location: tuple) -> str:
        result = "Miss!"
        for ship in self.ships:
            if ship.is_drowned:
                result = "Miss!"
            elif (location) in ship.decks:
                result = ship.fire(location[0], location[1])
                if result == "Hit!":
                    self.field[location] = "*"
                elif result == "Sunk!":
                    self.field[location] = "x"
        return result

    def print_field(self) -> None:
        for row in range(10):
            text = ""
            for column in range(10):
                text += f" {self.field[(row, column)]}"
            print(text)
