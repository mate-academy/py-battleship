from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.deck = []

    def create_ship(self) -> None:
        for coord_x in range(
                self.start[0], self.end[0] + 1
        ):

            for coord_y in range(self.start[1], self.end[1] + 1):
                # if self.end[0] - self.start[0] >= 5 or self.end[1] - self.start[1] >= 5:
                #     raise ValueError("Invalid ship size")
                if coord_x == self.start[0] or coord_y == self.start[1]:
                    self.deck.append(Deck(coord_x, coord_y))

    def get_deck(self, row: tuple, column: tuple) -> tuple:
        for deck in self.deck:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: tuple, column: tuple) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            if all(not d.is_alive for d in self.deck):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = ships
        self.field = {}

    def create_battle_field(self, ships: List[tuple]) -> None:
        square = "\u25A1"
        game_field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in ships:

            boat = Ship(ship[0], ship[1])
            (row1, column1), (row2, column2) = ship
            if row1 == row2:
                for column in range(column1, column2 + 1):
                    game_field[row1][column] = square
                    self.field[(row1, column)] = boat
            else:
                for row1 in range(row1, row2 + 1):
                    game_field[row1][column1] = square
                    self.field[(row1, column1)] = boat

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])

            # Оцінюємо, чи потоплений корабель
            if ship.is_drowned:
                return "Sunk"
            else:
                return "Hit!"


battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)

battle_ship.create_battle_field(battle_ship.ships)


print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)
