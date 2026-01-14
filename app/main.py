from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = True

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.start: Tuple[int, int] = start
        self.end: Tuple[int, int] = end
        self.decks: List[Deck] = self.create_decks(start, end)
        self.is_drowned: bool = False

    def create_decks(self,
                     start: Tuple[int, int],
                     end: Tuple[int, int]) -> List[Deck]:
        decks: List[Deck] = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))
        return decks

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.hit()
                break
        self.update_is_drowned()

    def update_is_drowned(self) -> None:
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field_representation: List[List[str]] = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if not deck.is_alive:
                    symbol = "x" if ship.is_drowned else "*"
                else:
                    symbol = "□"
                field_representation[deck.row][deck.column] = symbol
        for row in field_representation:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of ships should be 10")
        counts: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            length: int = len(ship.decks)
            if length in counts:
                counts[length] += 1
        if (
                counts
                [1] != 4 or counts[2] != 3 or counts[3] != 2 or counts[4] != 1
        ):
            raise ValueError("Invalid number of ships of each type")
        self._check_no_neighbors()

    def _check_no_neighbors(self) -> None:
        directions: List[Tuple[int, int]] = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for ship in self.ships:
            for deck in ship.decks:
                for direction in directions:
                    neighbor: Tuple[int, int] = (
                        deck.row + direction[0],
                        deck.column + direction[1]
                    )
                    if (
                            neighbor
                            in self.field and self.field[neighbor] != ship
                    ):
                        raise ValueError(
                            "Ships are located in neighboring cells"
                        )
