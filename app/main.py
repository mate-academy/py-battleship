from app.exceptions import (
    ShipsCountException,
    ShipsTypesException,
    ShipsAreNeighboursException
)


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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

        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return False

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self._validate_field()

    def check_neighbourhood(self) -> bool:
        list_of_coordinates = []
        for ship in self.field.values():
            additional_list = []
            for deck in ship.decks:
                coordinates_of_deck = (deck.row, deck.column)
                if coordinates_of_deck not in list_of_coordinates:
                    list_of_coordinates.append(coordinates_of_deck)
                    additional_list.append((deck.row - 1, deck.column))
                    additional_list.append((deck.row + 1, deck.column))
                    additional_list.append((deck.row, deck.column + 1))
                    additional_list.append((deck.row, deck.column - 1))
                else:
                    return False
            list_of_coordinates.extend(additional_list)

        return True

    def _validate_field(self) -> bool:
        if len(self.field) == 10:
            length_of_ships = []
            for ship in self.field.values():
                length_of_ships.append(len(ship.decks))
            if (
                    length_of_ships.count(4) == 1
                    and length_of_ships.count(3) == 2
                    and length_of_ships.count(2) == 3
                    and length_of_ships.count(1) == 4
            ):

                if self.check_neighbourhood():
                    return True
                raise ShipsAreNeighboursException
            else:
                raise ShipsTypesException
        else:
            raise ShipsCountException

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"

        return "Miss!"

    def recieve_status_of_dot(self, ship: Ship, current_deck: Deck) -> str:
        if ship.is_drowned:
            return "x"
        if current_deck.is_alive:
            return u"\u25A1"
        return "*"

    def print_field(self) -> None:
        list_of_ships = [ship for ship in self.field.values()]
        for row in range(10):
            for column in range(10):
                is_deck_found = False
                for ship in list_of_ships:
                    current_deck = ship.get_deck(row, column)
                    if current_deck:
                        print(
                            self.recieve_status_of_dot(ship, current_deck),
                            end="   "
                        )

                        is_deck_found = True
                        break
                    else:
                        continue
                if is_deck_found is False:
                    print("~", end="   ")
            print("\n")
