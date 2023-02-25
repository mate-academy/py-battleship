class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    matrix = [[" ~ " for j in range(10)] for _ in range(10)]
    decks = []

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.neighbors = False

    def set_decks(self) -> None:
        deck = []
        if self.start[0] == self.end[0]:
            for column_index in range(self.end[1], self.start[1] - 1, -1):
                deck.append(Deck(self.start[0], column_index))
                self.matrix[self.start[0]][int(column_index)] = u" \u25A1 "
                self._validate_field(self.start[0], column_index)
            self.decks.append(deck)

        elif self.start[1] == self.end[1]:
            for row_index in range(self.start[0], self.end[0] + 1):
                deck.append(Deck(row_index, self.start[1]))
                self.matrix[int(row_index)][self.start[1]] = u" \u25A1 "
                self._validate_field(row_index, self.start[1])
            self.decks.append(deck)

        elif self.start[0] != self.end[0] and self.start[1] != self.end[1]:
            self.neighbors = True

    def _validate_field(self, row_audit: int, column_audit: int) -> None:
        exist = u" \u25A1 "
        if row_audit != 0 \
                and self.matrix[row_audit - 1][column_audit] == exist \
                and row_audit - 1 < self.start[0]:
            self.neighbors = True
        elif row_audit != 9 \
                and self.matrix[row_audit + 1][column_audit] == exist \
                and row_audit + 1 > self.end[0]:
            self.neighbors = True
        elif column_audit != 0 \
                and self.matrix[row_audit][column_audit - 1] == exist \
                and column_audit - 1 < self.start[1]:
            self.neighbors = True
        elif column_audit != 9 \
                and self.matrix[row_audit][column_audit + 1] == exist \
                and column_audit + 1 > self.end[1]:
            self.neighbors = True

        elif row_audit != 0 \
                and column_audit != 0 \
                and self.matrix[row_audit - 1][column_audit - 1] == exist \
                and row_audit - 1 < self.start[0] \
                and column_audit - 1 < self.start[1]:
            self.neighbors = True
        elif row_audit != 0 \
                and column_audit != 9 \
                and self.matrix[row_audit - 1][column_audit + 1] == exist \
                and row_audit - 1 < self.start[0] \
                and column_audit + 1 > self.end[1]:
            self.neighbors = True
        elif row_audit != 9 \
                and column_audit != 0 \
                and self.matrix[row_audit + 1][column_audit - 1] == exist \
                and row_audit + 1 > self.end[0] \
                and column_audit - 1 < self.start[1]:
            self.neighbors = True
        elif row_audit != 9 \
                and column_audit != 9 \
                and self.matrix[row_audit + 1][column_audit + 1] == exist \
                and row_audit + 1 > self.end[0] \
                and column_audit + 1 > self.end[1]:
            self.neighbors = True

    def fire(self, row: int, column: int) -> str:
        ship_number = -1
        for ship_is_attacked in range(len(self.decks)):
            for deck in self.decks[ship_is_attacked]:
                if deck.row == row and deck.column == column:
                    deck.is_alive = False
                    self.matrix[row][column] = " * "
                    ship_number = ship_is_attacked
                    for deck_alive in self.decks[ship_number]:
                        if deck_alive.is_alive is True:
                            self.is_drowned = False
                            return "Hit!"
                    self.is_drowned = True
                    return "Sunk!"
        if ship_number == -1:
            return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = self.set_field()

    def set_field(self) -> dict:
        field = {}
        for ship in self.ships:
            field[ship] = Ship(ship[0], ship[1])
            field[ship].set_decks()
        return field

    @staticmethod
    def print_matrix() -> None:
        for index_matrix in range(10):
            print(" ".join(Ship.matrix[index_matrix]))

    def fire(self, location: tuple) -> str:
        for find_ship in self.field.keys():
            if location[0] >= find_ship[0][0] \
                    and location[0] <= find_ship[1][0] \
                    and location[1] >= find_ship[0][1] \
                    and location[1] <= find_ship[1][1]:
                return self.field[find_ship].fire(location[0], location[1])
        return "Miss!"

    def audit_neighbors(self) -> bool:
        for audit in self.field.values():
            if audit.neighbors is True:
                return True

    @staticmethod
    def count_ships() -> bool:
        single_deck = 0
        double_deck = 0
        three_deck = 0
        four_deck = 0

        if len(Ship.decks) != 10:
            return False

        for count_ship in Ship.decks:
            if len(count_ship) == 1:
                single_deck += 1
            elif len(count_ship) == 2:
                double_deck += 1
            elif len(count_ship) == 3:
                three_deck += 1
            elif len(count_ship) == 4:
                four_deck += 1

        if single_deck != 4 \
                or double_deck != 3 \
                or three_deck != 2 \
                or four_deck != 1:
            return False


if __name__ == "__main__":
    # input_ships = []
    # print("Enter 10 ship coordinates: ")
    # for index in range(10):
    #     print(f"Ship number {index + 1}")
    #     start = input("Enter the starting coordinates of the ship: ")
    #     end = input("Enter the ending coordinates of the ship: ")
    #     input_ships.append((
    #         (int(start[0]), int(start[-1])),
    #         (int(end[0]), int(end[-1]))
    #     ))
    # battle_ship = Battleship(input_ships)
    battle_ship = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )
    battle_ship.print_matrix()
    while True:
        if battle_ship.audit_neighbors() is True:
            print("Ships shouldn't be located in the neighboring "
                  "cells (even if cells are neighbors by diagonal).")
            break
        elif battle_ship.count_ships() is False:
            print("The total number of the ships should be 10")
            print("there should be 4 single-deck ships;")
            print("there should be 3 double-deck ships;")
            print("there should be 2 three-deck ships;")
            print("there should be 1 four-deck ship;")
            break
        print("Enter the coordinates for the fire:")
        row_value = input("Input row: ")
        column_value = input("Input column: ")
        if row_value == "stop" or column_value == "stop":
            print("GAME OVER")
            break
        print(battle_ship.fire((int(row_value), int(column_value))))
        battle_ship.print_matrix()

        drowned = []
        for ship in battle_ship.field.values():
            drowned.append(ship.is_drowned)
        if all(drowned):
            print("All ships are drowned")
            break
