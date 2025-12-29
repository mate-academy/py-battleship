from dataclasses import dataclass, field as fd

from app.ship import Ship
from app.errors import (
    NumberOfShipsError,
    CountShipsDecks,
    SpaceBetweenShips,
    FleetError
)


@dataclass
class Battleship:
    ships: list
    field: dict = fd(default_factory=dict)

    def __post_init__(self) -> None:
        self.field = {}
        self.ships = [
            Ship(*first_last_decks)
            for first_last_decks
            in self.ships
        ]
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def __repr__(self) -> str:
        text = "Battleship\nShips:\n"
        for ship in self.ships:
            text += f"{ship}\n"
        return text

    def fire(self, location: tuple) -> str:
        stricken_ship = self.field.get(location)
        if stricken_ship:
            stricken_ship.fire(*location)
            if stricken_ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        empty = "~"
        alive_deck = u"\u25A1"
        drowned = "x"
        destroyed_deck = "*"
        line = ""
        for row in range(0, 11):
            for column in range(0, 11):
                if (row, column) not in self.field:
                    line += empty
                elif self.field[(row, column)].get_deck(row, column):

                    line += alive_deck
                else:
                    if not self.field[(row, column)].is_drowned:
                        line += destroyed_deck
                    else:
                        line += drowned
            line += "\n"
        print(line)

    def _validate_number_of_ships(self) -> list:
        errors = []
        try:
            if len(self.ships) != 10:
                raise NumberOfShipsError(
                    f"the number of ships should be 10"
                    f" but received {len(self.ships)}")
        except NumberOfShipsError as e:
            errors.append(e)
        return errors

    def _validate_matching_decks(self) -> list:
        errors = []
        count_1_decks_ship = 0
        count_2_decks_ship = 0
        count_3_decks_ship = 0
        count_4_decks_ship = 0

        for ship in Ship.fleet:
            if ship.count_of_decks == 1:
                count_1_decks_ship += 1
            elif ship.count_of_decks == 2:
                count_2_decks_ship += 1
            elif ship.count_of_decks == 3:
                count_3_decks_ship += 1
            elif ship.count_of_decks == 4:
                count_4_decks_ship += 1

        try:
            if count_1_decks_ship != 4:
                raise CountShipsDecks(
                    f"There should be single-deck ships 4,"
                    f" received {count_1_decks_ship}")
        except CountShipsDecks as e:
            errors.append(e)
        try:
            if count_2_decks_ship != 3:
                raise CountShipsDecks(
                    f"There should be two-deck ships 3,"
                    f" received {count_2_decks_ship}")
        except CountShipsDecks as e:
            errors.append(e)
        try:
            if count_3_decks_ship != 2:
                raise CountShipsDecks(
                    f"There should be three-deck ships 2,"
                    f" received {count_3_decks_ship}")
        except CountShipsDecks as e:
            errors.append(e)
        try:
            if count_4_decks_ship != 1:
                raise CountShipsDecks(
                    f"There should be four-deck ships 1,"
                    f" received {count_4_decks_ship}")
        except CountShipsDecks as e:
            errors.append(e)
        return errors

    def _validate_approaching_ships(self) -> list:
        errors = []
        for deck, ship in self.field.items():
            for row in range(deck[0] - 1, deck[0] + 2):
                for column in range(deck[1] - 1, deck[1] + 2):
                    try:
                        if (
                            self.field.get((row, column))
                            and self.field.get((row, column))
                            is not ship
                        ):
                            raise SpaceBetweenShips(
                                f"next to the {ship} deck {deck}"
                                f" is the deck {(row, column)}"
                                f" of another {self.field.get((row, column))}")
                    except SpaceBetweenShips as e:
                        errors.append(e)
        return errors

    def _validate_field(self) -> None:
        errors = (
            self._validate_number_of_ships()
            + self._validate_matching_decks()
            + self._validate_approaching_ships()
        )

        if errors:
            text = ""
            for error in errors:
                text += str(error) + "\n"
            raise FleetError(text)
