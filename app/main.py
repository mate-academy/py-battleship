from typing import Tuple, List


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
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.get_decks_list(start, end)

    @staticmethod
    def get_decks_list(
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> List[Deck]:
        deck_list = []
        if start[0] != end[0]:
            for i in range(start[0], end[0] + 1):
                deck_list.append(Deck(i, start[1]))
        else:
            for i in range(start[1], end[1] + 1):
                deck_list.append(Deck(start[0], i))
        return deck_list

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return "Hit!"
            self.is_drowned = True
            return "Sunk!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship_coordinates in ships:
            ship = Ship(*ship_coordinates)
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

        self._validate()

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            result_string = self.field[location].fire(*location)
            self.print_field()
            return result_string
        return "Miss!"

    def _validate(self) -> None:
        ships = set(self.field.values())

        # list with count of different ships,
        # different_ships_count[index + 1] = count of index-deck ships
        different_ships_count = [0] * 4

        for ship in ships:
            different_ships_count[len(ship.decks) - 1] += 1

        if len(ships) == 10:
            ValueError("the total number of the ships should be 10")

        for index in range(4):
            if different_ships_count[index] == 4 - index:
                ValueError(f"there should be {4 - index} "
                           f"{index + 1}-deck ships")

        for cell in self.field:
            for other_cell in self.field:
                if self.field[cell] != self.field[other_cell]:
                    if (
                            abs(cell[0] - other_cell[0]) < 2
                            and abs(cell[1] - other_cell[1]) < 2
                    ):
                        raise ValueError(
                            "ships "
                            "shouldn't be located in the neighboring cells "
                            "(even if cells are neighbors by diagonal)"
                        )

    def print_field(self) -> None:
        for row in range(9):
            for column in range(9):
                ship = self.field.get((row, column))
                if ship:
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif ship.get_deck(row, column).is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print("")
        print("\n\n\n")
