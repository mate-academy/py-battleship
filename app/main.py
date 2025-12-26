from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.position: Tuple[int, int] = (row, column)
        self.is_alive: bool = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: List[Deck] = self.make_ship()

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.position == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            if not deck.is_alive:
                return "Miss!"

            deck.is_alive = False

            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"

        return "Miss!"

    def make_ship(self) -> List[Deck]:
        start_x, start_y = self.start
        end_x, end_y = self.end

        ship: List[Deck] = []

        while True:
            ship.append(Deck(start_x, start_y))

            if (start_x, start_y) == (end_x, end_y):
                break

            if start_x < end_x:
                start_x += 1
            elif start_x > end_x:
                start_x -= 1

            if start_y < end_y:
                start_y += 1
            elif start_y > end_y:
                start_y -= 1

        return ship


class Battleship:
    def __init__(
            self,
            ships: List[
                Tuple[Tuple[int, int], Tuple[int, int]]
            ]
    ) -> None:
        self.field:\
            Dict[Tuple[Tuple[int, int], ...], Ship] = self._add_ship(ships)
        self._validate_field()

    @staticmethod
    def _add_ship(
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> Dict[Tuple[Tuple[int, int], ...], Ship]:
        ships_field: Dict[Tuple[Tuple[int, int], ...], Ship] = {}
        for item in ships:
            ship = Ship(item[0], item[1])
            ships_field[tuple(deck.position for deck in ship.decks)] = ship
        return ships_field

    def fire(self, location: Tuple[int, int]) -> str:
        for ship_decks, ship in self.field.items():
            if location in ship_decks:
                return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        field = []

        for rows in range(10):
            row = []
            for columns in range(10):
                cell = "~"
                for ship_decks in self.field:
                    if (rows, columns) in ship_decks:
                        ship = self.field[ship_decks]
                        deck = ship.get_deck(rows, columns)

                        if ship.is_drowned:
                            cell = "x"
                        elif deck.is_alive:
                            cell = "□"
                        else:
                            cell = "*"

                row.append(cell)
            field.append(row)

        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        self._validate_ships_amount()
        self._validate_ships_pos()

    def _validate_ships_amount(self) -> None:
        tests = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        for ship_decks in self.field:
            tests[len(ship_decks)] += 1

        assert tests[1] == 4
        assert tests[2] == 3
        assert tests[3] == 2
        assert tests[4] == 1
        assert sum(tests.values()) == 10

    @staticmethod
    def is_neighbor(
            self_deck: tuple[int, int],
            neighbor_dack: tuple[int, int]
    ) -> bool:
        self_x, self_y = self_deck
        neighbor_x, neighbor_y = neighbor_dack

        dx = abs(self_x - neighbor_x)
        dy = abs(self_y - neighbor_y)
        return max(dx, dy) == 1

    def _validate_ships_pos(self) -> None:
        for decks in self.field:
            for neighbors_decks in self.field:
                if decks == neighbors_decks:
                    continue
                for deck in decks:
                    for neighbor in neighbors_decks:
                        assert not self.is_neighbor(deck, neighbor)
