from __future__ import annotations


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:

        if not self.__deck_can_be_created(row, column):
            raise RuntimeError(f"Deck ({row}, {column}) can't be created!")

        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"

    def __str__(self) -> str:
        return f"({self.row}, {self.column})"

    def __eq__(self, other: Deck) -> bool:
        return self.row == other.row and self.column == other.column

    @staticmethod
    def __deck_can_be_created(row: int,
                              column: int,) -> bool:
        """
        field should be 10 x 10 size
        """
        if row < 0 or row > 10:
            return False

        if column < 0 or column > 10:
            return False

        return True


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:

        if not self.__ship_can_be_created(start, end):
            raise RuntimeError(f"Ship with coordinates {start} "
                               f"and {end} can't be created!")

        self.decks: list[Deck] = self.__create_ship(start, end)

        self.is_drowned = is_drowned
        self.type = self.__detect_type_of_ship(self.decks)

    def get_deck(self, row: int, column: int) -> Deck | None:
        if self.is_drowned:
            print(f"Ship {self.type} already drowned!")
            return

        deck = Deck(row, column)

        if deck in self.decks:
            return self.decks[self.decks.index(deck)]

        print(f"Ship {self.type} not contain this deck: {deck}!")

    def fire(self, row: int, column: int) -> None:
        if self.is_drowned:
            print(f"Ship {self.type} already drowned!")
            return

        deck = Deck(row, column)

        if deck in self.decks:
            index_of_deck = self.decks.index(deck)
            if self.decks[index_of_deck].is_alive:
                self.decks[index_of_deck].is_alive = False
                self.__check_ship_health()
            else:
                print(f"Deck {deck} already destroyed!")
        else:
            print(f"Ship {self.type} not contain this deck: {deck}!")

    @staticmethod
    def __create_ship(start: tuple,
                      end: tuple) -> list[Deck]:

        ship: list[Deck] = []

        if start[0] < end[0]:
            for index in range(start[0], end[0] + 1):
                ship.append(Deck(index, start[1]))
            return ship

        if start[1] < end[1]:
            for index in range(start[1], end[1] + 1):
                ship.append(Deck(start[0], index))
            return ship

        if start[0] == end[0] and start[1] == end[1] :
            ship.append(Deck(start[0], start[1]))
            return ship

        raise RuntimeError("Error creating ship!!!")

    @staticmethod
    def __ship_can_be_created(deck_1: tuple,
                              deck_2: tuple) -> bool:
        if deck_1[0] != deck_2[0] and deck_1[1] != deck_2[1]:
            return False

        return True

    @staticmethod
    def __detect_type_of_ship(ship: list[Deck]) -> str:
        types = ("Submarine", "Cruiser", "Battleship", "Carrier")
        return types[len(ship) - 1]

    def __check_ship_health(self) -> None:
        for deck in self.decks:
            if deck.is_alive:
                return

        print(f"Ship {self.type} is drowned!")
        self.is_drowned = True

    def __repr__(self) -> str:
        return f"Ship {self.type}, coord: {self.decks}"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.__ships: list[Ship] = self.fill_ships_list(ships)
        self.field: dict[tuple, Ship] = self.__feel_field(self.__ships)
        self.__validate_field()

    @staticmethod
    def fill_ships_list(ships: list[tuple]) -> list[Ship]:
        list_of_ships: list[Ship] = []
        for coordinate in ships:
            list_of_ships.append(Ship(coordinate[0], coordinate[1]))
        return list_of_ships

    def fire(self, location: tuple) -> str:
        if not self.field[location]:
            self.print_field()
            return "Miss!"

        self.field[location].fire(location[0], location[1])

        if self.field[location].is_drowned:
            self.print_field()
            return "Sunk!"
        else:
            self.print_field()
            return "Hit!"

    @staticmethod
    def __feel_field(ships: list[Ship]) -> dict[tuple, Ship | None] :
        field: dict[tuple, Ship | None] = {}

        for ship in ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship

        for i_index in range(10):
            for j_index in range(10):
                _deck = (i_index, j_index)
                if _deck in field.keys():
                    continue
                else:
                    field[_deck] = None

        return field

    def __validate_field(self) -> None:
        """Check the size of the fleet"""
        expected_count_types = {"Submarine": 4,
                                "Cruiser": 3,
                                "Battleship": 2,
                                "Carrier": 1}
        count_types = {"Submarine": 0,
                       "Cruiser": 0,
                       "Battleship": 0,
                       "Carrier": 0}

        for ship in self.__ships:
            count_types[ship.type] += 1

        if count_types != expected_count_types:
            raise AssertionError(
                f"Count ships on battlefield not equal to expected! "
                f"Expected: {expected_count_types}. Actual: {count_types}")

        """Check if the field is filled in correctly"""
        for i_indx in range(10):
            for j_indx in range(10):
                if self.field[(i_indx, j_indx)]:
                    neighbors = [
                        (i_indx, j_indx + 1),
                        (i_indx, j_indx - 1),
                        (i_indx + 1, j_indx),
                        (i_indx - 1, j_indx),
                        (i_indx - 1, j_indx - 1),
                        (i_indx + 1, j_indx + 1),
                        (i_indx + 1, j_indx - 1),
                        (i_indx - 1, j_indx + 1)]
                    for ni, nj in neighbors:
                        if ni != 10 or ni != 0 or nj != 10 or nj != 0:
                            if ((ni, nj) in self.field
                                    and self.field[(ni, nj)]
                                    and (self.field[(i_indx, j_indx)]
                                         != self.field[(ni, nj)])):
                                raise RuntimeError(
                                    f"Ships don't be closer! Conflict deck: "
                                    f"({i_indx}, {j_indx}) and ({ni}, {nj})")

    def print_field(self) -> None:
        if not self.field:
            raise RuntimeError("Field is not feel!!!")

        print("   0  1  2  3  4  5  6  7  8  9 ")

        for i_indx in range(10):
            row = f"{i_indx} "
            for j_indx in range(10):
                _deck = (i_indx, j_indx)
                if not self.field[_deck]:
                    row += " ~ "
                    continue
                if self.field[_deck].is_drowned:
                    row += (" " + u"\u2715" + " ")
                    continue
                if not self.field[_deck].get_deck(i_indx , j_indx).is_alive:
                    row += " * "
                    continue
                if (self.field[_deck].get_deck(i_indx , j_indx).is_alive
                        and not self.field[_deck].is_drowned):
                    row += (" " + u"\u25A1" + " ")
                    continue
            print(row)

        print("----------------------------------")
