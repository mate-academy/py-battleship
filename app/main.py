from typing import Tuple, List


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self,
                 start: Tuple[int],
                 end: Tuple[int],
                 is_drowned: bool = False
                 ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                self.decks.append(Deck(x, y))
        self.length = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck

    def fire(self, row: int, column: int) -> None:
        target = self.get_deck(row, column)
        target.is_alive = False

        are_alive = False
        for deck in self.decks:
            if deck.is_alive:
                are_alive = True
        if not are_alive:
            self.is_drowned = True


class ShipCounter:

    def __init__(self) -> None:
        self.single_ship = 0
        self.double_ship = 0
        self.three_ship = 0
        self.four_ship = 0

    def count_ship(self, ship_length: int) -> None:
        self.four_ship += 1 if ship_length == 4 else 0
        self.three_ship += 1 if ship_length == 3 else 0
        self.double_ship += 1 if ship_length == 2 else 0
        self.single_ship += 1 if ship_length == 1 else 0


class Battleship:

    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        ship_counter = ShipCounter()

        for ship in ships:
            new_ship = Ship(ship[0], ship[1])

            for x in range(ship[0][0], ship[1][0] + 1):
                for y in range(ship[0][1], ship[1][1] + 1):
                    self.field[(x, y)] = new_ship

            ship_counter.count_ship(new_ship.length)
        self._validate(ship_counter, ships)

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship:
            deck = ship.get_deck(location[0], location[1])
            if deck.is_alive:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for x in range(10):
            for y in range(10):
                ship = self.field.get((x, y))
                if ship:
                    deck = ship.get_deck(x, y)
                    if ship.is_drowned:
                        print("x", end="\t")
                    elif not deck.is_alive:
                        print("*", end="\t")
                    else:
                        print(u"\u25A1", end="\t")
                else:
                    print("~", end="\t")
            print()

    def _are_neighbor(self, ship1: Tuple, ship2: Tuple) -> bool:
        start1, end1 = ship1
        start2, end2 = ship2

        for x in range(start1[0] - 1, end1[0] + 2):
            for y in range(start1[1] - 1, end1[1] + 2):
                if start2[0] <= x <= end2[0] and start2[1] <= y <= end2[1]:
                    return True
        return False

    def _validate(self, counter: ShipCounter, ships: List) -> None:
        ships_len = (
            counter.four_ship,
            counter.three_ship,
            counter.double_ship,
            counter.single_ship
        )

        if ships_len != (1, 2, 3, 4) or sum(ships_len) != 10:
            raise ValueError("""
the total number of the ships should be 10
there should be 4 single-deck ships
there should be 3 double-deck ships
there should be 2 three-deck ships
there should be 1 four-deck ship
            """)

        for i in range(len(ships)):
            for j in range(i + 1, len(ships)):
                if self._are_neighbor(ships[i], ships[j]):
                    raise ValueError(
                        "Ships shouldn't be located in the neighboring cells"
                    )
