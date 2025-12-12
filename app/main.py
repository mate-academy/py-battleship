FIELD_SIZE = 10
SYMBOL_WATER = u"~"
SYMBOL_ALIVE = u"\u25A1"
SYMBOL_HIT = u"*"
SYMBOL_SUNK = u"x"


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @property
    def location(self) -> tuple[int, int]:
        return self.row, self.column

    def __repr__(self) -> str:
        return (f"Deck({self.row}, "
                f"{self.column}, alive={self.is_alive})")


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.decks: list[Deck] = []
        self._is_drowned = is_drowned
        self._create_decks()

    @property
    def is_drowned(self) -> bool:
        return self._is_drowned

    @property
    def length(self) -> int:
        return len(self.decks)

    def _get_ship_coordinates(self) -> list[tuple[int, int]]:
        ((coordinates_x1, coordinates_y1),
         (coordinates_x2, coordinates_y2)) = self.start, self.end
        coords = []
        if coordinates_x1 == coordinates_x2:
            for coordinates_y in range(
                    min(coordinates_y1, coordinates_y2),
                    max(coordinates_y1, coordinates_y2) + 1):
                coords.append((coordinates_x1, coordinates_y))
        elif coordinates_y1 == coordinates_y2:
            for coordinates_x in range(
                    min(coordinates_x1, coordinates_x2),
                    max(coordinates_x1, coordinates_x2) + 1):
                coords.append((coordinates_x, coordinates_y1))
        else:
            pass
        return coords

    def _create_decks(self) -> None:
        coordinates = self._get_ship_coordinates()
        for coordinates_x, coordinates_y in coordinates:
            self.decks.append(Deck(coordinates_x, coordinates_y))

    def get_deck(self, row: int, column: int) -> Deck | None:
        location = (row, column)
        for deck in self.decks:
            if deck.location == location:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if not deck or not deck.is_alive:
            return "Miss!"
        deck.is_alive = False
        alive_count = sum(1 for d in self.decks if d.is_alive)
        if alive_count == 0:
            self._is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        self.ships: list[Ship] = []
        for ship_ends in ships:
            ship = Ship(ship_ends[0], ship_ends[1])
            self.ships.append(ship)
            for deck in ship.decks:
                location = deck.location
                if location in self.field:
                    raise ValueError(f"Кораблі "
                                     f"перетинаються у клітинці {location}.")
                self.field[location] = ship
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        coordinates_x, coordinates_y = location
        condition_1 = 0 <= coordinates_x < FIELD_SIZE
        condition_2 = 0 <= coordinates_y < FIELD_SIZE
        if not (condition_1 and condition_2):
            return "Miss!"
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        deck = ship.get_deck(coordinates_x, coordinates_y)
        if not deck.is_alive:

            return "Miss!"
        return ship.fire(coordinates_x, coordinates_y)

    def print_field(self) -> None:
        for coordinates_x in range(FIELD_SIZE):
            row_str = []
            for coordinates_y in range(FIELD_SIZE):
                location = (coordinates_x, coordinates_y)
                if location not in self.field:
                    row_str.append(SYMBOL_WATER)
                else:
                    ship = self.field[location]
                    deck = ship.get_deck(coordinates_x, coordinates_y)
                    if ship.is_drowned:
                        row_str.append(SYMBOL_SUNK)
                    elif deck.is_alive:
                        row_str.append(SYMBOL_ALIVE)
                    else:
                        row_str.append(SYMBOL_HIT)
            print("\t".join(row_str))

    def _validate_field(self) -> None:
        length_counts = {}
        for ship in self.ships:
            length_counts[ship.length] = length_counts.get(ship.length, 0) + 1
        required = {1: 4, 2: 3, 3: 2, 4: 1}
        if len(self.ships) != 10:
            raise ValueError(f"Неправильна загальна кількість "
                             f"кораблів: {len(self.ships)}. Очікується 10.")
        if length_counts != required:
            raise ValueError(f"Неправильний склад кораблів: "
                             f"{length_counts}. Очікується {required}.")
        neighbors = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for ship in self.ships:
            for deck in ship.decks:
                (coordinates_x, coordinates_y) = deck.location
                for dr, dc in neighbors:
                    nr, nc = coordinates_x + dr, coordinates_y + dc
                    neighbor_loc = (nr, nc)
                    if neighbor_loc in self.field:
                        neighbor_ship = self.field[neighbor_loc]
                        if neighbor_ship is not ship:
                            raise ValueError(
                                f"Кораблі розташовані надто близько: "
                                f"палуба {coordinates_x, coordinates_y} "
                                f"сусідить з палубою {nr, nc}.")
