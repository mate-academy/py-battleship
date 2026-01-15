from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int],
                 end: Tuple[int, int], is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        else:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int],
                                         Tuple[int, int]]]) -> None:
        self.field = {}
        self.ships = []
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            hit = ship.fire(*location)
            if hit:
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = "□"
                else:
                    if ship.is_drowned:
                        field[deck.row][deck.column] = "x"
                    else:
                        field[deck.row][deck.column] = "*"
        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        ship_lengths = [len(ship.decks) for ship in self.ships]
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships.")
        if ship_lengths.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships.")
        if ship_lengths.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships.")
        if ship_lengths.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships.")
        if ship_lengths.count(4) != 1:
            raise ValueError("There should be 1 four-deck ship.")
        if not self._check_no_adjacent_ships():
            raise ValueError("Ships should not be "
                             "located in neighboring cells.")

    def _check_no_adjacent_ships(self) -> bool:
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for (row, col) in self.field:
            for dx, dy in directions:
                nx, ny = row + dx, col + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and (nx, ny) in self.field:
                    if self.field[(nx, ny)] != self.field[(row, col)]:
                        return False
        return True
