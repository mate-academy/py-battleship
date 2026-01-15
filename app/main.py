class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.deck_sym = u"\u22A1"


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`

        self.is_drowned = is_drowned
        self.decks = self.create_decks(start, end)

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        self.get_deck(row, column).deck_sym = u"\u22C7"
        self.is_drowned = not any(deck.is_alive for deck in self.decks)

    @staticmethod
    def create_decks(
            start: tuple[int],
            end: tuple[int]
    ) -> list[Deck]:
        decks_list = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                decks_list.append(Deck(start[0], i))
        else:
            for i in range(start[0], end[0]):
                decks_list.append(Deck(i, start[1]))
        return decks_list


class Battleship:
    def __init__(
            self,
            ships: list[tuple]
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(*ship) for ship in ships]
        self.field = self.create_field()
        self._validate_field()

        self.wave_sym = u"\u224B"

    def fire(
            self,
            location: tuple
    ) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            if self.field[location].get_deck(*location).is_alive:
                self.field[location].fire(*location)
                if self.field[location].is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        else:
            return "Miss!"

    def create_field(
            self,
    ) -> dict:
        field = {}

        for ship in self.ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def print_field(self) -> None:
        for row in range(10):
            for clmn in range(10):
                if (row, clmn) in self.create_field():
                    print(
                        self.field[(row, clmn)].get_deck(row, clmn).deck_sym,
                        end="\t"
                    )
                else:
                    print(self.wave_sym, end="\t")
            print("\n")

    def _validate_field(self) -> None:
        ships = list(self.field.values())
        if len(set(ships)) < 10:
            raise ValueError
        valid_comb = [1, 1, 1, 1, 2, 2, 2, 2, 3, 4]
        if sorted([len(ship.decks) for ship in set(ships)]) != valid_comb:
            raise ValueError

        for pos1 in self.field:
            for pos2 in self.field:
                if self.field[pos1] != self.field[pos2]:
                    dist = (pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2
                    if dist ** (1 / 2) < 1.5:
                        raise ValueError
