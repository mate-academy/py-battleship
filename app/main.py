from app import standard
from app.custom_exceptions import (
    LocationError,
    NumberOfTypesError,
    NumberOfShipsError
)


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (
                deck.row == row
                and deck.column == column
            ):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:

    def __init__(self, ships: list) -> None:
        self.art_field = standard.art_field
        self.field = {}
        self.ships = []
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            self.ships.append(new_ship)
            for deck in new_ship.decks:
                self.art_field[deck.row][deck.column] = standard.art_deck
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field(self.ships)

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                for deck in self.field[location].decks:
                    self.art_field[deck.row][deck.column] = standard.sunk
                return "Sunk!"
            self.art_field[location[0]][location[1]] = standard.hit
            return "Hit!"
        self.art_field[location[0]][location[1]] = standard.miss
        return "Miss!"

    def print_field(self) -> None:
        print(standard.border_u)
        for row in self.art_field:
            print(standard.border_l + "".join(row) + standard.border_r)
        print(standard.border_d + "\n")

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise NumberOfShipsError(
                f"There should be 10 ships on the "
                f"battlefield. You have: {len(ships)}"
            )
        counter_deck = [0, 0, 0, 0]
        for ship in self.ships:
            if len(ship.decks) in range(1, 5):
                counter_deck[len(ship.decks) - 1] += 1
        for i in range(len(counter_deck)):
            if counter_deck[i] != len(counter_deck) - i:
                raise NumberOfTypesError(
                    f"There should be {len(counter_deck) - i}"
                    f" {i + 1}-deck ships. "
                    f"You have: {counter_deck[i]}."
                )
        for row, column in self.field:
            check_deck = [-1, 0, 1]
            for i in check_deck:
                for j_i in check_deck:
                    if (row + i, column + j_i) in self.field:
                        if (
                            self.field[(row + i, column + j_i)]
                            is not self.field[(row, column)]
                        ):
                            raise LocationError(
                                "Your ships are too "
                                "close to each other"
                            )


if "__main__" == __name__:
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

    print(battle_ship.fire((5, 5)))
    battle_ship.print_field()
    print(battle_ship.fire((7, 2)))
    battle_ship.print_field()
    print(battle_ship.fire((0, 9)))
    battle_ship.print_field()
    print(battle_ship.fire((1, 4)))
    battle_ship.print_field()
    print(battle_ship.fire((1, 1)))
    battle_ship.print_field()
    print(battle_ship.fire((0, 0)))
    battle_ship.print_field()
    print(battle_ship.fire((0, 1)))
    battle_ship.print_field()
    print(battle_ship.fire((0, 2)))
    battle_ship.print_field()
    print(battle_ship.fire((0, 3)))
    battle_ship.print_field()
