from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other: Deck) -> bool:
        if not isinstance(other, Deck):
            raise TypeError(f'"==" not supported between '
                            f'instances of {type(other)} and "Deck"')
        return self.row == other.row and self.column == other.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))


class Ship:
    def __init__(
            self,
            start: Deck,
            end: Deck,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if self.start.column == self.end.column:
            self.decks = [
                Deck(row=position, column=self.start.column)
                for position in range(self.start.row, self.end.row + 1)
            ]
        else:
            self.decks = [
                Deck(row=self.start.row, column=position)
                for position in range(self.start.column, self.end.column + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise BattleShipError("Ship deck does not exist")

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
        if any([deck.is_alive for deck in self.decks]) is False:
            self.is_drowned = True


class BattleShipError(Exception):
    pass


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship_tuple in ships:
            ship = Ship(
                start=Deck(row=ship_tuple[0][0], column=ship_tuple[0][1]),
                end=Deck(row=ship_tuple[1][0], column=ship_tuple[1][1])
            )
            for deck in ship.decks:
                self.field[deck] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        ship_shot = self.field.get(
            Deck(row=location[0], column=location[1]), "Miss!"
        )
        if ship_shot == "Miss!":
            return ship_shot
        else:
            ship_shot.fire(location[0], location[1])
            if ship_shot.is_drowned is True:
                return "Sunk!"
            return "Hit!"

    def print_field(self) -> None:
        field = ""
        for column in range(10):
            for row in range(10):
                ceil = self.field.get(Deck(row=row, column=column))
                if ceil is None:
                    field += "~ "
                elif ceil.is_drowned is True:
                    field += "x "
                else:
                    deck = ceil.get_deck(row, column)
                    if deck.is_alive:
                        field += "# "
                    else:
                        field += "* "
            field += "\n"
        print(field)

    def _validate_field(self) -> BattleShipError | None:
        if len(set(self.field.values())) != 10:
            raise BattleShipError("The number of ships should be 10.")

        ships_by_size = {
            "single_deck_ships": 0,
            "double_deck_ships": 0,
            "three_deck_ships": 0,
            "four_deck_ships": 0,
            "other_ships": 0
        }
        for ship in set(self.field.values()):
            decks_count = len(ship.decks)
            if decks_count == 1:
                ships_by_size["single_deck_ships"] += 1
            elif decks_count == 2:
                ships_by_size["double_deck_ships"] += 1
            elif decks_count == 3:
                ships_by_size["three_deck_ships"] += 1
            elif decks_count == 4:
                ships_by_size["four_deck_ships"] += 1
            elif decks_count > 4:
                ships_by_size["other_ships"] += 1
        if not ships_by_size == {
            "single_deck_ships": 4,
            "double_deck_ships": 3,
            "three_deck_ships": 2,
            "four_deck_ships": 1,
            "other_ships": 0
        }:
            raise BattleShipError("""In total,
            there can be 1 four-deck ship, 2 three-deck ships,
            3 two-deck ships and 4 single-deck ships.""")

        for ship in set(self.field.values()):
            for deck in ship.decks:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = deck.row + dr, deck.column + dc
                        if 0 <= nr < 10 and 0 <= nc < 10:
                            neighbor = Deck(row=nr, column=nc)
                            other_ship = self.field.get(neighbor)
                            if (
                                    other_ship is not None
                                    and other_ship is not ship
                            ):
                                raise BattleShipError("""Ships should not
                                be placed in close proximity.""")
