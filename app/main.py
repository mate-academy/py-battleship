from app.classes.ship import Ship
from app.tools.neighbor_checker import check_neighbours_free


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {cell: Ship(*cell) for cell in ships}
        self._validate_field()
        self._print_field = [["~" for _ in range(10)] for _ in range(10)]

    def _validate_field(self) -> None:
        self.check_len(self.field)
        self.check_set(self.field)
        self.check_near_cells(self.field)

    @classmethod
    def check_len(cls, data: dict) -> None | Exception:
        if len(data) != 10:
            raise Exception("Number of ships must be 10!")

    @classmethod
    def check_set(cls, data: dict) -> None | Exception:
        len_ships = [len(ship.decks) for ship in data.values()]
        for len_ship in len_ships:
            key = len(Ship.ship_set) - len_ship
            if len_ships.count(len_ship) != key:
                raise Exception(
                    f"There should be {key} {Ship.ship_set[key]}"
                )

    @classmethod
    def check_near_cells(cls, data: dict) -> None | Exception:
        bin_matrix = [[False for _ in range(10)] for _ in range(10)]
        for row in range(10):
            for col in range(10):
                for ship in data.values():
                    if ship.get_deck(row, col):
                        bin_matrix[row][col] = True

        for ship in data.values():
            for deck in ship.decks:
                if not check_neighbours_free(deck, ship, bin_matrix):
                    raise Exception(
                        "Ship can not be placed near other ship!"
                    )

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            row, col = location
            deck = ship.get_deck(row, col)

            if deck and deck.is_alive:
                ship.fire(row, col)
                if not ship.is_drowned:
                    return "Hit!"
                return "Sunk!"

            if deck and not deck.is_alive:
                return "This deck is already hit!"

        if self._print_field[row][col] == "~":
            self._print_field[row][col] = u"\U0001F6C7"
            return "Miss!"
        return "This cell is already hit and missed!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                for ship in self.field.values():
                    deck = ship.get_deck(row, col)
                    if deck:
                        self._print_field[row][col] = deck._sign

        for row in self._print_field:
            for cell in row:
                print(cell, end=" " * 2)
            print("")
