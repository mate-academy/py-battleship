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
        is_drowned=False
    ) -> None:
                self.decks = [
                    Deck(row, column)
                    for row in range(start[0], end[0] + 1)
                    for column in range(start[1], end[1] + 1)
                ]
                self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        print(f"Get Deck em ({row}, {column})")
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                print(f"Deck retornado: {deck}")
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        print(f"Fire em {deck}")
        if deck is None:
            return None
        if not deck.is_alive:
            return "Already destroyed"
        print(f"Fire - Deck existe e está vivo! Atirar!")
        deck.is_alive = False
        print("Fire - Deck destruído!")
        if any(deck.is_alive for deck in self.decks):
            print("Fire - Existem mais decks! Hit!")
            return "Hit!"
        else:
            print("Fire - Navio afundado! Sunk!")
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
        for row in range(0, 11):
            for column in range(0, 11):
                self.field[(row, column)] = "~"

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = "□"

    def fire(self, location: tuple):
        result = "Miss!"
        for ship in self.ships:
            if (location) in ship.decks:
                result = ship.fire(location[0], location[1])
                if result == "Hit!":
                    self.field[location] = "*"
                elif result == "Sunk!":
                    self.field[location] = "x"
        return result

    def print_field(self) -> None:
        for row in range(0, 11):
            text = ""
            for column in range(0, 11):
                text += f" {self.field[(row, column)]}"
            print(text)
