class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.coordinates = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], decks)
                for decks in range(start[1], end[1] + 1)
            ]
        elif start[1] == end[1]:
            self.decks = [
                Deck(decks, end[1])
                for decks in range(start[0], end[0] + 1)
            ]
        elif start[0] != end[0] and start[1] == end[1]:
            raise ValueError("Please enter correct value")
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.coordinates[0] == row and deck.coordinates[1] == column:
                return deck

    def check_all_drown_decks(self) -> bool:
        return not any(deck.is_alive for deck in self.decks)

    def repack_decks(self) -> dict:
        return {
            deck.coordinates: self
            for deck in self.decks
        }

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if self.check_all_drown_decks():
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            some_ship = Ship(*ship)
            self.field.update(
                Ship.repack_decks(some_ship)
            )

    def fire(self, location: tuple) -> str:
        if location not in self.field or self.field[location].is_drowned:
            return "Miss!"
        ship_to_strike = self.field[location]
        if ship_to_strike.is_drowned is False:
            ship_to_strike.fire(*location)
            if Ship.check_all_drown_decks(ship_to_strike):
                return "Sunk!"
            else:
                return "Hit!"
