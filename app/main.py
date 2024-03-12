class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.image: str = f"'{u"\u25A1"}'"

    def __repr__(self) -> str:
        return self.image


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, end[1]))

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple[int]]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            coordinates = []
            for deck in ship.decks:
                coordinates.append((deck.row, deck.column))
            self.field[*coordinates] = ship
        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValueError("Invalid number of ships."
                             " There should be 10 ships.")

        single_deck = double_deck = three_deck = four_deck = 0
        for coordinates in self.field.keys():
            if len(coordinates) == 4:
                four_deck += 1
            if len(coordinates) == 3:
                three_deck += 1
            if len(coordinates) == 2:
                double_deck += 1
            if len(coordinates) == 1:
                single_deck += 1

        if four_deck != 1:
            raise ValueError("Invalid number of four-deck ships."
                             " It must be 1 four-deck ship")
        if three_deck != 2:
            raise ValueError("Invalid number of three-deck ships."
                             " It must be 2 three-deck ship")
        if double_deck != 3:
            raise ValueError("Invalid number of double-deck ships."
                             " It must be 3 double-deck ship")
        if single_deck != 4:
            raise ValueError("Invalid number of single-deck ships."
                             " It must be 4 single-deck ship")

        coordinates_list = [coordinates for coordinates in self.field.keys()]
        for index in range(len(coordinates_list) - 1):
            first_ship = coordinates_list[index]
            second_ship = coordinates_list[index + 1]
            if self._are_ships_neighbors(first_ship, second_ship):
                raise ValueError("Ships cannot be neighbors."
                                 " One cell spacing is required.")

    @staticmethod
    def _are_ships_neighbors(
            coordinates_first_ship: list[int],
            coordinates_second_ship: list[int]
    ) -> bool:
        dangerous_cells = []
        if coordinates_first_ship[0][0] == coordinates_first_ship[-1][0]:
            row = coordinates_first_ship[0][0]
            start = coordinates_first_ship[0][1] - 1
            end = coordinates_first_ship[-1][1] + 2
            for i in range(start, end):
                dangerous_cells.append((row + 1, i))
                dangerous_cells.append((row - 1, i))
            dangerous_cells.append((row, start))
            dangerous_cells.append((row, end - 1))
        else:
            column = coordinates_first_ship[0][1]
            start = coordinates_first_ship[0][0] - 1
            end = coordinates_first_ship[-1][0] + 2
            for i in range(start, end):
                dangerous_cells.append((i, column + 1))
                dangerous_cells.append((i, column - 1))
            dangerous_cells.append((start, column))
            dangerous_cells.append((end - 1, column))

        for coordinate in coordinates_second_ship:
            if coordinate in dangerous_cells:
                return True
        return False

    def fire(self, location: tuple[int]) -> str:
        for coordinates, ship in self.field.items():
            if location in coordinates:
                ship.fire(*location)
                if not ship.is_drowned:

                    for deck in ship.decks:
                        if (deck.row, deck.column) == location:
                            deck.image = "'*'"
                    return "Hit!"

                for deck in ship.decks:
                    deck.image = "'x'"
                return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            for deck in ship.decks:
                field[deck.row][deck.column] = deck

        for row in field:
            print(row)
