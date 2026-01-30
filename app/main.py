from collections import Counter


class NumberOfShipsError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.__row = row
        self.__column = column
        self.__is_alive = is_alive

    def __repr__(self) -> str:
        return (f"Deck(row={self.row}, "
                f"column={self.column}, live={self.is_alive})")

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self.__is_alive = is_alive

    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column


class Ship:
    def __init__(self, coordinates: tuple[tuple[int]]) -> None:
        self.__decks = [Deck(*coord) for coord in coordinates]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.__decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def is_last_alive(self, row: int, column: int) -> bool:
        sum_of_alive = sum(deck.is_alive for deck in self.__decks)
        if sum_of_alive > 1:
            return False
        current_deck = self.get_deck(row, column)
        if (sum_of_alive == 1 and current_deck is not None
                and current_deck.is_alive):
            return True

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and self.is_last_alive(row, column):
            deck.is_alive = False
            return "Sunk!"
        if deck and deck.is_alive:
            deck.is_alive = False
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        return str(self.__decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.__field = {}
        for ship in ships:
            self.__fill_ship_key(*ship)

        self._validate_field()

    def __fill_ship_key(self, start: tuple, end: tuple) -> None:
        result_list = []
        if start == end:
            result_list.append((start[0], start[1]))
        elif start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                result_list.append((start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                result_list.append((i, start[1]))

        result_tuple = tuple(result_list)
        self.__field[result_tuple] = Ship(result_tuple)

    def fire(self, location: tuple) -> str:
        for cords in self.__field:
            if location in cords:
                return self.__field[cords].fire(location[0], location[1])

        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.__field) != 10:
            raise NumberOfShipsError(
                f"The total number of the ships should "
                f"be 10, but you have {len(self.__field)}")

        expected_dict = {"1": 4, "2": 3, "3": 2, "4": 1}
        counter = Counter(str(len(cords)) for cords in self.__field)
        if expected_dict != counter:
            raise NumberOfShipsError(
                "In Battleship should be: "
                "\n4 single-deck ships, but you have {}; "
                "\n3 double-deck ships, but you have {}; "
                "\n2 three-deck ships, but you have {}; "
                "\n1 four-deck ship, but you have {};".format(
                    counter["1"], counter["2"], counter["3"], counter["4"]
                )
            )

    def __repr__(self) -> str:
        return str(self.__field)
