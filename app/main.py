from typing import List, Tuple, Optional, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        if start[0] != end[0] and start[1] != end[1]:
            raise ValueError("Ships must be straight lines")

        self.is_drowned = is_drowned
        self.decks: List[Deck] = []

        row_start, row_end = min(start[0], end[0]), max(start[0], end[0])
        col_start, col_end = min(start[1], end[1]), max(start[1], end[1])

        for row_idx in range(row_start, row_end + 1):
            for col_idx in range(col_start, col_end + 1):
                self.decks.append(Deck(row_idx, col_idx))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck is not None:
            target_deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships_list: List[Ship] = []

        for start, end in ships:
            new_ship = Ship(start, end)

            for deck in new_ship.decks:
                if not (0 <= deck.row <= 9 and 0 <= deck.column <= 9):
                    raise ValueError("Coordinates out of range (0-9)")

                if (deck.row, deck.column) in self.field:
                    raise ValueError("Ships must not overlap")

                self.field[(deck.row, deck.column)] = new_ship

            self.ships_list.append(new_ship)

        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def _validate_field(self) -> None:
        if len(self.ships_list) != 10:
            raise ValueError("Fleet must have exactly 10 ships")

        ship_sizes = sorted(
            [len(ship.decks) for ship in self.ships_list], reverse=True
        )
        if ship_sizes != [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            raise ValueError("Invalid ship sizes composition")

        for ship in self.ships_list:
            for deck in ship.decks:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue

                        neighbor_pos = (deck.row + dr, deck.column + dc)

                        if neighbor_pos in self.field:
                            if self.field[neighbor_pos] != ship:
                                raise ValueError("Ships are touching!")
