class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_coordinates(self) -> tuple[int, int]:
        return self.row, self.column

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column})"


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        else:
            ship_position = "horizontal" if start[0] == end[0] else "vertical"
            num_of_middle_decks = abs(end[0] - start[0]
                                      + end[1] - start[1]) - 1
            self.decks.append(Deck(start[0], start[1]))
            for i in range(1, num_of_middle_decks + 1):
                if ship_position == "horizontal":
                    self.decks.append(Deck(start[0], start[1] + i))
                else:
                    self.decks.append(Deck(start[0] + i, start[1]))
            self.decks.append(Deck(end[0], end[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == deck.get_coordinates():
                return deck
        return None

    def is_all_decks_dead(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return False
        return True

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if self.is_all_decks_dead():
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            ship_decks = {deck.get_coordinates(): ship for deck in ship.decks}
            self.field.update(ship_decks)
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        ships = set(self.field.values())
        if len(ships) != 10:
            raise Exception("the total number of the ships should be 10")
        ships_deck_counts = [len(ship.decks) for ship in ships]
        if ships_deck_counts.count(1) != 4:
            raise Exception("the total number of the "
                            "single-deck ships should be 4")
        if ships_deck_counts.count(2) != 3:
            raise Exception("the total number of the "
                            "double-deck ships should be 3")
        if ships_deck_counts.count(3) != 2:
            raise Exception("the total number of the "
                            "three-deck ships should be 2")
        if ships_deck_counts.count(4) != 1:
            raise Exception("the total number of the "
                            "four-deck ships should be 1")
        for location, ship in self.field.items():
            ship_decks = [deck.get_coordinates() for deck in ship.decks]
            for i in range(-1, 2):
                for ii in range(-1, 2):
                    check_location = (location[0] + i, location[1] + ii)
                    if -1 not in check_location:
                        if (check_location in self.field
                                and check_location not in ship_decks):
                            raise Exception("ships shouldn't be located "
                                            "in the neighboring cells")

    def print_field(self) -> None:
        print(" \t0\t1\t2\t3\t4\t5\t6\t7\t8\t9")
        for row in range(10):
            line = f"{row}\t"
            for column in range(10):
                if (row, column) not in self.field:
                    line += "~\t"
                    continue
                ship = self.field[(row, column)]
                if ship.is_drowned:
                    line += "x\t"
                    continue
                if ship.get_deck(row, column).is_alive:
                    line += u"\u25A1\t"
                    continue
                line += "*\t"
            print(line)
