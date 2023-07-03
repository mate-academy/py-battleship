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

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:

        if self.start[0] == self.end[0]:
            if self.start[1] < self.end[1]:
                return self.create_decks_instances(
                    row=self.start[0],
                    start=self.start[1],
                    end=self.end[1],
                    is_row=True
                )

            if self.start[1] == self.end[1]:
                return [(Deck(row=self.start[0], column=self.start[1]))]

            return self.create_decks_instances(
                row=self.start[0],
                start=self.end[1],
                end=self.start[1],
                is_row=True
            )

        if self.start[1] == self.end[1]:
            if self.start[0] < self.end[0]:
                return self.create_decks_instances(
                    row=self.start[1],
                    start=self.start[0],
                    end=self.end[0]
                )

            return self.create_decks_instances(
                row=self.start[1],
                start=self.end[0],
                end=self.start[0]
            )

    @staticmethod
    def create_decks_instances(
            row: int,
            start: int,
            end: int,
            is_row: bool = False
    ) -> list[Deck]:
        decks = []
        for i in range(start, end + 1):
            if is_row:
                decks.append(Deck(row=row, column=i))
                continue
            decks.append(Deck(row=i, column=row))

        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False
                break
        else:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = dict()
        self.create_ships()
        if not self._validate_field():
            print("You should re_create your ships.")
            self.field = dict()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(row=location[0], column=location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def create_ships(self) -> None:
        ships = []
        for location in self.ships:
            ships.append(Ship(start=location[0], end=location[1]))

        for ship in ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def print_field(self) -> None:
        whole_field = dict()
        for i in range(10):
            for index in range(10):
                symbol = "~"
                if (i, index) in self.field:
                    symbol = "□"
                whole_field[(i, index)] = symbol

        for location in whole_field:
            ship = self.field.get(location)
            if ship:
                symbol = "*"
                if ship.is_drowned:
                    symbol = "x"
                for deck in ship.decks:
                    if not deck.is_alive:
                        whole_field[(deck.row, deck.column)] = symbol

        for index, location in enumerate(whole_field):
            if index % 10 == 0:
                print("")
            print(f"{whole_field.get(location)}      ", end="")

    def _validate_field(self) -> bool:
        single_deck_ship = 0
        double_deck_ship = 0
        three_deck_ship = 0
        four_deck_ship = 0

        ships = set([ship for ship in self.field.values()])
        for ship in ships:
            ship_length = len(ship.decks)
            if ship_length == 1:
                single_deck_ship += 1
                continue
            if ship_length == 2:
                double_deck_ship += 1
                continue
            if ship_length == 3:
                three_deck_ship += 1
                continue
            if ship_length == 4:
                four_deck_ship += 1

        if (
                single_deck_ship == 4 and double_deck_ship == 3
                and three_deck_ship == 2 and four_deck_ship == 1
        ):
            if self.check_neighbours_cells(ships):
                return True
        return False

    def check_neighbours_cells(self, ships: set[Ship]) -> bool:
        for ship in ships:
            locations = []
            for deck in ship.decks:
                locations.append((deck.row, deck.column))

            for location in locations:
                if not self.check_cell(locations, location, 0, -1):
                    return False
                if not self.check_cell(locations, location, 1, -1):
                    return False
                if not self.check_cell(locations, location, 1, 0):
                    return False
                if not self.check_cell(locations, location, 1, 1):
                    return False
                if not self.check_cell(locations, location, 0, 1):
                    return False
                if not self.check_cell(locations, location, -1, 1):
                    return False
                if not self.check_cell(locations, location, -1, 0):
                    return False
                if not self.check_cell(locations, location, -1, -1):
                    return False
        return True

    def check_cell(
            self,
            locations: list[tuple],
            location: tuple,
            row: int,
            column: int
    ) -> bool:
        if (location[0] + row, location[1] + column) in self.field:
            if (location[0] + row, location[1] + column) not in locations:
                return False
        return True
