class Deck:
    def __init__(
            self,
            row: tuple,
            column: tuple,
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

        self.start = Deck(start[0], start[1])
        self.end = Deck(end[0], end[1])
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        intermediate_coordinates = []

        if self.start.row == self.end.row:
            intermediate_coordinates = [
                (self.start.row, col) for col in range(
                    self.start.column, self.end.column + 1)]

        elif self.start.column == self.end.column:
            intermediate_coordinates = [
                (row, self.start.column) for row in range(
                    self.start.row, self.end.row + 1)]

        for coord in intermediate_coordinates:
            decks_instance = Deck(coord[0], coord[1])
            self.decks.append(decks_instance)

    def get_deck(self, row: tuple, column: tuple) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: tuple, column: tuple) -> None:
        hit_deck = self.get_deck(row, column)

        if hit_deck and hit_deck.is_alive:
            hit_deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int]]]) -> None:
        self.ships = ships
        self.field = {}
        self.create_field()

    def create_field(self) -> None:
        instance_of_ships = [Ship(inst[0], inst[1]) for inst in self.ships]

        for ship in instance_of_ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple) -> str:

        if location in self.field.keys():
            fired_ship = self.field.get(location)

            hit_deck = fired_ship.get_deck(location[0], location[1])

            if hit_deck and hit_deck.is_alive:
                hit_deck.is_alive = False

                if all(not deck.is_alive for deck in fired_ship.decks):
                    fired_ship.is_drowned = True
                    return "Sunk!"
                else:
                    return "Hit!"
        else:
            return "Miss!"
