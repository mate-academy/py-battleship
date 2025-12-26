from pprint import pprint


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
            sign: str = u"\u25A1"
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.sign = sign


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def create_decks(self) -> None:
        if self.start[0] == self.end[0]:
            number_of_decks = self.end[1] - self.start[1] + 1
            for ship_part in range(number_of_decks):
                deck = Deck(self.start[0], self.start[1] + ship_part)
                self.decks.append(deck)
        else:
            number_of_decks = self.end[0] - self.start[0] + 1
            for ship_part in range(number_of_decks):
                deck = Deck(self.start[0] + ship_part, self.start[1])
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        corresponding_deck = 0
        for index, deck in enumerate(self.decks):
            if deck.row == row and deck.column == column:
                corresponding_index = index
                corresponding_deck = self.decks[corresponding_index]
        return corresponding_deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        deck = self.get_deck(row, column)
        deck.is_alive = False
        deck.sign = "*"
        # And update the `is_drowned` value if it's needed
        all_decks_are_hit = all(not deck.is_alive for deck in self.decks)
        if all_decks_are_hit:
            self.is_drowned = True

    def deck_length(self) -> int:
        return len(self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in
        self.field = {}
        for ship in self.ships:
            new_ship = Ship(ship[0], ship[1])
            new_ship.create_decks()
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if self.field.get(location):
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                for deck in ship.decks:
                    deck.sign = "x"
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        ships_field = [["~" for i in range(10)] for j in range(10)]
        for row, column in self.field:
            sign = self.field[(row, column)].get_deck(row, column).sign
            ships_field[row][column] = sign
        pprint(ships_field)

    def _validate_field(self) -> bool:
        # the total number of the ships should be 10
        quantity = len(set(self.field.values())) == 10
        # there should be 4 single-deck ships, 3 double-deck ships,
        # 2 three-deck ships, 1 four-deck ship;
        lengths = []
        ships = {x: 1 for x in self.field.values()}
        list_of_neighbors = []
        for ship in ships:
            lengths.append(ship.deck_length())
            # ships shouldn't be located in the neighboring cells
            # (even if cells are neighbors by diagonal)
            if ship.start[0] == ship.end[0]:
                for length in range(ship.deck_length() + 2):
                    list_of_neighbors.append(
                        self.field.get(
                            (
                                ship.start[0] - 1,
                                ship.start[1] - 1 + length
                            )
                        )
                    )
                    list_of_neighbors.append(
                        self.field.get(
                            (
                                ship.start[0] + 1,
                                ship.start[1] - 1 + length
                            )
                        )
                    )
                list_of_neighbors.append(
                    self.field.get(
                        (
                            ship.start[0],
                            ship.start[1] - 1
                        )
                    )
                )
                list_of_neighbors.append(
                    self.field.get(
                        (
                            ship.start[0],
                            ship.end[1] + 1
                        )
                    )
                )
            else:
                for length in range(ship.deck_length() + 2):
                    list_of_neighbors.append(
                        self.field.get(
                            (
                                ship.start[0] - 1 + length,
                                ship.start[1] - 1
                            )
                        )
                    )
                    list_of_neighbors.append(
                        self.field.get(
                            (
                                ship.start[0] - 1 + length,
                                ship.start[1] + 1
                            )
                        )
                    )
                list_of_neighbors.append(
                    self.field.get(
                        (
                            ship.start[0] - 1,
                            ship.start[1]
                        )
                    )
                )
                list_of_neighbors.append(
                    self.field.get(
                        (
                            ship.end[0] + 1,
                            ship.end[1]
                        )
                    )
                )

        sorted_lengths = sorted(lengths)
        dont_have_neighbors = all([
            True for elem in list_of_neighbors if elem is None
        ])

        return all([
            quantity,
            sum(sorted_lengths[:4]) == 4,
            sum(sorted_lengths[4:7]) == 6,
            sum(sorted_lengths[7:9]) == 6,
            sum(sorted_lengths[9:10]) == 4,
            dont_have_neighbors
        ])
