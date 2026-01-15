class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.decks = self._create_decks()
        self.is_drowned = False

    def _create_decks(self) -> list[Deck]:
        decks = []

        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))

        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for ship_coords in ships:
            ship = Ship(ship_coords[0], ship_coords[1])
            self._add_ship_to_field(ship)

        self._validate_field()

    def _add_ship_to_field(self, ship: Ship) -> None:
        for deck in ship.decks:
            self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        field_representation = [["~"] * 10 for _ in range(10)]

        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)
            if not deck.is_alive and ship.is_drowned:
                field_representation[row][column] = "x"
            elif not deck.is_alive:
                field_representation[row][column] = "*"
            else:
                field_representation[row][column] = u"\u25A1"

        for row in field_representation:
            print(" ".join(row))

    def _validate_field(self) -> None:
        total_ships = len(set(self.field.values()))

        if total_ships != 10:
            raise ValueError(f"Amount of ships must be 10, "
                             f"but {total_ships} is found.")

        ship_sizes = [len(ship.decks) for ship in set(self.field.values())]
        one_deck_ships = ship_sizes.count(1)
        two_deck_ships = ship_sizes.count(2)
        three_deck_ships = ship_sizes.count(3)
        four_deck_ship = ship_sizes.count(4)

        if one_deck_ships != 4:
            raise ValueError(f"Expected 4 one-deck ships, "
                             f"but found {one_deck_ships}.")
        if two_deck_ships != 3:
            raise ValueError(f"Expected 3 two-deck ships, "
                             f"but found {two_deck_ships}.")
        if three_deck_ships != 2:
            raise ValueError(f"Expected 2 three-deck ships, "
                             f"but found {three_deck_ships}.")
        if four_deck_ship != 1:
            raise ValueError(f"Expected 1 four-deck ship, "
                             f"but found {four_deck_ship}.")

        for (row, column), ship in self.field.items():
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    other = (row + dx, column + dy)
                    if other in self.field and self.field[other] != ship:
                        raise ValueError(f"Ships can't be next to each other: "
                                         f"{other} is too close to the ship.")
