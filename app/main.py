from __future__ import annotations


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned=False) -> None:
        self.len_ship = round(((start[0] - end[0]
                                )**2 + (start[1] - end[1])**2)**0.5) + 1
        self.ship = [Deck(end[0], end[1] - i)
                     if start[1] < end[1]
                     else Deck(end[0] - i, end[1])
                     for i in range(self.len_ship)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | Ship:
        for ship in self.ships:
            if not ship.is_drowned:
                for decks in ship.ship:
                    if decks.row == row and decks.column == column:
                        return decks, ship

    def fire(self, row: int, column: int) -> str:
        deck, ship = self.get_deck(row, column)
        deck.is_alive = False
        ship.len_ship -= 1
        if ship.len_ship == 0:
            ship.is_drowned = True
            self.ship_drowned(ship.ship)
            return "Sunk!"
        return "Hit!"

    def ship_drowned(self, ship: list) -> None:
        for deck in ship:
            self.field[deck.row][deck.column] = "x"


class Battleship(Ship):
    def __init__(self, ships: list) -> None:
        self.field = [["~"] * 10 for _ in range(10)]
        self.ships = [Ship(start=coords[0], end=coords[1]) for coords in ships]
        self.take_spot()

    def take_spot(self) -> None:
        for ship in self.ships:
            for deck in ship.ship:
                self.field[deck.row][deck.column] = "□"

    def print_field(self) -> None:
        print(*self.field, sep="\n")

    def fire(self, location: tuple) -> str:
        if self.field[location[0]][location[1]] == "□":
            self.field[location[0]][location[1]] = "*" \
                if self.field[location[0]][location[1]] != "x" else "x"
            return super().fire(location[0], location[1])

        return "Miss!"


if __name__ == "__main__":
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

    print(
        battle_ship.fire((0, 4)),  # Miss!
        battle_ship.fire((0, 3)),  # Hit!
        battle_ship.fire((0, 2)),  # Hit!
        battle_ship.fire((0, 1)),  # Hit!
        battle_ship.fire((0, 0)),  # Sunk!
    )
    print(
        battle_ship.fire((9, 7)),
        battle_ship.fire((7, 9)),
        battle_ship.fire((9, 9)),
        battle_ship.fire((2, 8)),
        # battle_ship.fire((2, 9)),
    )

    battle_ship.print_field()
