import random
from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = [Deck(row, column) for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
            self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.ships = []
        self.field = {(i, j): None for i in range(10) for j in range(10)}
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

        self.japan = Japan(self.field)
        self.dolphin = Dolphin(self.field, self.japan.location)

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            if self.field[location]:
                self.field[location].fire(*location)
                if not self.field[location].is_drowned:
                    return "Hit!"
                return "Sunk!"
            return "Miss!"

    def print_field(self) -> None:
        self.dolphin.swim(self.field)

        print_field = ""
        for location, cell in self.field.items():
            if cell is None:
                if location == self.japan.location:
                    print_field += "\N{silhouette of japan}	"
                elif location == self.dolphin.location:
                    print_field += "\N{dolphin}	"
                else:
                    print_field += "\N{water wave}	"
            elif cell.is_drowned:
                print_field += "\N{anger symbol}	"
            elif cell.get_deck(*location).is_alive:
                print_field += "\N{sailboat}	"
            else:
                print_field += "\N{fire}	"

            if location[1] == 9:
                print_field += "\n"
        print(print_field)

    def _validate_field(self) -> None:
        assert sorted(len(ship.decks) for ship in self.ships) == [
            1, 1, 1, 1,
            2, 2, 2,
            3, 3,
            4
        ], ("There should be 10 ships: 4 single-deck ships, "
            "3 double-deck ships, 2 three-deck ships and 1 four-deck ship")

        for ship in self.ships:
            for deck in ship.decks:
                surroundings = get_surroundings((deck.row, deck.column))
                for cell in surroundings:
                    if cell in self.field:
                        assert self.field[cell] in [None, ship], (
                            "ships shouldn't be located "
                            "in the neighboring cells"
                        )

        for ship in self.ships:
            decks = []
            for deck in ship.decks:
                decks.append((deck.row, deck.column))
            assert (len(set(deck[0] for deck in decks)) == 1
                    or len(set(deck[1] for deck in decks)) == 1), (
                "ships should be straight lines"
            )


class Japan:
    """Used to spawn Japan in the `Battleship.print_field` method."""
    def __init__(self, field_dict: Dict[Tuple[int, int], Ship | None]) -> None:
        empty_cells = [cell for cell in field_dict if not field_dict[cell]]
        self.location = random.choice(empty_cells)


class Dolphin:
    """
    Used to spawn Dolphin in the `Battleship.print_field` method. Dolphin moves
     into free neighboring cell every time `Battleship.print_field` method is
     called but sometimes stays in the same cell (to feed in fishy spot).
    """
    def __init__(self,
                 field_dict: Dict[Tuple[int, int], Ship | None],
                 japan_loc: Tuple[int, int]) -> None:
        empty_cells = [cell for cell in field_dict if not field_dict[cell]]
        self.land = empty_cells.remove(japan_loc)
        self.location = random.choice(empty_cells)
        self.land = japan_loc

    def swim(self, field_dict: Dict[Tuple[int, int], Ship | None]) -> None:
        new_loc = random.choice(get_surroundings(self.location))
        if new_loc in field_dict:
            if not field_dict[new_loc] and new_loc != self.land:
                self.location = new_loc


def get_surroundings(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    rows = (
        cell[0] - 1,
        cell[0],
        cell[0] + 1
    )
    columns = (
        cell[1] - 1,
        cell[1],
        cell[1] + 1
    )
    return [(i, j) for i in rows for j in columns]
